#!/usr/bin/env python3
"""Write a long Russian bedtime story from a brief, with the local DeepSeek model.

usage: long_story.py NAME [--brief briefs/NAME.json] [--chapters 11] [--minutes 20]
       [--dry-run] [--redo N ...] [--skip-stress] [--skip-critique] [--check]

Four stages. The plan names the cast, the places, the refrain and one beat per chapter.
The draft asks for one chapter at a time and carries a continuity sheet forward.
The check runs the critic from story_critique_loop.py and then the hard rules below.
The stress stage copies the text to the Ubuntu PC, runs add_stress.py there and pulls it back.

Every request and every reply is appended to stories/NAME.writer.jsonl. A rerun resumes
from that log: a chapter already drafted is not asked for again unless it is in --redo.
The critic is an existing script with its own request settings. It is not changed here.

Run this on the Mac. The model is http://127.0.0.1:18888/v1, model deepseek-v4.1-flash.
"""
import argparse
import datetime
import http.client
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import story_modes
from story_critique_loop import parse_json_block
from russian_quality_loop import stress_issues

HERE = Path(__file__).resolve().parent
STORIES = HERE / "stories"
BRIEFS = HERE / "briefs"
VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")
LATIN = re.compile(r"[A-Za-z]")
WORD = re.compile(r"[А-Яа-яЁё+]+")
HEADING = re.compile(r"^# Глава (\d+)\. \S")
SENTENCE_END = (".", "!", "?", "…", ":")
MIN_WORDS, MAX_WORDS = 2, 24       # the renderer's own per-line rule
PARAGRAPH_MIN, PARAGRAPH_MAX = 3, 6
CHAPTER_MIN, CHAPTER_MAX = 180, 220
DRAFT_TRIES = 4
ENDPOINT = "http://127.0.0.1:18888/v1"
MODEL = "deepseek-v4.1-flash"
TEMPERATURE = 0.2
TIMEOUT = 4 * 3600.0
MAX_TOKENS = 98304
HOST = os.environ.get("NARRATION_HOST", "")
RUNTIME = os.environ.get("NARRATION_DEST", "bedtime-audiobooks")

# Words RUAccent missed in this week's stories. The map grows when a new miss appears.
HAND_STRESS = {
    "если": "+если",
    "стали": "ст+али",
    "ого": "ог+о",
    "лапкой": "л+апкой",
    "вздохнул": "вздохн+ул",
    "лунный": "л+унный",
    "лунного": "л+унного",
    "луну": "лун+у",
    "луна": "лун+а",
    "лучик": "л+учик",
    "лодочка": "л+одочка",
    "лодочку": "л+одочку",
    "лодочке": "л+одочке",
    "плывёт": "плывёт",
    "плывет": "плыв+ет",
    "течёт": "течёт",
    "течет": "теч+ет",
    "пик": "пик",
    "бобры": "бобр+ы",
    "бобров": "бобр+ов",
    "бобрёнок": "бобрёнок",
    "цапля": "ц+апля",
    "сова": "сов+а",
    "светлячки": "светлячк+и",
    "фонарик": "фон+арик",
    "фонарика": "фон+арика",
    "фонариком": "фон+ариком",
    "мышонок": "мыш+онок",
    "мышонка": "мыш+онка",
    "мышка": "м+ышка",
    "река": "рек+а",
    "реке": "рек+е",
    "реку": "рек+у",
    # The lodochka headings and the eleven lines RUAccent refused to mark.
    "глава": "глав+а",
    "камышей": "камыш+ей",
    "бобровой": "бобр+овой",
    "запруды": "запр+уды",
    "лягушачьей": "лягуш+ачьей",
    "отмели": "+отмели",
    "кустом": "куст+ом",
    "утиного": "ут+иного",
    "островка": "островк+а",
    "старого": "ст+арого",
    "старой": "ст+арой",
    "дуба": "д+уба",
    "лисьей": "л+исьей",
    "норы": "нор+ы",  # genitive «у норы». The plural «но́ры» needs a hand mark.
    "ольшанике": "ольш+анике",
    "медвежьей": "медв+ежьей",
    "берлоги": "берл+оги",
    "ивы": "+ивы",
    "дома": "д+ома",  # the adverb «дома» (at home). The plural «дома» (houses) has the stress on the end.
    "мои": "мо+и",
    "она": "он+а",
    "только": "т+олько",
    "дышит": "д+ышит",
    "светит": "св+етит",
    "еле": "+еле",
}

