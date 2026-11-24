#!/usr/bin/env python3
"""Improve a Russian story text with a local DeepSeek critic before it is rendered.

The critic reads a window of lines and returns strict JSON patches: a wrong stress mark, a word
the voice model will garble, a phrase that reads badly for a four year old. A second pass moves a
word across a line break when one line is too short or too long to breathe. Every patch is checked
against the same stress rules the renderer uses, and a rejected patch is never written.

The loop is bounded by --rounds and by a per-window patch cap. An unchanged story is a valid result.
The renderer caches by text, so a build after this loop synthesizes only the lines it touched.

usage: story_critique_loop.py STORY [--mode nighttime|morning] [--rounds 2] [--dry-run]
       [--endpoint URL] [--model ID] [--limit-lines N] [--max-patches 3]

Run this on your computer. It needs no model download and no GPU. It writes stories/STORY.stressed.txt,
the plain twin stories/STORY.txt, stories/STORY.critique.jsonl and .critique.json.
"""
import argparse
import datetime
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

from russian_quality_loop import stress_issues

HERE = Path(__file__).resolve().parent
STORIES = HERE / "stories"
VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
LATIN = re.compile(r"[A-Za-z]")
WORD = re.compile(r"[А-Яа-яЁё+]+")
WINDOW = 8
CONTEXT = 1
TARGET_MIN_S = 2.5
TARGET_MAX_S = 11.0
MIN_WORDS = 2
MAX_WORDS = 24

SYSTEM = (
    "Ты редактор русской детской книги для озвучки. Ты не пишешь историю заново. Ты чинишь ошибки. "
    "Словесное ударение помечено знаком + перед ударной гласной. Отвечай только JSON."
)


def utc_stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def seconds_per_byte(cfg: dict) -> float:
    """Speech seconds F5 gives one UTF-8 byte of text, at the generation speed.

    An empty window means the template has no recording yet. The critic then uses
    an 8 second example for the reference sentence. Set window_s after you record.
    """
    ref = cfg["reference"]
    ref_bytes = len(ref["text"].encode()) + 1
    window = ref["window_s"]
    ref_secs = float(window[1]) - float(window[0])
    if ref_secs <= 0:
        ref_secs = 8.0
    speed = float(cfg["generation"]["speed"])
    frames_per_sec = 24000 / 256
    return (ref_secs * frames_per_sec / ref_bytes) / speed / frames_per_sec


def estimate_seconds(text: str, per_byte: float) -> float:
    return max(0.0, len(text.encode()) * per_byte - 256 / 24000)


def chat(endpoint: str, model: str, messages: list[dict], timeout: float, temperature: float) -> str:
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": 0.9,
        "max_tokens": 2048,
        "chat_template_kwargs": {"enable_thinking": False},
    }).encode()
    request = urllib.request.Request(
        f"{endpoint.rstrip('/')}/chat/completions",
        data=body,
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as answer:
        payload = json.loads(answer.read().decode())
    return payload["choices"][0]["message"]["content"] or ""


def ask(endpoint: str, model: str, messages: list[dict], timeout: float, temperature: float,
        tries: int = 3) -> str:
    """The model answer, retried on a timeout, a dropped connection, a bad reply or an empty answer.
    A stalled local server once killed a whole build, so one window now costs three tries, not one."""
    last: Exception | None = None
    for attempt in range(tries):
        try:
            raw = chat(endpoint, model, messages, timeout, temperature)
            if raw.strip():
                return raw
            last = RuntimeError("empty answer")
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException, json.JSONDecodeError) as err:
            last = err
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"the model did not answer in {tries} tries: {last}")


def parse_json_block(raw: str) -> dict:
    """The first JSON object in the answer, with a ``` fence stripped."""
    text = re.sub(r"```(?:json)?", "", raw).strip()
    for start in (i for i, ch in enumerate(text) if ch == "{"):
        depth = 0
        for end in range(start, len(text)):
            depth += {"{": 1, "}": -1}.get(text[end], 0)
            if depth == 0:
                try:
                    value = json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    break
                if isinstance(value, dict):
                    return value
                break
    return {}


