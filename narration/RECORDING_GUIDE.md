# Recording a voice reference

The reference sets the noise and the pace of every book. A clean recording is the cheapest fix for noise.

## Why this matters

A recording with speech only 12 dB above the room noise makes every clone copy the noise. A louder gain makes it worse. A second recording at 24.6 dB raw, and 30.5 dB after a 70 Hz high-pass, cloned clean.

## Record

- Hold the phone one hand-span (about 20 cm) from your mouth, slightly to the side. Keep it still.
- Use a small, soft room, such as a bedroom. Stop fans and air conditioning. Enable airplane mode.
- Use the highest quality setting, 44.1 or 48 kHz, lossless if the app offers it. A 16 kHz recording has nothing above 8 kHz, so the cloned voice has nothing above 8 kHz.
- Do not use effects or earbuds.
- Start the recording and stay silent for 10 seconds. The tools take the noise profile from the pauses.
- Read the script at a calm pace, a little slower than normal talking. Do not whisper. Pause 1.5 seconds between lines. If you make a mistake, pause and read that line again. Read the whole set twice.
- Stay silent for 3 seconds, then stop.
- Send the file as a file, not as a voice message. A voice message compresses the sound.

The scripts are `reading/ru-reference.txt` and `reading/en-reference.txt`. A second pair, `reading/ru-reference-2.txt` and `reading/en-reference-2.txt`, is the same job for another speaker.

Keep the file in `narration/voice/`. That folder is ignored by git. Do not commit it.

## Check it

```sh
uv run --no-project --python 3.11 --with numpy --with scipy python narration/analyze_recording.py REC.wav
```

| Look at | Good |
|---|---|
| Gap after the high-pass | 25 dB or more |
| Clipped samples | 0 |
| Sample rate | 44.1 kHz or more |
| Lead-in silence | 3 s or more |
| Tonal peaks in the pauses | none |
| Band gaps | 25 dB or more from 130 Hz up |

The 0 to 60 Hz band always shows a low gap. It is rumble. The high-pass removes it.

## Choose the clip

1. Pick one calm line, 7 to 10 seconds long, that starts and ends in a pause.
2. Check the words with `asr_check.py REC.wav --windows START-END --model turbo`, and with `--model small`. Use a line only when both models give the script's words.
3. The reference text for F5 is what the speaker said, not what the script says. Add the stress marks.
4. Put the recording hash, the window and the text into `config/russian-standard.json`. Build the clip with `prepare_reference.py`. Render `reading/ru-audition-passage.json`. Listen before you keep the voice.

Only a listener can approve a voice. Whisper cannot judge stress, warmth or noise.