SYSTEM = (
    "Ты пишешь русскую сказку на ночь для ребёнка трёх лет. Её будут читать вслух. "
    "Пиши тепло и очень просто. Отвечай только JSON."
)


def utc_stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def words(line: str) -> list[str]:
    return WORD.findall(line.replace("+", ""))


def body_words(lines: list[str]) -> int:
    return sum(len(words(line)) for line in lines if line.strip() and not line.startswith("# "))


# --------------------------------------------------------------------------- checks


def chapter_problems(lines: list[str], refrain: list[str],
                     minimum: int = CHAPTER_MIN, maximum: int = CHAPTER_MAX) -> list[str]:
    """The hard rules for one chapter. `lines` holds body lines and blank lines, no heading."""
    lines = [line.replace("+", "") for line in lines]  # a hand-marked plain file checks the same
    while lines and not lines[-1].strip():
        lines.pop()
    problems = []
    count = sum(len(words(line)) for line in lines)
    if not minimum <= count <= maximum:
        problems.append(f"{count} words, expected {minimum}-{maximum}")
    for line in lines:
        if not line.strip():
            continue
        if LATIN.search(line):
            problems.append(f"latin letters: {line}")
        if re.search(r"\d", line):
            problems.append(f"digits: {line}")
        n = len(words(line))
        if not MIN_WORDS <= n <= MAX_WORDS:
            problems.append(f"{n} words in one line: {line}")
        if not line.rstrip().endswith(SENTENCE_END):
            problems.append(f"line does not end a sentence: {line}")
    if list(lines[-len(refrain):]) != list(refrain):
        problems.append("the chapter does not end with the refrain")
    refrain_keys = {" ".join(line.split()).lower() for line in refrain}
    seen: set[str] = set()
    for line in lines:
        key = " ".join(line.split()).lower()
        if not key or key in refrain_keys:
            continue
        if key in seen:
            problems.append(f"repeated line: {line}")
        seen.add(key)
    paragraphs, current = [], []
    for line in lines + [""]:
        if line.strip():
            current.append(line)
        elif current:
            paragraphs.append(current)
            current = []
    for paragraph in paragraphs[:-1]:
        if not PARAGRAPH_MIN <= len(paragraph) <= PARAGRAPH_MAX:
            problems.append(f"paragraph of {len(paragraph)} lines: {paragraph[0]}")
    if paragraphs and list(paragraphs[-1]) != list(refrain):
        problems.append("the refrain is not its own last paragraph")
    return problems


def split_chapters(lines: list[str]) -> list[tuple[str, list[str]]]:
    """(heading, body lines) per chapter. Chapter 0 is a body before the first heading."""
    chapters: list[tuple[str, list[str]]] = []
    heading, current = "", []
    for line in lines:
        if line.startswith("# "):
            if current or heading:
                chapters.append((heading, current))
            heading, current = line, []
        else:
            current.append(line)
    if current or heading:
        chapters.append((heading, current))
    return chapters


