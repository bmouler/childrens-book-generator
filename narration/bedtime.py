#!/usr/bin/env python3
"""Turn an epub or text book into one m4b audiobook with a cloned voice.

Runs on the render machine. The example env is Miniforge "bedtime":
  ~/miniforge3/envs/bedtime/bin/python bedtime.py BOOK.epub|BOOK.txt [options]
GPU run, optional. Set GPU_HOLD_SERVICE if a user service must release the GPU:
  ~/bedtime-audiobooks/gpu-run.sh BOOK.epub [options]

Voice: a 10-60 s clean recording at ~/bedtime-audiobooks/voice/reference.wav.
Without that file the model uses its built-in default voice.

Resume: chunk audio is cached per chapter under a key of text + voice + settings,
so a rerun with the same settings skips finished work and a settings change
regenerates cleanly.
"""
import argparse
import hashlib
import html
import html.parser
import json
import os
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path
import shutil

os.environ.setdefault("TQDM_DISABLE", "1")

HOME = Path.home()
BASE = HOME / "bedtime-audiobooks"
VOICE = BASE / "voice" / "reference.wav"

def _tool(name: str) -> str:
    pinned = HOME / "miniforge3/envs/bedtime/bin" / name
    if pinned.is_file():
        return str(pinned)
    return shutil.which(name) or str(pinned)


FFMPEG = _tool("ffmpeg")
FFPROBE = _tool("ffprobe")
RUBBERBAND = _tool("rubberband")
CHUNK_CHARS = 300
MIN_CHUNK = 80
MIN_CHAPTER = 600      # shorter parts are title pages or table-of-contents lines
SHORT_PARAGRAPH = 40   # merged into the next paragraph (one-word dialogue lines)
PAUSE_SENTENCE = 0.35  # seconds of silence after a chunk inside a paragraph
PAUSE_PARAGRAPH = 0.8  # after the last chunk of a paragraph
PAUSE_TITLE = 1.0      # after the spoken chapter title


