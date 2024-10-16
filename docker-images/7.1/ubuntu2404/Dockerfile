# ffmpeg - http://ffmpeg.org/download.html
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#
FROM        ubuntu:24.04 AS base

WORKDIR     /tmp/workdir

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ca-certificates openssl expat libgomp1 && \
        apt-get autoremove -y && \
        apt-get clean -y

FROM base AS build

ENV         FFMPEG_VERSION=7.1 \
    KVAZAAR_VERSION=2.3.1 \
    LIBVMAF_VERSION=3.0.0

## opencore-amr - https://sourceforge.net/projects/opencore-amr/
##         x264 - http://www.videolan.org/developers/x264.html
##         x265 - http://x265.org/ ( videolan )
##       libogg - https://www.xiph.org/ogg/ ( xiph )
##      libopus - https://www.opus-codec.org/ ( xiph )
##              - https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libopus
##    libvorbis - https://xiph.org/vorbis/ ( xiph )
##       libvpx - https://www.webmproject.org/code/
##              - https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libvpx
##      libwebp - https://developers.google.com/speed/webp/
##   libmp3lame - http://lame.sourceforge.net/
##         xvid - https://www.xvid.com/ (xvidcore)
##      fdk-aac - https://github.com/mstorsjo/fdk-aac
##              - https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libfdk-aac
##     openjpeg - https://github.com/uclouvain/openjpeg
##     freetype - https://www.freetype.org/
##                consider passing --no-install-recommends for this one its globbie (if you do, pass in libfreetype6)
##   libvidstab - https://github.com/georgmartius/vid.stab
##      fridibi - https://www.fribidi.org/
##   fontconfig - https://www.freedesktop.org/wiki/Software/fontconfig/
##       libass - https://github.com/libass/libass
##      lib aom - https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libaom
##    libsvtav1 - https://gitlab.com/AOMediaCodec/SVT-AV1.git
##              - https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libsvtav1
##     libdav1d - https://code.videolan.org/videolan/dav1d
##              - https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libdav1d
##  util-macros - (x.org) (and supporting libraries) for screen capture https://xcb.freedesktop.org/
##       xproto - (x.org)
##       libXau - 
##   libpthread - libpthread-stubs
##      libxml2 - for libbluray
##    libbluray - Requires libxml, freetype, and fontconfig
##       libzmq - https://github.com/zeromq/libzmq/
##                this one pulls in a bunch of dependencies
##       libpng - this one also pulls in a bunch of stuff
##   libaribb24 - 
##         zimg - https://github.com/sekrit-twc/zimg
##    libtheora - http://www.theora.org/ ( xiph )
##              - https://stackoverflow.com/questions/4810996/how-to-resolve-configure-guessing-build-type-failure
##       libsrt - https://github.com/Haivision/srt
##                Secure Reliable Transport UDP streaming library
##                multiple flavors (OpenSSL flavour) and ( GnuTLS flavour)
ARG OPENCORE_PKGS="libopencore-amrnb-dev libopencore-amrwb-dev"
ARG X264_PKGS="libx264-dev"
ARG X265_PKGS="libx265-dev libnuma-dev"
ARG OGG_PKGS="libogg-dev"
ARG OPUS_PKGS="libopus-dev"
ARG VORBIS_PKGS="libvorbis-dev"
ARG VPX_PKGS="libvpx-dev"
ARG WEBP_PKGS="libwebp-dev"
ARG MP3LAME_PKGS="libmp3lame-dev"
ARG XVIDCORE_PKGS="libxvidcore-dev"
ARG FDKAAC_PKGS="libfdk-aac-dev"
ARG OPENJP_PKGS="libopenjp2-7-dev"
ARG FREETYPE_PKGS="libfreetype6-dev"
ARG VIDSTAB_PKGS="libvidstab-dev"
ARG FRIBIDI_PKGS="libfribidi-dev"
ARG FONTCONFIG_PKGS="libfontconfig-dev fontconfig-config"
ARG LIBASS_PKGS="libass-dev"
ARG AOM_PKGS="libaom-dev"
ARG SVTAV1_PKGS="libsvtav1-dev libsvtav1enc-dev libsvtav1dec-dev"
ARG DAV1D_PKGS="libdav1d-dev"
ARG XORG_MACROS_PKGS="libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev"
ARG XPROTO_PKGS="x11proto-core-dev"
ARG XAU_PKGS="libxau-dev"
ARG PTHREAS_STUBS_PKGS="libpthread-stubs0-dev"
ARG XML2_PKGS="libxml2-dev"
ARG BLURAY_PKGS="libbluray-dev"
ARG ZMQ_PKGS="libzmq3-dev"
ARG PNG_PKGS="libpng-dev"
ARG ARIBB24_PKGS="libaribb24-dev"
ARG ZIMG_PKGS="libzimg-dev"
ARG THEORA_PKGS="libtheora-dev"
ARG SRT_PKGS="libssl-dev libsrt-openssl-dev"
ARG LIBDRM_PKGS="libdrm-dev libdrm2 libxcb1-dev libxcb1"

ARG MAKEFLAGS="-j2"
ARG PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"

ARG PREFIX="/opt/ffmpeg"
ARG LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"


ARG DEBIAN_FRONTEND=noninteractive