def story_problems(text: str, refrain: list[str], chapters: int, mode: str,
                   minimum: int = CHAPTER_MIN, maximum: int = CHAPTER_MAX,
                   total_min: int | None = None, total_max: int | None = None) -> list[str]:
    """The hard rules for the whole file, in contract C1 form."""
    lines = text.splitlines()
    problems = []
    if not lines or not lines[0].strip() or lines[0].startswith("# "):
        return ["the first line must be the title"]
    if len(lines) < 2 or lines[1].strip():
        problems.append("a blank line must follow the title")
    if any(LATIN.search(line) or re.search(r"\d", line) for line in lines[1:] if not line.startswith("# ")):
        problems.append("latin letters or digits in the body")
    parts = split_chapters(lines[1:])
    numbered = [(heading, body) for heading, body in parts if heading]
    if len(numbered) != chapters:
        problems.append(f"{len(numbered)} numbered chapters, expected {chapters}")
    for number, (heading, body) in enumerate(numbered, 1):
        match = HEADING.match(heading.replace("+", ""))
        if not match:
            problems.append(f"bad heading: {heading}")
        elif int(match.group(1)) != number:
            problems.append(f"heading out of order: {heading}")
        problems += [f"chapter {number}: {p}" for p in chapter_problems(body, refrain, minimum, maximum)]
    for heading, body in parts:
        if not heading and any(line.strip() for line in body):
            problems += [f"opening: {p}" for p in
                         chapter_problems(body, refrain, 0, 10 ** 6) if "refrain" not in p and "paragraph" not in p]
    cues = story_modes.cue_score(text)
    other = "morning" if mode == "nighttime" else "nighttime"
    if cues[mode] - cues[other] < story_modes.CUE_MARGIN:
        problems.append(f"cue words do not place the {mode} mode: {cues}")
    opening = "\n".join(lines[:story_modes.OPENING_LINES]).lower().replace("ё", "е")
    cues_for_mode = story_modes.NIGHT_CUES if mode == "nighttime" else story_modes.MORNING_CUES
    if not any(cue.replace("ё", "е") in opening for cue in cues_for_mode):
        problems.append(f"no {mode} cue in the first eight lines")
    if total_min is not None and total_max is not None:
        total = body_words(lines[1:])
        if not total_min <= total <= total_max:
            problems.append(f"{total} body words, expected {total_min}-{total_max}")
    return problems


def stress_problems(plain: str, stressed: str) -> list[str]:
    """Every stress problem in a plain and stressed pair, in the renderer's own rules."""
    problems = list(stress_issues(stressed))
    left, right = plain.splitlines(), stressed.splitlines()
    if len(left) != len(right):
        problems.append(f"line counts differ: {len(left)} and {len(right)}")
    for number, (a, b) in enumerate(zip(left, right), 1):
        if a.replace("+", "") != b.replace("+", ""):
            problems.append(f"line {number}: the texts differ after removing +")
    return problems


def correction_map() -> dict:
    table = json.loads((HERE / "config/russian-stress-corrections.json").read_text(encoding="utf-8"))
    table.update(HAND_STRESS)
    return {key.lower(): value for key, value in table.items()}


def hand_mark(line: str, table: dict) -> tuple[str, list[str]]:
    """Fill the missing marks on one stressed line from the correction map.

    add_stress.py keeps a line that already contains a plus, so the corrected line is
    written back into the plain file and the next run keeps every mark on it.
    """
    still_missing = []

    def fix(match: re.Match) -> str:
        token = match.group(0)
        letters = token.replace("+", "")
        if "+" in token or "ё" in letters.lower():
            return token
        if sum(ch in VOWELS for ch in letters) < 2:
            return token
        marked = table.get(letters.lower())
        if marked is None:
            still_missing.append(letters)
            return token
        return marked[:1].upper() + marked[1:] if letters[:1].isupper() else marked

    return WORD.sub(fix, line), still_missing


# --------------------------------------------------------------------------- the model


