#!/usr/bin/env bash
# Build all docker-images in parallel using GNU screen.
# Each Dockerfile gets its own named screen window; logs go to logs/<version>-<variant>.log
# Usage: ./build-parallel.sh [IMAGE_PREFIX]
#   IMAGE_PREFIX defaults to "jrottenberg/ffmpeg"

set -euo pipefail

IMAGE_PREFIX="${1:-jrottenberg/ffmpeg}"
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="${REPO_ROOT}/logs"
SESSION="ffmpeg-build"

mkdir -p "${LOG_DIR}"

# Collect all Dockerfiles: docker-images/<version>/<variant>/Dockerfile
mapfile -t DOCKERFILES < <(find "${REPO_ROOT}/docker-images" -name Dockerfile | sort)

if [[ ${#DOCKERFILES[@]} -eq 0 ]]; then
    echo "No Dockerfiles found under docker-images/" >&2
    exit 1
fi

# Kill any stale session with the same name
screen -S "${SESSION}" -X quit 2>/dev/null || true

echo "Starting screen session '${SESSION}' with ${#DOCKERFILES[@]} builds"
echo "Logs → ${LOG_DIR}/"
echo ""

FIRST=true
for dockerfile in "${DOCKERFILES[@]}"; do
    variant_dir="$(dirname "${dockerfile}")"
    variant="$(basename "${variant_dir}")"
    version_dir="$(dirname "${variant_dir}")"
    version="$(basename "${version_dir}")"
    tag="${IMAGE_PREFIX}:${version}-${variant}"
    logfile="${LOG_DIR}/${version}-${variant}.log"
    window_name="${version}-${variant}"

    build_cmd="docker build -t \"${tag}\" --build-arg MAKEFLAGS=\"-j\$(((\$(nproc) + 1)))\" \"${variant_dir}\" 2>&1 | tee \"${logfile}\"; echo \"EXIT \$?\" >> \"${logfile}\""

    if [[ "${FIRST}" == true ]]; then
        # Create the session with the first window
        screen -dmS "${SESSION}" -t "${window_name}" bash -c "${build_cmd}"
        FIRST=false
    else
        # Add subsequent windows to the existing session
        screen -S "${SESSION}" -X screen -t "${window_name}" bash -c "${build_cmd}"
    fi

    echo "  Queued: ${tag}  (log: logs/${version}-${variant}.log)"
done

echo ""
echo "All builds launched."
echo ""
echo "Attach to the session:   screen -r ${SESSION}"
echo "List windows:            screen -S ${SESSION} -Q windows"
echo "Follow a log:            tail -f logs/<version>-<variant>.log"
echo "Kill all:                screen -S ${SESSION} -X quit"
