#!/usr/bin/env bash
# Build all docker-images in parallel using tmux with a tiled grid view.
# Each Dockerfile gets its own pane showing live build output.
# Usage: ./build-parallel-tmux.sh [IMAGE_PREFIX]
#   IMAGE_PREFIX defaults to "jrottenberg/ffmpeg"

set -euo pipefail

IMAGE_PREFIX="${1:-jrottenberg/ffmpeg}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="${REPO_ROOT}/logs"
SESSION="ffmpeg-build"

mkdir -p "${LOG_DIR}"

mapfile -t DOCKERFILES < <(find "${REPO_ROOT}/docker-images" -name Dockerfile | sort)

if [[ ${#DOCKERFILES[@]} -eq 0 ]]; then
    echo "No Dockerfiles found under docker-images/" >&2
    exit 1
fi

# Kill any stale session with the same name
tmux kill-session -t "${SESSION}" 2>/dev/null || true

echo "Starting tmux session '${SESSION}' with ${#DOCKERFILES[@]} builds"
echo "Logs → ${LOG_DIR}/"
echo ""

FIRST=true
for dockerfile in "${DOCKERFILES[@]}"; do
    variant_dir="$(dirname "${dockerfile}")"
    variant="$(basename "${variant_dir}")"
    version="$(basename "$(dirname "${variant_dir}")")"
    tag="${IMAGE_PREFIX}:${version}-${variant}"
    logfile="${LOG_DIR}/${version}-${variant}.log"
    pane_title="${version}-${variant}"

    build_cmd="printf '\033]2;%s\033\\' '${pane_title}'; docker build -t '${tag}' --build-arg MAKEFLAGS='-j\$(($(nproc) + 1))' '${variant_dir}' 2>&1 | tee '${logfile}'; echo \"--- done: \$? ---\"; read -r"

    if [[ "${FIRST}" == true ]]; then
        tmux new-session -d -s "${SESSION}" -x "220" -y "50" bash
        tmux send-keys -t "${SESSION}" "${build_cmd}" Enter
        FIRST=false
    else
        tmux split-window -t "${SESSION}" bash
        tmux send-keys -t "${SESSION}" "${build_cmd}" Enter
        tmux select-layout -t "${SESSION}" tiled
    fi

    echo "  Queued: ${tag}"
done

# Final tiled layout
tmux select-layout -t "${SESSION}" tiled

echo ""
echo "All builds launched."
echo ""
echo "Attach:    tmux attach -t ${SESSION}"
echo "Kill all:  tmux kill-session -t ${SESSION}"
