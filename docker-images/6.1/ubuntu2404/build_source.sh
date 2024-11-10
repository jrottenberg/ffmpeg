#!/usr/bin/env bash

# Stop execution on any error
# Note: we can override this in the Dockerfile RUN command with an || true.
#       which is useful for debugging
set -e

manifestJsonFile="/tmp/workdir/generated_build_manifest.json"
manifestJsonVersionsFile="/tmp/workdir/generated_build_versions_manifest.json"

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
######################### Callback build functions #########################
build_libopencore-amr() {
    ./configure --prefix="${PREFIX}" --enable-shared
    make
    make install
}

build_libx264() {
    ./configure --prefix="${PREFIX}" --enable-shared --enable-pic --disable-cli
    make
    make install
}

build_libx265() {
    cd build/linux
    sed -i "/-DEXTRA_LIB/ s/$/ -DCMAKE_INSTALL_PREFIX=\${PREFIX}/" multilib.sh
    sed -i "/^cmake/ s/$/ -DENABLE_CLI=OFF/" multilib.sh
    ./multilib.sh
    make -C 8bit install
}

build_libogg() {
    ./configure --prefix="${PREFIX}" --enable-shared
    make
    make install
}

build_libopus() {
    ./configure --prefix="${PREFIX}" --enable-shared
    make
    make install
}

build_libvorbis() {
    ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared
    make
    make install
    # https://gitlab.xiph.org/xiph/vorbis
    # cmake -G YOUR-PROJECT-GENERATOR -DBUILD_SHARED_LIBS=1 -DCMAKE_INSTALL_PREFIX="${PREFIX}" .
    # make
    # make install
}

build_libvpx() {
    local data=$(jq -r '.[] | select(.library_name == "libvpx")' $manifestJsonFile)
    local dir=$(echo "$data" | jq -r '.build_dir')
    local vpx_version=$(jq -r '.["libvpx"]' $manifestJsonVersionsFile)
    if [ -n "$vpx_version" ] && [[ "$vpx_version" != "null" ]]; then
        echo "Building [libvpx-${vpx_version}] in [${dir}]"
    else
        echo "Error: libvpx version is empty or unset"
    fi
    version="v${vpx_version}"
    git -C libvpx pull 2> /dev/null || git clone --branch ${version} --depth 1 https://chromium.googlesource.com/webm/libvpx.git
    cd libvpx
    pwd
    ./configure  --prefix="${PREFIX}" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --enable-pic --enable-shared --as=yasm
    make
    make install
}

build_libwebp() {
    ./configure --prefix="${PREFIX}" --enable-shared && \
    make && \
    make install
}

build_libmp3lame() {
    ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --enable-shared --enable-nasm --disable-frontend && \
    make && \
    make install
}


build_libxvid() {
    # read doc/INSTALL
    cd build/generic
    ./configure --help
    echo "Now guess"
    ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin --enable-shared"
    make
    make install
}

build_libfdk-aac() {
    autoreconf -fiv && \
    ./configure --prefix="${PREFIX}" --enable-shared
    make
    make install
}

build_openjpeg() {
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
    make && \
    make install
}

build_freetype() {
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install
}

build_libvidstab() {
    cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
    make && \
    make install
}

build_fribidi() {
    # Currently broken, need to fix
    # sed -i 's/^SUBDIRS =.*/SUBDIRS=gen.tab charset lib bin/' Makefile.am
    # ./bootstrap --no-config --auto
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared
    make -j1
    make install
}

build_fontconfig() {
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install
}

build_libass() {
    ./autogen.sh && \
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install
}

build_kvazaar() {
    # ./autogen.sh && \
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install
}

# aom is a git clone ( to get source, so not in the loop using the callback function)
build_aom() {
    local data=$(jq -r '.[] | select(.library_name == "aom")' $manifestJsonFile)
    local dir=$(echo "$data" | jq -r '.build_dir')
    local aom_version=$(jq -r '.["aom"]' $manifestJsonVersionsFile)  # Access value with key "aom"
    if [ -n "$aom_version" ] && [[ "$aom_version" != "null" ]]; then
        echo "Building [aom-${aom_version}] in [${dir}]"
    else
        echo "Error: aom version is empty or unset"
    fi
    version="v${aom_version}"
    git clone --branch ${version} --depth 1 https://aomedia.googlesource.com/aom ${dir} && \
    cd ${dir} && \
    mkdir -p ./aom_build && \
    cd ./aom_build && \
    cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 -DENABLE_NASM=on .. && \
    make && \
    make install
}

