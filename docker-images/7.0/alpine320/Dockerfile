# ffmpeg - http://ffmpeg.org/download.html
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#

FROM        alpine:3.20 as base

RUN         apk add --no-cache --update libgcc libstdc++ ca-certificates openssl expat git

FROM        base as build

WORKDIR     /tmp/workdir

ENV         FFMPEG_VERSION=7.0.2 \
    AOM_VERSION=v3.8.1 \
    CHROMAPRINT_VERSION=1.5.0 \
    FDKAAC_VERSION=0.1.5 \
    FONTCONFIG_VERSION=2.12.4 \
    FREETYPE_VERSION=2.10.4 \
    FRIBIDI_VERSION=0.19.7 \
    KVAZAAR_VERSION=2.0.0 \
    LAME_VERSION=3.100 \
    LIBASS_VERSION=0.13.7 \
    LIBPTHREAD_STUBS_VERSION=0.4 \
    LIBVIDSTAB_VERSION=1.1.0 \
    LIBXCB_VERSION=1.13.1 \
    XCBPROTO_VERSION=1.13 \
    OGG_VERSION=1.3.2 \
    OPENCOREAMR_VERSION=0.1.6 \
    OPUS_VERSION=1.2 \
    OPENJPEG_VERSION=2.5.2 \
    PYTHON=python3 \
    THEORA_VERSION=1.1.1 \
    VORBIS_VERSION=1.3.5 \
    VPX_VERSION=1.8.0 \
    WEBP_VERSION=1.0.2 \
    X264_VERSION=20191217-2245-stable \
    X265_VERSION=4.0 \
    XAU_VERSION=1.0.9 \
    XORG_MACROS_VERSION=1.19.2 \
    XPROTO_VERSION=7.0.31 \
    XVID_VERSION=1.3.7 \
    LIBXML2_VERSION=2.9.12 \
    LIBBLURAY_VERSION=1.1.2 \
    # LIBZMQ_VERSION=4.3.5 \
    LIBSRT_VERSION=1.5.3 \
    LIBARIBB24_VERSION=1.0.3 \
    LIBPNG_VERSION=1.6.9 \
    LIBVMAF_VERSION=2.3.1 \
    ZIMG_VERSION=3.0.5 \
    SRC=/usr/local

ARG         FREETYPE_SHA256SUM="5eab795ebb23ac77001cfb68b7d4d50b5d6c7469247b0b01b2c953269f658dac freetype-2.10.4.tar.gz"
ARG         FRIBIDI_SHA256SUM="3fc96fa9473bd31dcb5500bdf1aa78b337ba13eb8c301e7c28923fea982453a8 0.19.7.tar.gz"
ARG         LIBASS_SHA256SUM="8fadf294bf701300d4605e6f1d92929304187fca4b8d8a47889315526adbafd7 0.13.7.tar.gz"
ARG         LIBVIDSTAB_SHA256SUM="14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb v1.1.0.tar.gz"
ARG         OGG_SHA256SUM="e19ee34711d7af328cb26287f4137e70630e7261b17cbe3cd41011d73a654692 libogg-1.3.2.tar.gz"
ARG         OPUS_SHA256SUM="77db45a87b51578fbc49555ef1b10926179861d854eb2613207dc79d9ec0a9a9 opus-1.2.tar.gz"
ARG         THEORA_SHA256SUM="40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b libtheora-1.1.1.tar.gz"
ARG         VORBIS_SHA256SUM="6efbcecdd3e5dfbf090341b485da9d176eb250d893e3eb378c428a2db38301ce libvorbis-1.3.5.tar.gz"
ARG         LIBBLURAY_SHA256SUM="a3dd452239b100dc9da0d01b30e1692693e2a332a7d29917bf84bb10ea7c0b42 libbluray-1.1.2.tar.bz2"
ARG         LIBARIBB24_SHA256SUM="f61560738926e57f9173510389634d8c06cabedfa857db4b28fb7704707ff128 v1.0.3.tar.gz"