def line_problems(text: str, per_byte: float) -> list[str]:
    """Everything that makes a line unusable, by the renderer's own rules."""
    if not text.strip():
        return ["empty"]
    problems = []
    if LATIN.search(text):
        problems.append("latin letters")
    if re.search(r"\d", text):
        problems.append("digits")
    plain_words = [w for w in WORD.findall(text.replace("+", ""))]
    if not MIN_WORDS <= len(plain_words) <= MAX_WORDS:
        problems.append(f"{len(plain_words)} words")
    problems += [f"stress: {issue}" for issue in stress_issues(text)]
    seconds = estimate_seconds(text, per_byte)
    if not 1.5 <= seconds <= 13.0:
        problems.append(f"{seconds:.1f} s")
    return problems


def sentence_end(text: str) -> bool:
    return text.rstrip().endswith((".", "!", "?", "…", ":")) or text.rstrip().endswith("—")


def neighbours(lines: list[str], index: int) -> tuple[int | None, int | None]:
    before = next((i for i in range(index - 1, -1, -1) if lines[i].strip()), None)
    after = next((i for i in range(index + 1, len(lines)) if lines[i].strip()), None)
    return before, after


def join_problems(lines: list[str], index: int, new_text: str) -> list[str]:
    """Problems a line makes with the line before and the line after it."""
    before, after = neighbours(lines, index)
    problems = []
    old = lines[index].strip()
    starts_sentence = before is None or before == 0 or sentence_end(lines[before])
    if old[:1].isupper() and new_text[:1].islower() and starts_sentence:
        problems.append("starts a sentence but is lowercase")
    if old[:1].islower() and new_text[:1].isupper() and not starts_sentence:
        problems.append("continues a sentence but starts uppercase")
    def opening(text: str) -> str:
        return next((ch for ch in text if ch.isalpha()), "")

    if after is not None:
        if sentence_end(old) and not sentence_end(new_text) and opening(lines[after]).isupper():
            problems.append("drops the full stop but the next line starts a sentence")
        if not sentence_end(old) and sentence_end(new_text) and opening(lines[after]).islower():
            problems.append("adds a full stop but the next line continues in lowercase")
    return problems


def name_tokens(lines: list[str]) -> set[str]:
    """Words capitalised anywhere but at a line start, by their first four letters: the names."""
    found = set()
    for line in lines:
        for token in line.split()[1:]:
            letters = re.sub(r"[^А-Яа-яЁё]", "", token)
            if letters[:1].isupper():
                found.add(letters[:4].lower())
    return found


def apply_patch(lines: list[str], index: int, new_text: str, per_byte: float,
                check_join: bool = True, names: set[str] | None = None) -> tuple[bool, str]:
    """Replace one line in place when the new text passes every rule."""
    if not 0 <= index < len(lines):
        return False, "line is outside the story"
    new_text = " ".join(new_text.split())
    if new_text == lines[index].strip():
        return False, "unchanged"
    problems = line_problems(new_text, per_byte)
    names = names or set()
    for word in (w.replace("+", "") for w in re.findall(r"[А-Яа-яЁё+]+", new_text)):
        if word[:1].islower() and word[:4].lower() in names:
            problems.append(f"name written in lowercase: {word}")
    if check_join:
        problems += join_problems(lines, index, new_text)
    if problems:
        return False, "; ".join(problems)
    lines[index] = new_text
    return True, "ok"


def seam_pairs(lines: list[str], per_byte: float) -> list[int]:
    """Indexes of lines whose join to the next line is weak and worth moving words across.

    No seam across a blank line: a paragraph break is a deliberate beat. No seam on a refrain that
    repeats three times or more: its shortness is the point.
    """
    order = [i for i, line in enumerate(lines) if line.strip()]
    counts = Counter(lines[i].strip() for i in order)
    out = []
    for here, following in zip(order, order[1:]):
        if following != here + 1:
            continue
        if counts[lines[here].strip()] >= 3:
            continue
        seconds = estimate_seconds(lines[here], per_byte)
        if seconds > TARGET_MAX_S or seconds < TARGET_MIN_S:
            out.append(here)
    return out