def chat(endpoint: str, model: str, messages: list[dict]) -> dict:
    """One completion call. Max reasoning, thinking on, four hour timeout."""
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": TEMPERATURE,
        "top_p": 0.9,
        "max_tokens": MAX_TOKENS,
        "reasoning_effort": "max",
        "chat_template_kwargs": {"enable_thinking": True},
    }, ensure_ascii=False).encode()
    request = urllib.request.Request(
        f"{endpoint.rstrip('/')}/chat/completions",
        data=body,
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
        return json.loads(answer.read().decode())


class Log:
    """The writer journal. Every request and reply is on disk before the next call."""

    def __init__(self, path: Path):
        self.path = path
        self.handle = path.open("a", encoding="utf-8")

    def write(self, record: dict) -> None:
        self.handle.write(json.dumps({"ts": utc_stamp(), **record}, ensure_ascii=False) + "\n")
        self.handle.flush()

    def close(self) -> None:
        self.handle.close()


def load_log(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # a crash can leave one half written line
    return records


def drafted_chapters(records: list[dict], redo: set[int]) -> dict[int, dict]:
    """The accepted draft of every chapter in the log, minus the ones --redo names."""
    chapters: dict[int, dict] = {}
    for record in records:
        if record.get("stage") == "draft" and record.get("ok"):
            chapters[int(record["chapter"])] = record
    return {n: record for n, record in chapters.items() if n not in redo}


def saved_plan(records: list[dict]) -> dict | None:
    for record in reversed(records):
        if record.get("stage") == "plan" and record.get("ok"):
            return record.get("plan")
    return None


def ask_model(log: Log, stage: str, messages: list[dict], chapter: int | None = None,
              tries: int = 3, endpoint: str = ENDPOINT, model: str = MODEL) -> str:
    """The model's answer text, with the request and the reply in the journal."""
    last: Exception | None = None
    for attempt in range(1, tries + 1):
        log.write({"stage": stage, "chapter": chapter, "event": "request",
                   "attempt": attempt, "messages": messages})
        try:
            payload = chat(endpoint, model, messages)
            message = payload["choices"][0]["message"]
            raw = message.get("content") or ""
            log.write({"stage": stage, "chapter": chapter, "event": "reply", "attempt": attempt,
                       "content": raw, "reasoning": message.get("reasoning_content"),
                       "usage": payload.get("usage")})
            if raw.strip():
                return raw
            last = RuntimeError("empty answer")
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException,
                json.JSONDecodeError, KeyError, IndexError) as err:
            last = err
            log.write({"stage": stage, "chapter": chapter, "event": "error", "error": str(err)})
        time.sleep(5 * attempt)
    raise RuntimeError(f"{stage}: the model did not answer in {tries} tries: {last}")


# --------------------------------------------------------------------------- stages


def plan_prompt(brief: dict, chapters: int) -> list[dict]:
    bends = "\n".join(f"{i}. {beat}" for i, beat in enumerate(brief["bends"], 1))
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": (
            f"Составь план сказки «{brief['title']}».\n{brief['premise']}\n\n"
            f"Повороты реки по главам:\n{bends}\n\n"
            f"Припев, который заканчивает каждую главу: {' '.join(brief['refrain'])}\n"
            f"Правила: {' '.join(brief['rules'])}\n\n"
            f"Глав ровно {chapters}. Ответ — один JSON объект:\n"
            '{"cast": [{"name", "kind", "trait", "speech"}], '
            '"places": ["места по порядку"], '
            '"refrain": ["строка", "строка"], '
            '"recurring": ["три повторяющихся предмета или фразы"], '
            '"chapters": [{"title", "beat", "quieter", "cast": ["имя"]}]}\n'
            "В quieter напиши, как глава кончается тише, чем началась."
        )},
    ]


