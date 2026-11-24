# The Russian voice settings

`config/russian-standard.json` is the machine-readable form. The scripts read that file. The copy in this repository is a template. Fill the reference fields after you record. Do not commit the recording or its hash to a public fork.

## Starting values

| Part | Value |
|---|---|
| Engine | F5-TTS 1.1.22, config `F5TTS_v1_Base` |
| Checkpoint | `Misha24-10/F5-TTS_RUSSIAN`, revision `ea166adeae4c80ec5ee423a671e2bdb83906cf84`, file `F5TTS_v1_Base_v2/model_last_inference.safetensors`. Vocabulary: `F5TTS_v1_Base/vocab.txt`. License: CC BY-NC 4.0. |
| Sampling | 32 steps, guidance 2.0. The seed base is in the config. Each part adds its index. |
| Speed | Start at 0.788. A new reference needs a new speed. `--match-seconds 47.9` picks the speed that gives the audition passage that length. |
| Clip processing | 70 Hz high-pass, 4th order, over the whole recording. Wiener denoise, decision-directed, gain floor -9 dB, with the noise profile taken from the pauses. One gain: RMS -20 dBFS, peak at most -1.5 dBFS. 24 kHz, 16-bit mono WAV. |
| Output | Two-pass loudness normalization to -18 LUFS, true peak -2 dB. AAC 160 kbit/s, 48 kHz mono. Do not denoise, compress or time-stretch the approved voice. |
| Modes | Nighttime keeps the longer pauses. Morning shortens only the default pauses. Optional music is normalized, faded and sidechain-ducked. The narration is not compressed. |

## What the denoise changed

The same passage, the same seeds, the same pauses. Only the reference processing changed. Numbers are from the unnormalised render.

| Render | Reference | Floor (p10) | Speech (p75) | Gap |
|---|---|---:|---:|---:|
| Earlier, noisy memo | 12 dB gap, FFT denoise | -48.0 dBFS | -23.1 dBFS | 24.9 dB |
| High-pass only | cleaner recording | -48.7 dBFS | -17.0 dBFS | 31.7 dB |
| High-pass and Wiener | cleaner recording | -58.5 dBFS | -18.7 dBFS | 39.8 dB |

Floor is the 10th percentile of the 25 ms frame levels. Speech is the 75th percentile. Gap is speech minus floor. These numbers are proxies. Your ears decide.

## Fill the template

1. Record with [RECORDING_GUIDE.md](RECORDING_GUIDE.md).
2. Run `analyze_recording.py` and pick a 7 to 10 second window.
3. Set `reference.source_recording.name`, `sha256`, `sample_rate` and `duration_s`.
4. Set `reference.window_s` to the start and end of the clean line, in seconds.
   Until you set `window_s`, the text critic uses an 8 second example for the reference sentence. The renderer does not use that example. `prepare_reference.py` stops until the window is real.
5. Set `reference.text` to what the speaker said, with a `+` before the stressed vowel.
6. Leave `reference.wav_sha256` empty. `prepare_reference.py` prints the hash of the clip. Paste that hash into the config. The renderer then refuses a clip that does not match.

```sh
uv run --no-project --python 3.11 --with numpy==2.2.5 --with scipy==1.16.3 \
  python narration/prepare_reference.py narration/voice/your-recording.wav
```

Copy `narration/voice/reference-ru-standard.wav` to the render machine, under `$NARRATION_DEST/voice/`. Then render the audition passage and listen.

```sh
export NARRATION_HOST=your-render-machine
narration/deploy.sh
ssh "$NARRATION_HOST"
cd ~/bedtime-audiobooks
f5-env/bin/python f5_russian.py reading/ru-audition-passage.json --out samples/ru-standard-check.m4a
```

## Limits

- A 16 kHz recording has nothing above 8 kHz. The voice sounds dull. A 48 kHz recording is brighter. The process stays the same. You write a new manifest.
- The pace belongs to the reference. A new reference needs a new speed.
- Unmarked words get the model's stress guess. Mark them.
- Whisper cannot judge stress. Only a listener can.
- The checkpoint license is CC BY-NC 4.0. Do not sell the voice.