def window_prompt(lines: list[str], targets: list[int], per_byte: float, mode: str, limit: int) -> str:
    shown = range(max(0, targets[0] - CONTEXT), min(len(lines), targets[-1] + CONTEXT + 1))
    return (
        f"Режим: {mode}. Номера от {targets[0] + 1} до {targets[-1] + 1} можно править, остальные строки — контекст.\n"
        "После каждой строки в скобках её длина в секундах при этой скорости. Пустая строка — новый абзац.\n\n"
        + "\n".join(
            f"{i + 1}. {lines[i]}  [{estimate_seconds(lines[i], per_byte):.1f} s]"
            for i in shown if lines[i].strip()
        )
        + f"\n\nНайди не больше {limit} настоящих ошибок: неверное ударение, слово, которое синтезатор "
        "произнесёт неверно, неестественный порядок слов. Смысл и число предложений не меняй, "
        f"держи {MIN_WORDS}-{MAX_WORDS} слов в строке. Если строка хороша, не трогай её.\n"
        'Ответ: {"patches": [{"line": 12, "text": "новая строка", "why": "коротко"}]}\n'
        "Пустой список patch — это нормальный ответ."
    )


def seam_prompt(lines: list[str], index: int, following: int, per_byte: float) -> str:
    a, b = lines[index], lines[following]
    return (
        "Две соседние строки. Одна из них слишком короткая или слишком длинная для вдоха.\n\n"
        f"{index + 1}. {a}  [{estimate_seconds(a, per_byte):.1f} s]\n"
        f"{following + 1}. {b}  [{estimate_seconds(b, per_byte):.1f} s]\n\n"
        "Перенеси одно-два слова через границу так, чтобы обе строки стали по 3-14 слов и шов звучал "
        "естественно. Слова и ударения сохрани. Точку ставь только в конце второго предложения, "
        "первую строку не заканчивай точкой, если предложение продолжается.\n"
        f'Ответ: {{"line": {index + 1}, "text": "первая строка", "next": "вторая строка", "why": "коротко"}}\n'
    )


def run_window(args, lines, targets, per_byte, log, names) -> int:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": window_prompt(lines, targets, per_byte, args.mode, args.max_patches)},
    ]
    raw = ask(args.endpoint, args.model, messages, args.timeout, args.temperature)
    log({"phase": "patch", "from": targets[0] + 1, "to": targets[-1] + 1, "raw": raw})
    applied = 0
    for patch in parse_json_block(raw).get("patches", [])[: args.max_patches + 2]:
        try:
            index = int(patch["line"]) - 1
        except (KeyError, TypeError, ValueError):
            log({"phase": "patch", "rejected": patch, "reason": "no line number"})
            continue
        if index not in targets:
            log({"phase": "patch", "rejected": patch, "reason": "outside the window"})
            continue
        ok, why = apply_patch(lines, index, str(patch.get("text", "")), per_byte, names=names)
        log({"phase": "patch", "line": index + 1, "text": patch.get("text"), "why": patch.get("why"),
             "accepted": ok, "reason": why})
        applied += ok
    return applied


