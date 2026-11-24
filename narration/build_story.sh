#!/usr/bin/env bash
# Build one Russian story on the render machine and pull the audio back.
# One command per story. The build reads the mode from stories/modes.json and refuses a
# story whose words do not match its mode.
#
# usage: narration/build_story.sh STORY [--rounds N] [--skip-critique] [--dry-run]
#        narration/build_story.sh STORY [--workers 1|2] [--device auto|cuda|cpu]
#        narration/build_story.sh STORY [--min-part-words N] [--chapters A-B]
#
# Set NARRATION_HOST to the SSH name of the render machine before you run this.
# --chapters builds only that chapter range and does not replace the finished story.
set -euo pipefail
HOST=${NARRATION_HOST:?Set NARRATION_HOST to the SSH name of the render machine}
DEST=${NARRATION_DEST:-bedtime-audiobooks}
cd "$(dirname "$0")"

story=${1:?usage: build_story.sh STORY [--rounds N]}
shift
build_args=("$@")

[ -f "stories/$story.stressed.txt" ] || { echo "no story: stories/$story.stressed.txt"; exit 2; }

./deploy.sh
mkdir -p builds
rc=0
ssh -n -o BatchMode=yes "$HOST" \
  "cd '$DEST' && PYTHONPATH=. ~/miniforge3/envs/bedtime/bin/python story_build.py '$story' ${build_args[*]:-}" || rc=$?

for f in "stories/$story.stressed.txt" "stories/$story.txt" "stories/$story.critique.json" "stories/$story.critique.jsonl"; do
  scp -q -o BatchMode=yes "$HOST:$DEST/$f" "$f" </dev/null 2>/dev/null || true
done
scp -q -o BatchMode=yes "$HOST:$DEST/books-ru/$story/$story.build.json" "builds/$story.build.json" </dev/null 2>/dev/null || true
[ "$rc" -eq 0 ] || { echo "build failed, code $rc; text and logs pulled, audio not replaced"; exit "$rc"; }

subset=""
prev=""
for arg in ${build_args[*]:-}; do
  [ "$prev" = "--chapters" ] && subset=$arg
  prev=$arg
done
name=$story
[ -n "$subset" ] && name="$story.chapters-$subset"
out="$HOME/Downloads/Russian-Story-$name.m4a"
scp -q -o BatchMode=yes "$HOST:$DEST/books-ru/$name.m4a" "$out" </dev/null
echo "built: $out"
head -1 "stories/$story.stressed.txt" | sed 's/^/title: /'
if [ -n "$subset" ]; then
  echo "chapters $subset only: books-ru/$story.m4a is unchanged"
fi