build_nvidia-codec-headers() {
    local dir=${1}
	# git clone https://github.com/FFmpeg/nv-codec-headers ${dir}
	# git checkout n${NVIDIA_HEADERS_VERSION}
	make PREFIX="${PREFIX}"
	make install PREFIX="${PREFIX}"
}

build_libsvtav1() {
    cd Build && \
    cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DCMAKE_BUILD_TYPE=Release -DBUILD_DEC=OFF -DBUILD_SHARED_LIBS=OFF .. \
    make && \
    make install
}

build_xorg-macros() {
    dir=${1}
    ./configure --srcdir=${dir} --prefix="${PREFIX}" && \
    make && \
    make install
}

build_xproto() {
    dir=${1}
    cp /usr/share/misc/config.guess . && \
    ./configure --srcdir=${dir} --prefix="${PREFIX}" && \
    make && \
    make install
}

build_libxau() {
    dir=${1}
    ./configure --srcdir=${dir} --prefix="${PREFIX}" && \
    make && \
    make install
}

build_libpthread-stubs() {
    ./configure --prefix="${PREFIX}" && \
    make && \
    make install
}

build_libxml2() {
    ./autogen.sh --prefix="${PREFIX}" --with-ftp=no --with-http=no --with-python=no && \
    make && \
    make install
}

build_libbluray() {
    ## libbluray - Requires libxml, freetype, and fontconfig
    ./configure --prefix="${PREFIX}" --disable-examples --disable-bdjava-jar --disable-static --enable-shared && \
    make && \
    make install
}

build_libzmq() {
    ./autogen.sh && \
    ./configure --prefix="${PREFIX}" && \
    make && \
    make install
}

# another special, code clone situation ( actually currently using the tarball build approach )
build_libpng() {
    local dir = "/tmp/png"
    # local libpng_version=$(jq -r '.["libpng"]' $manifestJsonVersionsFile)  # Access value with key "libpng"
    # git clone https://git.code.sf.net/p/libpng/code ${dir} -b v${libpng_version} --depth 1 && \
    ./autogen.sh && \
    ./configure --prefix="${PREFIX}" && \
    make check && \
    make install
}

build_libaribb24() {
    autoreconf -fiv && \
    ./configure CFLAGS="-I${PREFIX}/include -fPIC" --prefix="${PREFIX}" && \
    make && \
    make install
}

build_zimg() {
    ./autogen.sh && \
    ./configure --prefix="${PREFIX}" --enable-shared  && \
    make && \
    make install
}

# Dependancy on libogg
build_libtheora() {
    if [ "$is_ubuntu" = true ]; then
        cp /usr/share/misc/config.guess .
    fi
    ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared --disable-examples
    make
    make install
}

build_libsrt() {
    # requires libssl-dev
    cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
    make && \
    make install
}

build_libvmaf() {
    # https://github.com/Netflix/vmaf/issues/788#issuecomment-756098059
    mkdir ./libvmaf/build
    cd ./libvmaf/build
    meson setup -Denable_tests=false -Denable_docs=false --buildtype=release --default-library=static --prefix "${PREFIX}" .. && \
    # meson setup -Denable_tests=false -Denable_docs=false --buildtype=release --default-library=shared --prefix "${PREFIX}" ..
    ninja
    ninja install
}