def run_seam(args, lines, index, following, per_byte, log, names) -> int:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": seam_prompt(lines, index, following, per_byte)},
    ]
    raw = ask(args.endpoint, args.model, messages, args.timeout, args.temperature)
    log({"phase": "seam", "line": index + 1, "raw": raw})
    data = parse_json_block(raw)
    first, second = str(data.get("text", "")), str(data.get("next", ""))
    if not first or not second:
        log({"phase": "seam", "line": index + 1, "accepted": False, "reason": "missing text"})
        return 0
    old_first, old_second = lines[index], lines[following]
    ok_first, why_first = apply_patch(lines, index, first, per_byte, check_join=False, names=names)
    if not ok_first:
        log({"phase": "seam", "line": index + 1, "accepted": False, "reason": why_first})
        return 0
    ok_second, why_second = apply_patch(lines, following, second, per_byte, check_join=False, names=names)
    if not ok_second:
        lines[index] = old_first
        log({"phase": "seam", "line": index + 1, "accepted": False, "reason": f"second line: {why_second}"})
        return 0
    problems = join_problems(lines, index, first) + join_problems(lines, following, second)
    if problems:
        lines[index], lines[following] = old_first, old_second
        log({"phase": "seam", "line": index + 1, "accepted": False, "reason": "; ".join(problems)})
        return 0
    log({"phase": "seam", "line": index + 1, "next": following + 1, "accepted": True, "why": data.get("why"),
         "before": [old_first, old_second], "after": [first, second]})
    return 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Improve a story text with a local DeepSeek critic.")
    ap.add_argument("story")
    ap.add_argument("--mode", choices=("nighttime", "morning"), default="nighttime")
    ap.add_argument("--rounds", type=int, default=2, help="critique passes over the text")
    ap.add_argument("--max-patches", type=int, default=3, help="patch cap per window")
    ap.add_argument("--limit-lines", type=int, default=0, help="only the first N lines, for a trial")
    ap.add_argument("--endpoint", default="http://127.0.0.1:18888/v1")
    ap.add_argument("--model", default="deepseek-v4.1-flash")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--timeout", type=float, default=180.0)
    ap.add_argument("--config", default=str(HERE / "config/russian-standard.json"))
    ap.add_argument("--dry-run", action="store_true", help="write nothing, print the accepted patches")
    args = ap.parse_args()

    if args.rounds < 1:
        ap.error("--rounds must be at least 1")
    source = STORIES / f"{args.story}.stressed.txt"
    if not source.is_file():
        sys.exit(f"no story: {source}")
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    per_byte = seconds_per_byte(cfg)

    text = source.read_text(encoding="utf-8")
    original = text.splitlines()
    lines = [line.strip() for line in original]
    if args.limit_lines:
        lines = lines[: args.limit_lines]
    if not lines or not lines[0]:
        sys.exit(f"the first line of {source} must be the title")
    if not any(line.strip() for line in lines[1:]):
        sys.exit("no story lines after the title")

    stamp = utc_stamp()
    log_path = STORIES / f"{args.story}.critique.jsonl"
    handle = log_path.open("a", encoding="utf-8")

    def log(record: dict) -> None:
        handle.write(json.dumps({"ts": stamp, **record}, ensure_ascii=False) + "\n")
        handle.flush()
        for key in ("line", "from"):
            if key in record and record.get("accepted"):
                print(f"  accepted line {record['line']}" if "line" in record else f"  window {record['from']}", flush=True)
                break

    total = 0
    try:
        for round_number in range(1, args.rounds + 1):
            print(f"round {round_number}: patches", flush=True)
            order = [i for i in range(1, len(lines)) if lines[i].strip()]  # line 0 is the title
            names = name_tokens(lines)
            for start in range(0, len(order), WINDOW):
                total += run_window(args, lines, order[start: start + WINDOW], per_byte, log, names)
            if round_number < args.rounds:
                print(f"round {round_number}: seams", flush=True)
                for index in seam_pairs(lines, per_byte):
                    following = next(i for i in range(index + 1, len(lines)) if lines[i].strip())
                    total += run_seam(args, lines, index, following, per_byte, log, name_tokens(lines))
    finally:
        handle.close()

    stressed = "\n".join(lines) + "\n"
    plain = re.sub(r"\+", "", stressed)
    issues = stress_issues(stressed)
    changed = sum(1 for a, b in zip(original, lines) if a != b)
    print(f"{changed} lines changed, {total} patches accepted, {len(issues)} stress issues after the loop")
    if args.dry_run:
        for number, (before, after) in enumerate(zip(original, lines), 1):
            if before != after:
                print(f"  {number}: {before}\n  {' ' * len(str(number))}  -> {after}")
        return
    backup = STORIES / f"{args.story}.stressed.txt.{stamp}.bak"
    backup.write_text(text, encoding="utf-8")
    source.write_text(stressed, encoding="utf-8")
    (STORIES / f"{args.story}.txt").write_text(plain, encoding="utf-8")
    (STORIES / f"{args.story}.critique.json").write_text(json.dumps({
        "story": args.story,
        "model": args.model,
        "endpoint": args.endpoint,
        "mode": args.mode,
        "rounds": args.rounds,
        "lines_changed": changed,
        "patches_accepted": total,
        "stress_issues_after": issues,
        "source": str(source),
        "backup": str(backup),
        "text_sha256_before": __import__("hashlib").sha256(text.encode()).hexdigest(),
        "text_sha256_after": __import__("hashlib").sha256(stressed.encode()).hexdigest(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"backup {backup.name}")


if __name__ == "__main__":
    main()