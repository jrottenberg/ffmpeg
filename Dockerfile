# ffmpeg - http://ffmpeg.org/download.html
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#
FROM        ubuntu:16.04
MAINTAINER  Julien Rottenberg <julien@rottenberg.info>


CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]
WORKDIR     /tmp/workdir


ENV         FFMPEG_VERSION=3.1.2 \
            FAAC_VERSION=1.28    \
            FDKAAC_VERSION=0.1.4 \
            LAME_VERSION=3.99.5  \
            OGG_VERSION=1.3.2    \
            OPUS_VERSION=1.1.1   \
            THEORA_VERSION=1.1.1 \
            YASM_VERSION=1.3.0   \
            VORBIS_VERSION=1.3.5 \
            VPX_VERSION=1.5.0    \
            XVID_VERSION=1.3.4   \
            X265_VERSION=1.9     \
            SRC=/usr/local

RUN     export MAKEFLAGS="-j$[$(nproc) + 1]" && \
        apt-get -yqq update && \
        apt-get install -yq --no-install-recommends \
        autoconf \
        automake \
        bzip2 \
        ca-certificates \
        cmake \
        curl \
        g++ \
        gcc \
        git \
        libssl-dev \
        libtool \
        make \
        nasm \
        perl \
        pkg-config \
        python \
        tar \
        xmlto \
        zlib1g-dev && \

# yasm
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -sL https://github.com/yasm/yasm/archive/v${YASM_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd ${DIR}/yasm-${YASM_VERSION} && \
        ./autogen.sh && \
        ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --docdir=${DIR} -mandir=${DIR}&& \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR} && \

# x264  TODO : pin version, at least we use the stable branch
        DIR=$(mktemp -d) && cd ${DIR} && \
        git clone -b stable  --single-branch --depth 1 git://git.videolan.org/x264 && \
        cd x264 && \
        ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --enable-static && \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR} && \

# x265
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s https://bitbucket.org/multicoreware/x265/downloads/x265_{X265_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd x265_${X265_VERSION}/source && \
        cmake -G "Unix Makefiles" . && \
        cmake . && \
        make && \
        ../build/linux/multilib.sh && \
        make install && \
        build/linux/multilib.sh && \
        rm -rf ${DIR} && \
# libogg
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s http://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd libogg-${OGG_VERSION} && \
        ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --disable-shared --datadir=${DIR} && \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR} && \
# libopus
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s http://downloads.xiph.org/releases/opus/opus-${OPUS_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd opus-${OPUS_VERSION} && \
        autoreconf -fiv && \
        ./configure --prefix="${SRC}" --disable-shared --datadir="${DIR}" && \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR} && \
# libvorbis
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd libvorbis-${VORBIS_VERSION} && \
        ./configure --prefix="${SRC}" --with-ogg="${SRC}" --bindir="${SRC}/bin" \
        --disable-shared --datadir="${DIR}" && \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR}  && \
# libtheora
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.bz2 | \
        tar jxvf - -C . && \
        cd libtheora-${THEORA_VERSION} && \
        ./configure --prefix="${SRC}" --with-ogg="${SRC}" --bindir="${SRC}/bin" \
        --disable-shared --datadir="${DIR}" && \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR} && \
# libvpx
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s https://codeload.github.com/webmproject/libvpx/tar.gz/v${VPX_VERSION} | \
        tar zxf - -C . && \
        cd libvpx-${VPX_VERSION} && \
        ./configure --prefix="${SRC}" --enable-vp8 --enable-vp9 --disable-examples --disable-docs && \
        make && \
        make install && \
        make clean && \
        rm -rf ${DIR} && \
# libmp3lame
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -Ls https://downloads.sf.net/project/lame/lame/${LAME_VERSION%.*}/lame-${LAME_VERSION}.tar.gz \
        | tar zxf - -C . && \
        cd lame-${LAME_VERSION} && \
        ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --disable-shared --enable-nasm --datadir="${DIR}" && \
        make && \
        make install && \
        make distclean&& \
        rm -rf ${DIR} && \
# faac + http://stackoverflow.com/a/4320377
        DIR=$(mktemp -d) &&  cd ${DIR} && \
        curl -Lss https://downloads.sf.net/faac/faac-${FAAC_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd faac-${FAAC_VERSION} && \
        sed -i '126d' common/mp4v2/mpeg4ip.h && \
        ./bootstrap && \
        ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --datadir="${DIR}" && \
        make && \
        make install && \
        rm -rf ${DIR} && \
# xvid
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -L -s  http://downloads.xvid.org/downloads/xvidcore-${XVID_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd xvidcore/build/generic && \
        ./configure --prefix="${SRC}" --bindir="${SRC}/bin" --datadir="${DIR}" && \
        make && \
        make install && \
        rm -rf ${DIR} && \
# fdk-aac
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s https://codeload.github.com/mstorsjo/fdk-aac/tar.gz/v${FDKAAC_VERSION} | \
        tar zxf - -C . && \
        cd fdk-aac-${FDKAAC_VERSION} && \
        autoreconf -fiv && \
        ./configure --prefix="${SRC}" --disable-shared --datadir="${DIR}" && \
        make && \
        make install && \
        make distclean && \
        rm -rf ${DIR} && \
# # ffmpeg
        DIR=$(mktemp -d) && cd ${DIR} && \
        curl -s http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz | \
        tar zxf - -C . && \
        cd ffmpeg-${FFMPEG_VERSION} && \
        ./configure --prefix="${SRC}" \
        --extra-cflags="-I${SRC}/include" \
        --extra-ldflags="-L${SRC}/lib" \
        --bindir="${SRC}/bin" \
        --disable-doc \
        --extra-libs=-ldl \
        --enable-version3 \
        --enable-libfaac \
        --enable-libfdk_aac \
        --enable-libmp3lame \
        --enable-libopus \
        --enable-libtheora \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libxvid \
        --enable-gpl \
        --enable-avresample \
        --enable-postproc \
        --enable-nonfree \
        --disable-debug \
        --enable-small \
        --enable-openssl && \
        make && \
        make install && \
        make distclean && \
        hash -r && \
        cd tools && \
        make qt-faststart && \
        cp qt-faststart ${SRC}/bin && \
        rm -rf ${DIR} && \
# cleanup
        apt-get purge -yqq \
        autoconf \
        automake \
        bzip2 \
        cmake \
        g++ \
        gcc \
        git \
        libtool \
        libssl-dev \
        make \
        nasm \
        perl \
        pkg-config \
        python \
        xmlto \
        zlib1g-dev && \
        apt-get autoremove -y && \
        apt-get clean -y && \
        rm -rf /var/lib/apt/lists && \
        ffmpeg -buildconf

# Let's make sure the app built correctly
# Convenient to verify on https://hub.docker.com/r/jrottenberg/ffmpeg/builds/ console output