build_ffmpeg() {
    # Here is a list of things that we enable in the ffmpeg build: that are not in the
    # track configuration guide: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg
    # --enable-fontconfig
    # --enable-libaribb24
    # --enable-libbluray
    # --enable-libkvazaar
    # --enable-libopencore-amrnb
    # --enable-libopencore-amrwb
    # --enable-libopenjpeg
    # --enable-libsrt
    # --enable-libtheora
    # --enable-libvmaf
    # --enable-libwebp
    # --enable-libxvid
    # --enable-libzimg
    # --enable-libzmq
    # --enable-openssl
    # --enable-postproc
    # --enable-small
    # --enable-version3

    # export PKG_CONFIG_PATH=${PKG_CONFIG_PATH}
    ./configure --disable-debug \
        --disable-doc \
        --disable-ffplay \
        --enable-fontconfig \
        --enable-gpl \
        --enable-libaom \
        --enable-libaribb24 \
        --enable-libass \
        --enable-libbluray \
        --enable-libdav1d \
        --enable-libfdk-aac \
        --enable-libfontconfig \
        --enable-libfreetype \
        --enable-libfribidi \
        --enable-libharfbuzz \
        --enable-libkvazaar \
        --enable-libmp3lame \
        --enable-libopencore-amrnb \
        --enable-libopencore-amrwb \
        --enable-libopenjpeg \
        --enable-libopus \
        --enable-libsrt \
        --enable-libsvtav1 \
        --enable-libtheora \
        --enable-libvidstab \
        --enable-libvmaf \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libwebp \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libxvid \
        --enable-libzimg \
        --enable-libzmq \
        --enable-nonfree \
        --enable-openssl \
        --enable-postproc \
        --enable-shared \
        --enable-small \
        --enable-version3 \
        --extra-cflags="-I${PREFIX}/include -I/usr/include/x86_64-linux-gnu" \
        --extra-ldflags="-L${PREFIX}/lib -L/usr/lib/x86_64-linux-gnu -L/usr/lib" \
        --extra-ldflags=-L/opt/ffmpeg/lib/x86_64-linux-gnu \
        --extra-libs=-ldl \
        --extra-libs=-lm \
        --extra-libs=-lpthread \
        --ld=g++ \
        --prefix="${PREFIX}" && \
    make && \
    make install && \
    make tools/zmqsend && cp tools/zmqsend ${PREFIX}/bin/ && \
    make distclean && \
    hash -r && \
    cd tools && \
    make qt-faststart && cp qt-faststart ${PREFIX}/bin/
}
######################### Helper functions #########################
extract_tarball() {
    local tarball_name=$1
    # grab the extension of the tarball
    local extension="${tarball_name##*.}"
    # tar extraction args: -z, -j, -J, --lzma  Compress archive with gzip/bzip2/xz/lzma
    if [ "$extension" == "gz" ]; then
        tar -zx --strip-components=1 -f ${tarball_name}
    elif [ "$extension" == "bz2" ]; then
        tar -jx --strip-components=1 -f ${tarball_name}
    elif [ "$extension" == "xz" ]; then
        tar -Jx --strip-components=1 -f ${tarball_name}
    else
        echo "Error while extract_tarball, got an unknown extension: $extension"
    fi
}

build_support_libraries() {
    local librariesRaw="$(jq -r '.[] | .library_name' $manifestJsonFile)"
    local libs=( $librariesRaw )
    for i in "${!libs[@]}"; do
        lib_name=${libs[$i]}
        # handle the clone source case's ( there are only two )
        # if [ "$lib_name" == "libsvtav1" ]; then
        #     echo "-------------------- Running callback: build_aom --------------------"
        #     echo "Building 'aom' before we build $lib_name"
        #     build_aom
        # fi
        # ffmpeg is in the lib_name string then the callback name is build_ffmpeg
        callback_lib_name=${lib_name}
        if [[ "$lib_name" == *"ffmpeg"* ]]; then
            # take out the version numbers
            callback_lib_name="ffmpeg"
        fi

        local data=$(jq -r '.[] | select(.library_name == "'${lib_name}'")' $manifestJsonFile)
        build_dir=$(echo "$data" | jq -r '.build_dir')
        tarball_name=$(echo "$data" | jq -r '.tarball_name')
        sha256sum=$(echo "$data" | jq -r '.sha256sum')

        echo "Building $lib_name: from ${build_dir}/$tarball_name"
        cd $build_dir
        extract_tarball $tarball_name
        if [ -n "$sha256sum" ] && [[ "$sha256sum" != "null" ]]; then
            echo "Checking sha256sum for $tarball_name"
            echo $sha256sum | sha256sum --check
        fi
        # make a callback function to build the library
        # if anything fails, we will exit with a non-zero status
        echo "-------------------- Running callback: build_${lib_name} --------------------"
        build_${callback_lib_name} ${build_dir}
        echo "Finished building $lib_name removing build directory [${build_dir}]"
        cd /tmp/workdir
        rm -rf $build_dir
    done
}

build_support_libraries