def chapter_prompt(brief: dict, plan: dict, number: int, minimum: int, maximum: int,
                   facts: list[str], tail: list[str], problems: list[str]) -> list[dict]:
    beat = plan["chapters"][number - 1]
    cast = "; ".join(f"{c['name']} — {c['kind']}, {c['trait']}, {c['speech']}" for c in plan["cast"])
    previous = "\n".join(tail) if tail else "это первая глава"
    retry = ""
    if problems:
        retry = "\nВ прошлой попытке были ошибки, исправь их:\n" + "\n".join(f"- {p}" for p in problems) + "\n"
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": (
            f"Напиши главу {number} сказки «{brief['title']}» из {len(plan['chapters'])}.\n"
            f"Название главы: {beat['title']}.\nЧто происходит: {beat['beat']}\n"
            f"Чем глава кончается тише: {beat['quieter']}\n"
            f"Герои: {cast}\nВ этой главе: {', '.join(beat['cast'])}.\n"
            f"Повторяющиеся предметы и фразы: {', '.join(plan['recurring'])}.\n\n"
            f"Уже установлено в прошлых главах, не противоречь:\n"
            + ("\n".join(f"- {f}" for f in facts) if facts else "- ничего, это первая глава")
            + f"\n\nПоследние строки прошлой главы:\n{previous}\n\n"
            f"Правила текста:\n"
            f"- от {minimum} до {maximum} слов, это важно;\n"
            "- настоящее время, короткие предложения;\n"
            "- одна строка — одно законченное предложение, от двух до двадцати четырёх слов;\n"
            "- абзац — от трёх до шести предложений;\n"
            "- слова понятны ребёнку трёх лет;\n"
            "- никаких страхов, опасностей, погони, никто не теряется;\n"
            "- только русские буквы, числа пиши словами, без цифр;\n"
            "- не повторяй одно и то же предложение дважды, кроме припева;\n"
            "- не пиши о самой сказке, о главе и о припеве, только о том, что происходит;\n"
            "- в конце отдельным абзацем припев, две строки, дословно:\n"
            + "\n".join(brief["refrain"])
            + ("\n- в первых строках этой главы слова: вечер, ночь, луна, спать." if number == 1 else "")
            + f"\n{retry}\n"
            'Ответ — один JSON объект: {"title": "название главы", '
            '"paragraphs": [["предложение", "предложение"], ["..."]], '
            '"facts": ["новые факты этой главы для следующих глав"]}\n'
            "Припев тоже входит в paragraphs, последним абзацем."
        )},
    ]


def chapter_lines(data: dict, refrain: list[str]) -> list[str]:
    """Body lines from the model's JSON, or from plain text when the JSON is absent."""
    paragraphs = data.get("paragraphs")
    lines: list[str] = []
    if isinstance(paragraphs, list) and paragraphs:
        for paragraph in paragraphs:
            if isinstance(paragraph, str):
                paragraph = [paragraph]
            for line in paragraph:
                line = " ".join(str(line).split())
                if line and not line.startswith("# "):
                    lines.append(line)
            lines.append("")
    else:
        text = str(data.get("text", ""))
        for line in text.splitlines():
            line = " ".join(line.split())
            if line.startswith("# "):
                continue
            lines.append(line)
    while lines and not lines[-1]:
        lines.pop()
    paragraphs, current = [], []
    for line in lines + [""]:
        if line.strip():
            current.append(line)
        elif current:
            paragraphs.append(current)
            current = []
    if paragraphs and any(line in refrain for line in paragraphs[-1]):
        paragraphs.pop()  # the model's own closing lines are replaced by the exact refrain
    lines = [line for paragraph in paragraphs for line in paragraph + [""]]
    while lines and not lines[-1]:
        lines.pop()
    if lines[-len(refrain):] != refrain:
        lines += [""] + list(refrain)
    return lines


def assemble(title: str, plan: dict, drafts: dict[int, dict]) -> str:
    out = [title, ""]
    for number in sorted(drafts):
        record = drafts[number]
        heading = record.get("title") or plan["chapters"][number - 1]["title"]
        out.append(f"# Глава {number}. {heading}")
        out.extend(record["lines"])
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def chapter_word_counts(text: str) -> list[tuple[str, int]]:
    counts = []
    for heading, body in split_chapters(text.splitlines()[1:]):
        if heading:
            counts.append((heading, body_words(body)))
    return counts


