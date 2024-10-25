#!/bin/bash

# Stop execution on any error
# Note: we can override this in the Dockerfile RUN command with an || true.
#       which is useful for debugging
set -e
strip_libs=false

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --strip)
      strip_libs=true
      shift 1
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

OS_NAME=$(uname -s)
is_ubuntu=false
is_alpine=false
if [[ "$OS_NAME" == "Linux" ]]; then
    if grep -q "Ubuntu" /etc/os-release; then
        is_ubuntu=true
    elif grep -q "Alpine Linux" /etc/alpine-release; then
        is_alpine=true
    fi
fi

install_ffmpeg() {
    ## cleanup
    # This is used for both the source and packages version ( be robust about looking for libs to copy )
    if [ ! -f ${PREFIX}/bin/ffmpeg ]; then
        echo "ERROR: ffmpeg not found in ${PREFIX}/bin"
        exit 1
    fi
    # Check if ffmpeg library is linked to x86_64-linux-gnu and copy it to /usr/local/lib
    if ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | grep -q . ; then
        ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/
    fi
    # some nvidia libs are in the cuda targets directory
    if [[ -d /usr/local/cuda/targets/x86_64-linux/lib/ ]]; then
        cp -p /usr/local/cuda/targets/x86_64-linux/lib/libnpp* /usr/local/lib
    fi

    # Check if ffmpeg library is linked to opt/ffmpeg and copy it to /usr/local/lib
    if ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | grep -q . ; then
        ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/
    fi

    # Create symbolic links for shared libraries in /usr/local/lib
    for lib in /usr/local/lib/*.so.*; do
        ln -sf "${lib##*/}" "${lib%%.so.*}".so
    done

    # Copy ffmpeg binaries and share directory to /usr/local
    cp -r ${PREFIX}/bin/* /usr/local/bin/
    cp -r ${PREFIX}/share/ffmpeg /usr/local/share/

    # Build configuration and copy include directories
    LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf && \
    cp -rp ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include

    # Create pkgconfig directory and copy and modify pkgconfig files
    mkdir -p /usr/local/lib/pkgconfig
    for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc ${PREFIX}/lib/pkgconfig/kvazaar.pc ${PREFIX}/lib/pkgconfig/libsw*.pc ${PREFIX}/lib/x86_64-linux-gnu/pkgconfig/libvmaf*; do
        if [[ -f "$pc" ]]; then
            # sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"
            sed "s:${PREFIX}:/usr/local:g; s:/lib64:/lib:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"; \
        else
            echo "Warning: File '$pc' not found."
        fi
    done

    # Strip libraries if requested
    if $strip_libs; then
        for lib in /usr/local/lib/*.so.*; do
            strip --strip-all "$lib"
        done
    fi
    if $is_alpine && $strip_libs; then
        for lib in /usr/lib/*.so.*; do
            # some of the support libs in the alpine build are are here
            strip --strip-all "$lib"
        done
    fi
}

install_ffmpeg
