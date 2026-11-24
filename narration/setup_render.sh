#!/usr/bin/env bash
# Create the narration environments on the render machine.
# Run this script on that machine. It does not stop a service. It does not set a host.
#
# usage: narration/setup_render.sh [--dest DIR] [--with-model] [--dry-run]
set -euo pipefail

DEST=${NARRATION_DEST:-$HOME/bedtime-audiobooks}
WITH_MODEL=0
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --dest)
      DEST=$2
      shift 2
      ;;
    --with-model)
      WITH_MODEL=1
      shift
      ;;
    --dry-run)
      DRY=1
      shift
      ;;
    -h|--help)
      echo "usage: setup_render.sh [--dest DIR] [--with-model] [--dry-run]"
      exit 0
      ;;
    *)
      echo "unknown argument: $1"
      exit 2
      ;;
  esac
done

run() {
  if [ "$DRY" = 1 ]; then
    printf 'dry-run:'
    printf ' %q' "$@"
    printf '\n'
    return 0
  fi
  "$@"
}

if [ "$DRY" = 0 ] && ! command -v python3.11 >/dev/null 2>&1; then
  echo "Python 3.11 is not on PATH. Install it, then run this script again."
  exit 1
fi

echo "Destination: $DEST"
run mkdir -p "$DEST"

if [ ! -x "$DEST/bedtime/bin/python" ]; then
  run python3.11 -m venv "$DEST/bedtime"
fi
run "$DEST/bedtime/bin/python" -m pip install -U pip
run "$DEST/bedtime/bin/python" -m pip install \
  "setuptools<81" "chatterbox-tts==0.1.7" "torch==2.6.0" "torchaudio==2.6.0" "transformers==4.46.3"

if [ ! -x "$DEST/f5-env/bin/python" ]; then
  run "$DEST/bedtime/bin/python" -m venv --system-site-packages "$DEST/f5-env"
fi
run "$DEST/f5-env/bin/python" -m pip install \
  "f5-tts==1.1.22" "torch==2.6.0" "torchaudio==2.6.0" "torchcodec==0.2.1" \
  "transformers==4.46.3" "setuptools<81" "pyarrow==21.0.0"

if [ ! -x "$DEST/ruaccent-env/bin/python" ]; then
  run python3.11 -m venv "$DEST/ruaccent-env"
fi
run "$DEST/ruaccent-env/bin/python" -m pip install "huggingface_hub==0.25.2" ruaccent

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is not on PATH."
  echo "On Debian, run: sudo apt-get install ffmpeg"
  echo "On macOS, run: brew install ffmpeg"
fi
if ! command -v rubberband >/dev/null 2>&1; then
  echo "rubberband is not on PATH."
  echo "On Debian, run: sudo apt-get install rubberband-cli"
  echo "On macOS, run: brew install rubberband"
fi

MODEL_CMD=("$DEST/f5-env/bin/huggingface-cli" download Misha24-10/F5-TTS_RUSSIAN --revision ea166adeae4c80ec5ee423a671e2bdb83906cf84)
if [ "$WITH_MODEL" = 1 ]; then
  echo "The Russian speech weights are CC BY-NC 4.0. Do not sell output that depends on them."
  run "${MODEL_CMD[@]}"
else
  echo "The Russian speech weights are not installed. They are CC BY-NC 4.0."
  echo "Download them with this command:"
  printf ' '
  printf ' %q' "${MODEL_CMD[@]}"
  printf '\n'
fi

if [ "$DRY" = 0 ]; then
  cat > "$DEST/env.sh" <<EOF
export NARRATION_DEST=$(printf '%q' "$DEST")
export NARRATION_PYTHON=$(printf '%q' "$DEST/bedtime/bin/python")
export PATH=$(printf '%q' "$DEST/bedtime/bin"):\$PATH
EOF
  echo "Wrote $DEST/env.sh"
  echo "On this machine, run: source $DEST/env.sh"
fi