RUN      buildDeps="autoconf \
                    automake \
                    cmake \
                    build-essential \
                    texinfo \
                    curl \
                    wget \
                    bzip2 \
                    libexpat1-dev \
                    gcc \
                    git \
                    git-core \
                    gperf \
                    libtool \
                    make \
                    meson \
                    ninja-build \
                    nasm \
                    perl \
                    pkg-config \
                    python3 \
                    yasm \
                    zlib1g-dev \
                    libfreetype6-dev \
                    libgnutls28-dev \
                    libsdl2-dev \
                    libva-dev \
                    libvdpau-dev \
                    libnuma-dev" && \
        apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ${buildDeps}

RUN \
        echo "Installing dependencies..." && \
        apt-get install -yq ${OPENCORE_PKGS} ${X264_PKGS} ${X265_PKGS} ${OGG_PKGS} ${OPUS_PKGS} ${VORBIS_PKGS} ${VPX_PKGS} ${WEBP_PKGS} ${MP3LAME_PKGS} ${XVIDCORE_PKGS} ${FDKAAC_PKGS} ${OPENJP_PKGS} ${FREETYPE_PKGS} ${VIDSTAB_PKGS} ${FRIBIDI_PKGS} ${FONTCONFIG_PKGS} ${LIBASS_PKGS} ${AOM_PKGS} ${SVTAV1_PKGS} ${DAV1D_PKGS} ${XORG_MACROS_PKGS} ${XPROTO_PKGS} ${XAU_PKGS} ${PTHREAS_STUBS_PKGS} ${XML2_PKGS} ${BLURAY_PKGS} ${ZMQ_PKGS} ${PNG_PKGS} ${ARIBB24_PKGS} ${ZIMG_PKGS} ${THEORA_PKGS} ${SRT_PKGS} ${LIBDRM_PKGS}

        # apt install libdrm-dev

## kvazaar https://github.com/ultravideo/kvazaar
RUN \
        echo "Building kvazaar-${KVAZAAR_VERSION}" && \
        DIR=/tmp/kvazaar && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/ultravideo/kvazaar/releases/download/v${KVAZAAR_VERSION}/kvazaar-${KVAZAAR_VERSION}.tar.gz && \
        tar -zx --strip-components=1 -f kvazaar-${KVAZAAR_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}

## libvmaf https://github.com/Netflix/vmaf
RUN \
        echo "Adding g++ for VMAF build" && \
        apt-get install -yq g++

# https://github.com/Netflix/vmaf/issues/788
RUN \
        if which meson || false; then \
        echo "Building VMAF v${LIBVMAF_VERSION}" && \
        DIR=/tmp/vmaf && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/Netflix/vmaf/archive/refs/tags/v${LIBVMAF_VERSION}.tar.gz && \
        tar -xz --strip-components=1 -f v${LIBVMAF_VERSION}.tar.gz && \
        ls -al && \
        mkdir ./libvmaf/build && \
        cd ./libvmaf/build && \
        meson setup -Denable_tests=false -Denable_docs=false --buildtype=release --default-library=static .. --prefix "${PREFIX}" && \
        ninja && \
        ninja install && \
        # meson build --buildtype release --prefix=${PREFIX} && \
        # ninja -vC build && \
        # ninja -vC build install && \
        mkdir -p ${PREFIX}/share/model/ && \
        cp -r /tmp/vmaf/model/* ${PREFIX}/share/model/ && \
        rm -rf ${DIR}; \
        else \
        echo "VMAF skipped."; \
        fi


## Download ffmpeg https://ffmpeg.org/
RUN  \
        echo "Building (intial configure) ffmpeg-${FFMPEG_VERSION}" && \
        DIR=/tmp/ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
        curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        ./configure     --disable-debug  --disable-doc    --disable-ffplay   --enable-shared --enable-gpl  --extra-libs=-ldl && \
        make ;  make install



# ## Build ffmpeg https://ffmpeg.org/
RUN  \
        echo "Building (final detailed configure) ffmpeg-${FFMPEG_VERSION}" && \
        echo "PKG_CONFIG_PATH=${PKG_CONFIG_PATH}" && \
        dpkg -l |grep srt && \
        DIR=/tmp/ffmpeg && cd ${DIR} && \
        export PKG_CONFIG_PATH=${PKG_CONFIG_PATH} && \
        ./configure  \
        --enable-fontconfig \
        --enable-libaom \
        --enable-libaribb24 \
        --enable-libass \
        --enable-libbluray \
        --enable-libdav1d \
        --enable-libfdk-aac \
        --enable-libfreetype \
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
        --enable-small \
        --enable-version3 \
        --extra-cflags="-I${PREFIX}/include -I/usr/include/x86_64-linux-gnu" \
        --extra-ldflags="-L${PREFIX}/lib -L/usr/lib/x86_64-linux-gnu" \
        --extra-libs=-lm \
        --extra-libs=-lpthread \
        --ld=g++ \
        --prefix="${PREFIX}" && \
        make clean && \
        make && \
        make install && \
        make tools/zmqsend && cp tools/zmqsend ${PREFIX}/bin/ && \
        make distclean && \
        hash -r && \
        cd tools && \
        make qt-faststart && cp qt-faststart ${PREFIX}/bin/




## cleanup
RUN \
        ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/ && \
        for lib in /usr/local/lib/*.so.*; do ln -sf "${lib##*/}" "${lib%%.so.*}".so; done && \
        cp ${PREFIX}/bin/* /usr/local/bin/ && \
        cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
        LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf && \
        cp -r ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include && \
        mkdir -p /usr/local/lib/pkgconfig && \
        for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc ${PREFIX}/lib/pkgconfig/libsw*.pc; do \
          sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"; \
        done

FROM        base AS release

LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]

COPY --from=build /usr/local /usr/local/
