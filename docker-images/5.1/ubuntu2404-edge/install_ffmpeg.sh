#!/bin/bash

continue_on_build_failure=false

# Check if the argument is provided and set the flag accordingly
if [[ "$#" -eq 1 && "$1" == "--continue-on-build-failure" ]]; then
    continue_on_build_failure=true
fi

install_ffmpeg() {
    ## cleanup
    # This is used for both the source and packages version ( be robust about looking for libs to copy )
    if [[ "$continue_on_build_failure" == true && ! -f "${PREFIX}/bin/ffmpeg" ]]; then
        echo "WARNING: ffmpeg not found in ${PREFIX}/bin"
        return 0
    fi

    if [ ! -f ${PREFIX}/bin/ffmpeg ]; then
        echo "ERROR: ffmpeg not found in ${PREFIX}/bin"
        exit 1
    fi
    # Check if ffmpeg library is linked to x86_64-linux-gnu and copy it to /usr/local/lib
    if ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | grep -q . ; then
        ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/
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
    LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf
    cp -rp ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include

    # Create pkgconfig directory and copy and modify pkgconfig files
    mkdir -p /usr/local/lib/pkgconfig
    for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc ${PREFIX}/lib/pkgconfig/kvazaar.pc ${PREFIX}/lib/pkgconfig/libsw*.pc; do
        if [[ -f "$pc" ]]; then
            sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"
        else
            echo "Warning: File '$pc' not found."
        fi
    done
}

install_ffmpeg