ARG         MAKEFLAGS="-j2"
ARG         PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig"
ARG         PREFIX="/opt/ffmpeg"
ARG         LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"


RUN         libDeps="libgomp \
                    # https://github.com/zeromq/libzmq/
                    zeromq \
                    zeromq-dev \
                    # https://sourceforge.net/projects/opencore-amr/
                    opencore-amr \
                    opencore-amr-dev \
                    # https://www.xiph.org/ogg/
                    libogg \
                    libogg-static \
                    libogg-dev \
                    # libtheora http://www.theora.org/
                    libtheora \
                    libtheora-static \
                    libtheora-dev \
                    # http://www.videolan.org/developers/x264.html
                    x264 \
                    x264-libs \
                    x264-dev \
                    # http://x265.org/
                    x265 \
                    x265-libs \
                    x265-dev \
                    # https://www.opus-codec.org/
                    opus \
                    opus-tools \
                    opus-dev \
                    # https://xiph.org/vorbis/
                    libvorbis \
                    libvorbis-static \
                    libvorbis-dev \
                    # https://www.webmproject.org/code/
                    libvpx \
                    libvpx-utils \
                    libvpx-dev \
                    # https://developers.google.com/speed/webp/
                    libwebp \
                    libwebp-dev \
                    libwebp-static \
                    libwebp-tools \
                    # http://lame.sourceforge.net/
                    lame \
                    lame-libs \
                    lame-dev \
                    # https://www.xvid.com/
                    xvidcore \
                    xvidcore-static \
                    xvidcore-dev \
                    # https://github.com/mstorsjo/fdk-aac
                    fdk-aac \
                    fdk-aac-dev \
                    # https://github.com/uclouvain/openjpeg
                    openjpeg \
                    openjpeg-tools \
                    openjpeg-dev \
                    # https://www.freetype.org/
                    freetype \
                    freetype-static \
                    freetype-dev \
                    # https://github.com/georgmartius/vid.stab
                    vidstab \
                    vidstab-dev \
                    ## https://www.fribidi.org/
                    fribidi \
                    fribidi-static \
                    fribidi-dev \
                    # fontconfig https://www.freedesktop.org/wiki/Software/fontconfig/
                    fontconfig \
                    fontconfig-static \
                    fontconfig-dev \
                    # https://github.com/libass/libass
                    libass \
                    libass-dev \
                    # https://aomedia.googlesource.com/aom
                    aom \ 
                    aom-libs \
                    aom-dev \
                    # https://xcb.freedesktop.org/
                    # https://www.x.org/archive//individual/util/util-macros-
                    util-macros \
                    # https://www.x.org/archive/individual/proto/xproto-
                    xorgproto \
                    # https://www.x.org/archive/individual/lib/libXau-
                    libxau \
                    libxau-dev \
                    # https://github.com/GNOME/libxml2/
                    libxml2 \
                    libxml2-static \
                    libxml2-utils \
                    libxml2-dev \
                    # https://github.com/Haivision/srt
                    libsrt \
                    libsrt-progs \
                    libsrt-dev \
                    # https://git.code.sf.net/p/libpng/code
                    libpng \
                    libpng-static \
                    libpng-utils \
                    libpng-dev \
                    # https://github.com/sekrit-twc/zimg
                    zimg \
                    zimg-dev" && \
            apk add --no-cache --update ${libDeps}


RUN     buildDeps="autoconf \
                   automake \
                   bash \
                   binutils \
                   bzip2 \
                   cmake \
                   coreutils \
                   curl \
                   diffutils \
                   expat-dev \
                   file \
                   g++ \
                   gcc \
                   gperf \
                   libtool \
                   make \
                   nasm \
                   openssl-dev \
                   python3 \
                   tar \
                   xcb-proto \
                   yasm \
                   zlib-dev \
                   alpine-sdk \
                   linux-headers" && \
        apk add --no-cache --update ${buildDeps}
