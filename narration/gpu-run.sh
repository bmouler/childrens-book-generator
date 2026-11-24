#!/usr/bin/env bash
# Run one narration job on the render machine.
# Usage: gpu-run.sh BOOK.epub [bedtime.py options]
#        gpu-run.sh --exec COMMAND [args...]
# Set GPU_HOLD_SERVICE to a systemd user unit that holds the GPU. The script stops
# that unit for the job and starts it again on exit, including failure and Ctrl-C.
# Leave it unset and the script does not stop any service.
set -uo pipefail
PY=${NARRATION_PYTHON:-$HOME/miniforge3/envs/bedtime/bin/python}
RUNTIME=${NARRATION_DEST:-$HOME/bedtime-audiobooks}
HOLD=${GPU_HOLD_SERVICE:-}

# Optional. Use matching user-space CUDA libraries while the kernel module and
# libcuda.so.1 disagree. A reboot, or a pinned driver package, is the real fix.
compat=$RUNTIME/nvidia-compat/lib
kernel=$(cat /sys/module/nvidia/version 2>/dev/null || true)
installed=$(readlink -f /usr/lib/x86_64-linux-gnu/libcuda.so.1 2>/dev/null | sed -n 's/.*libcuda\.so\.//p')
if [ -n "$kernel" ] && [ -n "$installed" ] && [ "$kernel" != "$installed" ] && [ -e "$compat/libcuda.so.$kernel" ]; then
  export LD_LIBRARY_PATH="$compat${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  echo "gpu-run: nvidia-compat $kernel active (system libcuda is $installed)"
fi

restore() {
  [ -n "$HOLD" ] || return 0
  systemctl --user start "$HOLD" && echo "$HOLD restarted"
}
borrow() {
  [ -n "$HOLD" ] || return 0
  trap restore EXIT
  systemctl --user stop "$HOLD"
  for _ in $(seq 1 30); do
    used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null || echo 0)
    [ "$used" -lt 3000 ] && break
    sleep 1
  done
}

if [ "${1:-}" = "--exec" ]; then
  shift
  if ! "$PY" -c 'import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)' 2>/dev/null; then
    echo "gpu-run: CUDA is unusable, so the command runs on the CPU"
    exec "$@"
  fi
  borrow
  export NARRATION_GPU_WINDOW=1
  "$@"
  exit $?
fi

borrow
TQDM_DISABLE=1 "$PY" "$RUNTIME/bedtime.py" "$@" --device cuda
