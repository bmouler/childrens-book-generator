#!/usr/bin/env bash
# Copy the narration code to the render machine and check every hash after the copy.
# Voice files, books, models and the virtualenvs never move.
# usage: NARRATION_HOST=render-machine narration/deploy.sh
#        NARRATION_DEST=other-folder narration/deploy.sh
set -euo pipefail
HOST=${NARRATION_HOST:?Set NARRATION_HOST to the SSH name of the render machine}
DEST=${NARRATION_DEST:-bedtime-audiobooks}
cd "$(dirname "$0")"
CODE=(audio_tools.py background_music.py make_music.py bedtime.py gpu-run.sh f5_russian.py russian_quality_loop.py story_modes.py story_values.py story_critique_loop.py story_build.py measure_seams.py add_stress.py asr_check.py prepare_reference.py analyze_recording.py README.md)
DATA=(config/russian-standard.json config/russian-stress-corrections.json config/values.json config/content-lint.json reading/ru-audition-passage.json)
STORY_TEXT=(stories/modes.json stories/*.txt)

ssh -o BatchMode=yes "$HOST" "mkdir -p '$DEST/config' '$DEST/reading' '$DEST/stories'"
scp -q "${CODE[@]}" "$HOST:$DEST/"
scp -q config/russian-standard.json config/russian-stress-corrections.json config/values.json config/content-lint.json "$HOST:$DEST/config/"
scp -q reading/ru-audition-passage.json "$HOST:$DEST/reading/"
scp -q "${STORY_TEXT[@]}" "$HOST:$DEST/stories/"
ssh -o BatchMode=yes "$HOST" "chmod 755 '$DEST/bedtime.py' '$DEST/gpu-run.sh' '$DEST/f5_russian.py' '$DEST/russian_quality_loop.py' '$DEST/story_critique_loop.py' '$DEST/story_build.py' '$DEST/measure_seams.py' '$DEST/make_music.py' '$DEST/asr_check.py' '$DEST/add_stress.py'"

bad=0
for f in "${CODE[@]}" "${DATA[@]}" "${STORY_TEXT[@]}"; do
  want=$(shasum -a 256 "$f" | cut -d' ' -f1)
  got=$(ssh -o BatchMode=yes "$HOST" "sha256sum '$DEST/$f'" | cut -d' ' -f1)
  [ "$want" = "$got" ] || { echo "MISMATCH $f"; bad=1; }
done
[ "$bad" -eq 0 ] && echo "deployed to $HOST:$DEST ($(( ${#CODE[@]} + ${#DATA[@]} + ${#STORY_TEXT[@]} )) files, hashes match)"
exit "$bad"