# --------------------------------------------------------------------------- the PC


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(command)}: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout


def stress_on_pc(name: str) -> str:
    """Copy the plain text to the render machine, mark it there, pull the stressed text back."""
    if not HOST:
        raise RuntimeError("NARRATION_HOST is not set")
    txt = STORIES / f"{name}.txt"
    run(["ssh", HOST, f"mkdir -p {RUNTIME}/stories"])
    run(["scp", "-q", str(txt), f"{HOST}:{RUNTIME}/stories/"])
    out = run(["ssh", HOST, f"cd {RUNTIME} && nice -n 10 ./ruaccent-env/bin/python add_stress.py "
                            f"stories/{name}.txt stories/{name}.stressed.txt"])
    print(out.strip(), flush=True)
    run(["scp", "-q", f"{HOST}:{RUNTIME}/stories/{name}.stressed.txt", str(STORIES / f"{name}.stressed.txt")])
    return (STORIES / f"{name}.stressed.txt").read_text(encoding="utf-8")


def fix_stress(name: str) -> None:
    """Mark the misses by hand and rerun until the pair is clean."""
    table = correction_map()
    for attempt in range(1, 6):
        plain = (STORIES / f"{name}.txt").read_text(encoding="utf-8")
        stressed = stress_on_pc(name)
        problems = stress_problems(plain, stressed)
        if not problems:
            print(f"stress: clean after {attempt} run(s)", flush=True)
            return
        print(f"stress run {attempt}: {len(problems)} problems", flush=True)
        missing: set[str] = set()
        lines = stressed.splitlines()
        changed = False
        for index, line in enumerate(lines):
            fixed, misses = hand_mark(line, table)
            missing.update(misses)
            if fixed != line:
                lines[index] = fixed
                changed = True
        if not changed:
            raise RuntimeError("stress: no correction for " + ", ".join(sorted(missing))
                               + "\n" + "\n".join(problems[:20]))
        (STORIES / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    raise RuntimeError("stress: still not clean after five runs")


def run_critic(name: str, mode: str, rounds: int) -> dict:
    """The existing critic, unchanged. It writes the plain twin and both report files."""
    command = [sys.executable, "-B", str(HERE / "story_critique_loop.py"), name,
               "--mode", mode, "--rounds", str(rounds)]
    print("critic: " + " ".join(command), flush=True)
    result = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
    print(result.stdout.strip(), flush=True)
    if result.returncode != 0:
        raise RuntimeError(f"critic failed: {result.stderr.strip()}")
    counts = {"accepted": 0, "rejected": 0}
    log_path = STORIES / f"{name}.critique.jsonl"
    for record in load_log(log_path):
        if record.get("accepted") is True:
            counts["accepted"] += 1
        elif record.get("accepted") is False or "rejected" in record:
            counts["rejected"] += 1
    return counts


def restore_fixed_lines(name: str, headings: list[str], refrain: list[str]) -> None:
    """The headings and the refrain are ours, not the critic's. Put both back after the loop."""
    plain_path = STORIES / f"{name}.txt"
    stressed_path = STORIES / f"{name}.stressed.txt"
    stressed_refrain = list(refrain)
    if stressed_path.is_file():
        marked = stressed_path.read_text(encoding="utf-8").splitlines()
        for index in range(len(marked) - 1):
            pair = [marked[index], marked[index + 1]]
            if [line.replace("+", "").strip() for line in pair] == refrain:
                stressed_refrain = pair
                break
    for path, fixed in ((plain_path, refrain), (stressed_path, stressed_refrain)):
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        wanted = iter(headings)
        table = correction_map()
        for index, line in enumerate(lines):
            if line.startswith("# "):
                heading = next(wanted, line).replace("+", "")
                if path == stressed_path:
                    heading = hand_mark(heading, table)[0]
                lines[index] = heading
        body: list[int] = []
        numbered = False
        for index in range(len(lines) + 1):
            line = lines[index] if index < len(lines) else "# end"
            if line.startswith("# "):
                spoken = [i for i in body if lines[i].strip()]
                if numbered and len(spoken) >= len(fixed):
                    for offset, text in enumerate(fixed):
                        lines[spoken[-len(fixed) + offset]] = text
                body = []
                numbered = True
            else:
                body.append(index)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- main


def main() -> None:
    ap = argparse.ArgumentParser(description="Write a long Russian bedtime story from a brief.")
    ap.add_argument("name")
    ap.add_argument("--brief", default=None)
    ap.add_argument("--chapters", type=int, default=0, help="override the brief's chapter count")
    ap.add_argument("--minutes", type=int, default=0, help="override the brief's target minutes")
    ap.add_argument("--chapter-words", default=f"{CHAPTER_MIN}:{CHAPTER_MAX}",
                    help="per chapter word window, MIN:MAX")
    ap.add_argument("--dry-run", action="store_true", help="print the prompts, call nothing, write no story")
    ap.add_argument("--redo", type=int, nargs="+", default=[], help="draft these chapters again")
    ap.add_argument("--skip-stress", action="store_true")
    ap.add_argument("--skip-critique", action="store_true")
    ap.add_argument("--rounds", type=int, default=1, help="critic passes over the text")
    ap.add_argument("--check", action="store_true", help="only validate the files on disk")
    ap.add_argument("--endpoint", default=ENDPOINT)
    ap.add_argument("--model", default=MODEL)
    args = ap.parse_args()

    brief_path = Path(args.brief) if args.brief else BRIEFS / f"{args.name}.json"
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    chapters = args.chapters or int(brief.get("chapters", 11))
    minutes = args.minutes or int(brief.get("minutes", 20))
    total_words = round(minutes * 2.6 * 60 / 1.35)
    target = round(total_words / chapters)
    chapter_min, chapter_max = (int(v) for v in args.chapter_words.split(":"))
    minimum = min(chapter_min, target - 5)
    maximum = max(chapter_max, target + 5)
    total_min, total_max = round(total_words * 0.95), round(total_words * 1.03)
    refrain = list(brief["refrain"])
    print(f"{args.name}: {chapters} chapters, about {total_words} words, "
          f"{minimum}-{maximum} words per chapter", flush=True)

    if args.check:
        text = (STORIES / f"{args.name}.txt").read_text(encoding="utf-8")
        problems = story_problems(text, refrain, chapters, brief["mode"], minimum, maximum, total_min, total_max)
        stressed = STORIES / f"{args.name}.stressed.txt"
        if stressed.is_file():
            problems += stress_problems(text, stressed.read_text(encoding="utf-8"))
        for heading, count in chapter_word_counts(text):
            print(f"{count:4d}  {heading}")
        print(f"body words: {body_words(text.splitlines()[1:])}")
        for problem in problems:
            print("PROBLEM " + problem)
        sys.exit(1 if problems else 0)

    log_path = STORIES / f"{args.name}.writer.jsonl"
    records = load_log(log_path)
    redo = set(args.redo)
    drafts = drafted_chapters(records, redo)
    plan = saved_plan(records)

    if args.dry_run:
        prompts: list[tuple[str, int | None, list[dict]]] = [("plan", None, plan_prompt(brief, chapters))]
        for number in range(1, chapters + 1):
            prompts.append(("draft", number,
                            chapter_prompt(brief, plan or {"cast": [], "recurring": [],
                                                           "chapters": [{"title": "...", "beat": "...",
                                                                         "quieter": "...", "cast": []}] * chapters},
                                           number, minimum, maximum, [], [], [])))
        for stage, number, messages in prompts:
            print(f"===== {stage} {number or ''} =====")
            for message in messages:
                print(f"[{message['role']}]\n{message['content']}\n")
        return

    log = Log(log_path)
    try:
        if plan is None:
            raw = ask_model(log, "plan", plan_prompt(brief, chapters), endpoint=args.endpoint, model=args.model)
            plan = parse_json_block(raw)
            if not plan.get("chapters") or len(plan["chapters"]) != chapters:
                raise RuntimeError(f"the plan has {len(plan.get('chapters', []))} chapters, expected {chapters}")
            plan["refrain"] = refrain
            (STORIES / f"{args.name}.plan.json").write_text(
                json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            log.write({"stage": "plan", "ok": True, "plan": plan})
            print(f"plan: {len(plan['cast'])} cast, {len(plan['chapters'])} chapters", flush=True)
        plan_path = STORIES / f"{args.name}.plan.json"
        if not plan_path.is_file():
            plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        for number in range(1, chapters + 1):
            if number in drafts:
                print(f"chapter {number}: resumed from the log", flush=True)
                continue
            facts = [fact for n in sorted(drafts) for fact in drafts[n].get("facts", [])]
            tail = drafts[number - 1]["lines"][-4:] if number - 1 in drafts else []
            problems: list[str] = []
            for attempt in range(1, DRAFT_TRIES + 1):
                messages = chapter_prompt(brief, plan, number, minimum, maximum, facts, tail, problems)
                raw = ask_model(log, "draft", messages, chapter=number,
                                endpoint=args.endpoint, model=args.model)
                data = parse_json_block(raw) or {"text": raw}
                lines = chapter_lines(data, refrain)
                problems = chapter_problems(lines, refrain, minimum, maximum)
                log.write({"stage": "draft", "chapter": number, "attempt": attempt,
                           "event": "check", "ok": not problems, "problems": problems,
                           "words": sum(len(words(line)) for line in lines)})
                if not problems:
                    break
                print(f"chapter {number} attempt {attempt}: {len(problems)} problems", flush=True)
            else:
                raise RuntimeError(f"chapter {number} failed {DRAFT_TRIES} times: {problems}")
            record = {"stage": "draft", "chapter": number, "ok": True, "lines": lines,
                      "title": data.get("title") or plan["chapters"][number - 1]["title"],
                      "facts": [str(f) for f in data.get("facts", []) if str(f).strip()]}
            drafts[number] = record
            log.write(record)
            (STORIES / f"{args.name}.txt").write_text(assemble(brief["title"], plan, drafts), encoding="utf-8")
            print(f"chapter {number}: {sum(len(words(line)) for line in lines)} words", flush=True)

        text = assemble(brief["title"], plan, drafts)
        (STORIES / f"{args.name}.txt").write_text(text, encoding="utf-8")
        problems = story_problems(text, refrain, chapters, brief["mode"], minimum, maximum, total_min, total_max)
        if problems:
            raise RuntimeError("story rules:\n" + "\n".join(problems))
        print(f"draft: {body_words(text.splitlines()[1:])} body words", flush=True)

        if not args.skip_stress:
            fix_stress(args.name)
        if not args.skip_critique:
            headings = [line for line in text.splitlines() if line.startswith("# ")]
            counts = run_critic(args.name, brief["mode"], args.rounds)
            restore_fixed_lines(args.name, headings, refrain)
            print(f"critic: {counts['accepted']} accepted, {counts['rejected']} rejected", flush=True)

        plain = (STORIES / f"{args.name}.txt").read_text(encoding="utf-8")
        problems = story_problems(plain, refrain, chapters, brief["mode"], minimum, maximum, total_min, total_max)
        stressed_path = STORIES / f"{args.name}.stressed.txt"
        if stressed_path.is_file():
            problems += stress_problems(plain, stressed_path.read_text(encoding="utf-8"))
        for heading, count in chapter_word_counts(plain):
            print(f"{count:4d}  {heading}")
        if problems:
            raise RuntimeError("final rules:\n" + "\n".join(problems))
        print("done: every hard rule passes", flush=True)
    finally:
        log.close()


if __name__ == "__main__":
    main()