class _Text(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag in ("p", "div", "br", "h1", "h2", "h3", "li"):
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in ("p", "h1", "h2", "h3"):
            self.parts.append("\n\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        self.parts.append(data)


def epub_chapters(path: Path):
    """Return [(title, text)] in spine order from an epub."""
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        docs = sorted(n for n in names if n.endswith((".xhtml", ".html", ".htm")))
        opf = next((n for n in names if n.endswith(".opf")), None)
        if opf:
            opf_text = zf.read(opf).decode("utf-8", "ignore")
            spine = re.findall(r'idref="([^"]+)"', opf_text)
            manifest = dict(
                re.findall(r'<item[^>]*?id="([^"]+)"[^>]*?href="([^"]+)"', opf_text)
            )
            ordered = []
            for sid in spine:
                if sid in manifest:
                    cand = str(Path(opf).parent / manifest[sid])
                    ordered.append(cand if cand in names else manifest[sid])
            docs = [d for d in ordered if d in names] or docs
        chapters = []
        for name in docs:
            p = _Text()
            p.feed(zf.read(name).decode("utf-8", "ignore"))
            text = re.sub(r"[ \t]+", " ", "".join(p.parts))
            text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
            if len(text) < 200:  # cover pages, toc filler
                continue
            chapters.append((p.title or Path(name).stem, text))
    return chapters


def strip_gutenberg_boilerplate(text: str) -> str:
    start = re.search(
        r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", text, re.I | re.S
    )
    end = re.search(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", text, re.I)
    if start:
        text = text[start.end():]
    if end:
        text = text[:end.start()]
    return text.strip("\r\n")  # keep the indentation of a leading heading


def txt_chapters(text: str):
    """Split on 'Chapter N' headings or indented ALL-CAPS tale titles."""
    text = "\n" + strip_gutenberg_boilerplate(text)  # a heading may be line one
    parts = re.split(
        r"\n(?=(?:chapter|part|prologue|epilogue)\s+[\dIVXLC]+)"
        r"|\n(?=\s{4,}[A-Z][A-Z \u2019',!.-]{3,60}\s*$)",
        text,
        flags=re.M,
    )
    if len(parts) > 1:
        out = []
        for part in parts:
            part = part.strip()
            if len(part) < MIN_CHAPTER:  # title page, table-of-contents lines
                continue
            head, _, body = part.partition("\n")
            head = re.sub(r"\s+", " ", head).strip(" *_#-")[:80]
            out.append((head, body.strip()))
        if out:
            return out
    blocks, buf = [], []
    for block in re.split(r"\n\s*\n", text):
        buf.append(block)
        if sum(len(b) for b in buf) > 1500:
            blocks.append("\n\n".join(buf))
            buf = []
    if buf:
        blocks.append("\n\n".join(buf))
    return [(f"Part {i + 1}", b.strip()) for i, b in enumerate(blocks) if b.strip()]


def paragraphs(raw: str):
    text = re.sub(r"\[illustration.*?\]", " ", raw, flags=re.I | re.S)
    text = re.sub(r"[*_#]{1,3}", " ", text)
    out = []
    for p in re.split(r"\n\s*\n", text):
        p = html.unescape(re.sub(r"\s+", " ", p)).strip()
        if p:
            out.append(p)
    return out


def sentence_chunks(text: str, limit=CHUNK_CHARS, minimum=MIN_CHUNK):
    sentences = re.split(r"(?<=[.!?;])\s+(?=[\"'A-Z\u201c])", text)
    chunks, buf = [], ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(buf) + len(s) + 1 <= limit:
            buf = f"{buf} {s}".strip()
        else:
            if buf:
                chunks.append(buf)
            while len(s) > limit:  # monster sentence: hard split at commas
                cut = s.rfind(", ", 0, limit)
                cut = cut if cut > minimum else limit
                chunks.append(s[:cut].strip())
                s = s[cut:].lstrip(", ")
            buf = s
    if buf:
        chunks.append(buf)
    return [c for c in chunks if len(c) >= 3]


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def plan_chunks(title: str, raw: str):
    """Return [(text, pause_after_seconds)] for one chapter."""
    paras = paragraphs(raw)
    announce = title and len(title) <= 60 and not re.fullmatch(r"Part \d+", title)
    if announce and paras and _norm(paras[0]) == _norm(title):
        paras = paras[1:]  # heading already in the body: say it once
    items = []
    if announce:
        spoken = title.title() if title.isupper() else title
        items.append((spoken.rstrip(".!?") + ".", PAUSE_TITLE))
    carry = ""
    for p in paras:
        if carry:
            p = f"{carry} {p}"
            carry = ""
        if len(p) < SHORT_PARAGRAPH:
            carry = p
            continue
        chunks = sentence_chunks(p)
        for i, c in enumerate(chunks):
            items.append((c, PAUSE_PARAGRAPH if i == len(chunks) - 1 else PAUSE_SENTENCE))
    if carry:
        items.append((carry, PAUSE_PARAGRAPH))
    return items


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def media_seconds(path: Path) -> float:
    out = run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
               "-of", "json", str(path)]).stdout
    return float(json.loads(out)["format"]["duration"])


def chapter_metadata(book: str, starts: list[tuple[str, float]], total_s: float) -> str:
    """ffmpeg FFMETADATA1 with real chapter ends. A chapter ends where the next one starts and the last one
    ends with the book. The writer used to end every chapter one second after its start, so a player that
    reads the end time showed a one-second chapter. ffmpeg wants = ; # \\ and a newline escaped in a title."""
    def esc(text: str) -> str:
        return re.sub(r"([=;#\\])", r"\\\1", text).replace("\n", "\\\n")

    lines = [";FFMETADATA1", f"title={esc(book)}"]
    for index, (title, start) in enumerate(starts):
        end = starts[index + 1][1] if index + 1 < len(starts) else total_s
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}", f"END={int(end * 1000)}",
                  f"title={esc(title)}"]
    return "\n".join(lines)


def stretched(wav: Path, speed: float) -> Path:
    """Slow a chunk with Rubber Band R3 (formant-safe); cached next to the chunk."""
    if speed == 1.0:
        return wav
    out = wav.with_name(f"{wav.stem}-s{speed}.wav")
    if not out.exists():
        run([RUBBERBAND, "-3", "-q", "-t", f"{1 / speed:.4f}", str(wav), str(out)])
    return out


