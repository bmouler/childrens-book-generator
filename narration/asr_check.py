#!/usr/bin/env python3
"""Check what a recording or a render says: a Whisper transcript, and the word differences from the expected text.

usage: asr_check.py AUDIO [--expected TEXT_OR_PARTS_JSON] [--windows 17.6-25.4,32.2-39.4] [--model small|turbo]

A transcript is a sanity check. It does not prove pronunciation or stress. Whisper reads a vowel that
sounds like another one as the other word (горела as горело). It often adds a phrase such as
"спасибо за просмотр" after the last word. Use the turbo model to settle a doubt: two models that agree
on a word make a misread unlikely.

Run it on the Ubuntu PC in the bedtime env:
  ~/miniforge3/envs/bedtime/bin/python ~/bedtime-audiobooks/asr_check.py OUT.m4a --expected PARTS.json
"""
import argparse
import difflib
import json
import os
import re
from pathlib import Path

import audio_tools as A

MODELS = {"small": "openai/whisper-small", "turbo": "openai/whisper-large-v3-turbo"}


def words(text: str):
    return re.findall("[а-я]+", text.lower().replace("ё", "е"))


def expected_text(path: Path) -> str:
    if path.suffix.lower() == ".json":
        items = json.loads(path.read_text(encoding="utf-8"))
        text = " ".join(i if isinstance(i, str) else i["text"] for i in items)
    else:
        text = path.read_text(encoding="utf-8")
    return text.replace("+", "")


def main():
    ap = argparse.ArgumentParser(description="Whisper transcript and word differences.")
    ap.add_argument("audio")
    ap.add_argument("--expected", default=None, help="text file or parts .json; stress marks are ignored")
    ap.add_argument("--windows", default=None, help="comma list of START-END seconds")
    ap.add_argument("--model", choices=sorted(MODELS), default="small")
    ap.add_argument("--threads", type=int, default=8)
    args = ap.parse_args()

    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    import torch
    from transformers import pipeline
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(1)

    windows = [tuple(float(v) for v in w.split("-")) for w in args.windows.split(",")] if args.windows else [(0.0, None)]
    asr = pipeline("automatic-speech-recognition", model=MODELS[args.model], device=-1)
    heard = []
    for start, end in windows:
        audio, _ = A.decode(args.audio, sr=16000, start=start, duration=None if end is None else end - start)
        text = asr(audio.copy(), return_timestamps=True,
                   generate_kwargs={"language": "russian", "task": "transcribe"})["text"].strip()
        heard.append(text)
        print(json.dumps({"window": [start, end], "model": args.model, "text": text}, ensure_ascii=False))
    if args.expected:
        want, got = words(expected_text(Path(args.expected).expanduser())), words(" ".join(heard))
        ops = difflib.SequenceMatcher(a=want, b=got, autojunk=False).get_opcodes()
        diffs = [{"op": o, "expected": want[a:b], "heard": got[c:d]} for o, a, b, c, d in ops if o != "equal"]
        print(json.dumps({"expected_words": len(want), "heard_words": len(got), "differences": diffs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
