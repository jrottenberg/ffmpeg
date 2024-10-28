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
    elif [[ -f /etc/alpine-release ]]; then
        is_alpine=true
    fi
fi

install_ffmpeg() {
    echo "Installing ffmpeg"
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

    if [ ! -d /usr/local/include ]; then
        mkdir -p /usr/local/include
    fi

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
}

fakeroot_install_with_striped_libs() {
    echo "Installing ffmpeg with fakeroot and striped libs"
    mkdir -p /tmp/fakeroot/lib
    ldd ${PREFIX}/bin/ffmpeg | cut -d ' ' -f 3 | strings | xargs -I R cp R /tmp/fakeroot/lib/
    for lib in /tmp/fakeroot/lib/*; do strip --strip-all $lib; done
    cp -r ${PREFIX}/bin /tmp/fakeroot/bin/
    cp -r ${PREFIX}/share/ffmpeg /tmp/fakeroot/share/
    LD_LIBRARY_PATH=/tmp/fakeroot/lib /tmp/fakeroot/bin/ffmpeg -buildconf
}

fakeroot_install() {
    echo "Using fakeroot to install ffmpeg"
    mkdir -p /tmp/fakeroot/lib
    ldd ${PREFIX}/bin/ffmpeg | cut -d ' ' -f 3 | strings | xargs -I R cp R /tmp/fakeroot/lib/
    cp -r ${PREFIX}/bin /tmp/fakeroot/bin/
    cp -r ${PREFIX}/share/ffmpeg /tmp/fakeroot/share/
    LD_LIBRARY_PATH=/tmp/fakeroot/lib /tmp/fakeroot/bin/ffmpeg -buildconf
}

# if strip_libs is true then call the install_with_striped_libs function
# else if is_alpine is true then call the fakeroot_install function
if $strip_libs; then
    fakeroot_install_with_striped_libs
elif $is_alpine; then
    fakeroot_install
else
    install_ffmpeg
fi