def main():
    ap = argparse.ArgumentParser(
        description="epub/txt to m4b audiobook with a cloned voice"
    )
    ap.add_argument("book", help="epub or txt file")
    ap.add_argument("--out", default=str(BASE / "books"), help="output directory")
    ap.add_argument("--voice", default=str(VOICE), help="reference wav for cloning")
    ap.add_argument("--exaggeration", type=float, default=0.3,
                    help="0.3 calm narrator (slower) .. 0.7 dramatic character voices (faster)")
    ap.add_argument("--cfg", type=float, default=0.5, help="classifier-free guidance weight")
    ap.add_argument("--speed", type=float, default=0.85,
                    help="tempo multiplier after synthesis (0.85 preferred English pace, 1.0 as generated)")
    ap.add_argument("--chapters", default="", help="range like 1-3 or 2 (1-based)")
    ap.add_argument("--device", default="cpu", help="cpu (default) or cuda (see gpu-run.sh)")
    args = ap.parse_args()

    book = Path(args.book).expanduser()
    if not book.exists():
        sys.exit(f"no such file: {book}")
    work = Path(args.out).expanduser() / book.stem
    work.mkdir(parents=True, exist_ok=True)

    if book.suffix.lower() == ".epub":
        chapters = epub_chapters(book)
    else:
        chapters = txt_chapters(book.read_text(encoding="utf-8", errors="ignore"))
    if not chapters:
        sys.exit("no readable chapters found")
    if args.chapters:
        if "-" in args.chapters:
            a, b = args.chapters.split("-")
            sel = range(int(a) - 1, int(b))
        else:
            sel = [int(args.chapters) - 1]
        chapters = [chapters[i] for i in sel if 0 <= i < len(chapters)]

    voice = Path(args.voice).expanduser()
    use_voice = voice if voice.exists() else None
    print(f"book: {book.name} | chapters: {len(chapters)} | voice: {use_voice or 'BUILT-IN DEFAULT'}"
          f" | speed {args.speed} | exaggeration {args.exaggeration} | {args.device}")
    if not use_voice:
        print("tip: record 10-60 s and save as " + str(VOICE) + " to clone your voice")
    voice_sig = f"{voice.stat().st_size}-{voice.stat().st_mtime_ns}" if use_voice else "default"
    setting_sig = f"{voice_sig}|{args.exaggeration}|{args.cfg}"

    import torch
    if args.device == "cpu":
        torch.set_num_threads(min(32, os.cpu_count() or 8))
    from chatterbox.tts import ChatterboxTTS
    import torchaudio
    t0 = time.time()
    model = ChatterboxTTS.from_pretrained(device=args.device)
    if use_voice:  # embed the reference once instead of once per chunk
        model.prepare_conditionals(str(use_voice), exaggeration=args.exaggeration)
    print(f"model loaded in {time.time() - t0:.0f} s")

    def synth(text: str):
        wav = model.generate(text, exaggeration=args.exaggeration, cfg_weight=args.cfg)
        for attempt in range(2):
            secs = wav.shape[-1] / model.sr
            if 0.3 <= secs <= len(text) / 6 + 3:  # else: babble loop or empty, retry
                break
            print(f"    retry {attempt + 1}: {secs:.1f} s for {len(text)} chars", flush=True)
            wav = model.generate(text, exaggeration=args.exaggeration, cfg_weight=args.cfg)
        return wav

    chapter_files = []
    t_book = time.time()
    for ci, (title, raw) in enumerate(chapters, 1):
        cdir = work / f"{ci:03d}"
        cdir.mkdir(exist_ok=True)
        items = plan_chunks(title, raw)
        print(f"[{ci}/{len(chapters)}] {title[:60]} | {len(items)} chunks", flush=True)
        segs = []
        for n, (text, pause) in enumerate(items):
            key = hashlib.sha1(f"{text}|{setting_sig}".encode()).hexdigest()[:10]
            w = cdir / f"{n:04d}-{key}.wav"
            if not w.exists() or w.stat().st_size < 2000:  # tiny file = failed, redo
                torchaudio.save(str(w), synth(text), model.sr)
            segs.append((stretched(w, args.speed), pause))
        inputs, filt = [], ""
        for i, (w, pause) in enumerate(segs):
            inputs += ["-i", str(w)]
            filt += (
                f"[{i}:a]silenceremove=start_periods=1:start_threshold=-45dB,"
                f"areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
                f"apad=pad_dur={pause}[a{i}];"
            )
        n = len(segs)
        mix = "".join(f"[a{i}]" for i in range(n))
        chapter_wav = cdir / "chapter.wav"
        run([FFMPEG, "-y", "-v", "error"] + inputs +
            ["-filter_complex", filt + f"{mix}concat=n={n}:v=0:a=1,apad=pad_dur=0.6[cat]",
             "-map", "[cat]", str(chapter_wav)])
        aac = cdir / "chapter.m4a"
        run([FFMPEG, "-y", "-v", "error", "-i", str(chapter_wav),
             "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100",
             "-c:a", "aac", "-b:a", "128k", str(aac)])
        chapter_files.append((title, aac))
        done = sum(media_seconds(a) for _, a in chapter_files)
        wall = time.time() - t_book
        print(f"    chapter audio: {media_seconds(aac):.0f} s | book total: {done:.0f} s"
              f" | wall {wall:.0f} s", flush=True)

    starts, t = [], 0.0
    for title, aac in chapter_files:
        starts.append((title, t))
        t += media_seconds(aac)
    concat = work / "list.txt"
    concat.write_text("".join(f"file '{aac}'\n" for _, aac in chapter_files))
    meta = work / "chapters.txt"
    meta.write_text(chapter_metadata(book.stem, starts, t))
    out_m4b = Path(args.out).expanduser() / f"{book.stem}.m4b"
    run([FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-i", str(meta), "-map_metadata", "1", "-map", "0:a", "-c", "copy",
         str(out_m4b)])
    print(f"DONE {out_m4b} | {t / 60:.1f} min of audio")


if __name__ == "__main__":
    main()