## libvmaf https://github.com/Netflix/vmaf
RUN \
        if which meson || false; then \
        echo "Building VMAF." && \
        DIR=/tmp/vmaf && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/Netflix/vmaf/archive/v${LIBVMAF_VERSION}.tar.gz && \
        tar -xz --strip-components=1 -f v${LIBVMAF_VERSION}.tar.gz && \
        cd /tmp/vmaf/libvmaf && \
        meson build --buildtype release --prefix=${PREFIX} && \
        ninja -vC build && \
        ninja -vC build install && \
        mkdir -p ${PREFIX}/share/model/ && \
        cp -r /tmp/vmaf/model/* ${PREFIX}/share/model/ && \
        rm -rf ${DIR}; \
        else \
        echo "VMAF skipped."; \
        fi

## kvazaar https://github.com/ultravideo/kvazaar
RUN \
        DIR=/tmp/kvazaar && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/ultravideo/kvazaar/archive/v${KVAZAAR_VERSION}.tar.gz && \
        tar -zx --strip-components=1 -f v${KVAZAAR_VERSION}.tar.gz && \
        ./autogen.sh && \
        ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}

# libevent && libevent-dev has usr/lib/libevent_pthreads ???
RUN \
        DIR=/tmp/libpthread-stubs && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://xcb.freedesktop.org/dist/libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}.tar.gz && \
        tar -zx --strip-components=1 -f libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" && \
        make && \
        make install && \
        rm -rf ${DIR}


## libbluray - Requires libxml, freetype, and fontconfig
RUN \
        DIR=/tmp/libbluray && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://download.videolan.org/pub/videolan/libbluray/${LIBBLURAY_VERSION}/libbluray-${LIBBLURAY_VERSION}.tar.bz2 && \
        echo ${LIBBLURAY_SHA256SUM} | sha256sum --check && \
        tar -jx --strip-components=1 -f libbluray-${LIBBLURAY_VERSION}.tar.bz2 && \
        ./configure --prefix="${PREFIX}" --disable-examples --disable-bdjava-jar --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}

## libaribb24
RUN \
        DIR=/tmp/b24 && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/nkoriyama/aribb24/archive/v${LIBARIBB24_VERSION}.tar.gz && \
        echo ${LIBARIBB24_SHA256SUM} | sha256sum --check && \
        tar -xz --strip-components=1 -f v${LIBARIBB24_VERSION}.tar.gz && \
       
        autoreconf -fiv && \
        ./configure CFLAGS="-I${PREFIX}/include -fPIC" --prefix="${PREFIX}" && \
        make && \
        make install && \
        rm -rf ${DIR}

## Download ffmpeg https://ffmpeg.org/
RUN  \
        DIR=/tmp/ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
        curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        ./configure     --disable-debug  --disable-doc    --disable-ffplay   --enable-shared --enable-gpl  --extra-libs=-ldl && \
        make ;  make install





# ## Build ffmpeg https://ffmpeg.org/
RUN  \
        DIR=/tmp/ffmpeg && cd ${DIR} && \
        ./configure \
        --disable-debug \
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
        --extra-cflags="-I${PREFIX}/include" \
        --extra-ldflags="-L${PREFIX}/lib" \
        --extra-libs=-ldl \
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


RUN \
    ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp {} /usr/local/lib/ && \
    for lib in /usr/local/lib/*.so.*; do ln -sf "${lib##*/}" "${lib%%.so.*}".so; done && \
    cp ${PREFIX}/bin/* /usr/local/bin/ && \
    cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
    LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf && \
    mkdir -p /usr/local/include && \
    cp -r ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include && \
    mkdir -p /usr/local/lib/pkgconfig && \
    for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc ${PREFIX}/lib/pkgconfig/libsw*.pc; do \
        sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"; \
    done

### Release Stage
FROM        base as release
LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]

COPY --from=build /usr/local /usr/local
