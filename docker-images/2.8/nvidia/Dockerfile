<<<<<<< HEAD
<<<<<<< HEAD
# ffmpeg - http://ffmpeg.org/download.html
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#

FROM    nvidia/cudagl:9.2-devel-ubuntu16.04 AS devel-base

ENV	    NVIDIA_DRIVER_CAPABILITIES compat32,compute,video
WORKDIR     /tmp/workdir

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ca-certificates expat libgomp1 && \
        apt-get autoremove -y && \
        apt-get clean -y

FROM        nvidia/cudagl:9.2-runtime-ubuntu16.04 AS runtime-base

ENV	    NVIDIA_DRIVER_CAPABILITIES compat32,compute,video
WORKDIR     /tmp/workdir

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ca-certificates expat libgomp1 libxcb-shape0-dev && \
        apt-get autoremove -y && \
        apt-get clean -y


FROM  devel-base as build

ENV        NVIDIA_HEADERS_VERSION=8.1.24.9
ARG        PKG_CONFIG_PATH=/opt/ffmpeg/lib/pkgconfig
ENV        LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/ffmpeg/lib"
ARG        PREFIX=/opt/ffmpeg
ARG        MAKEFLAGS="-j12"

ENV         FFMPEG_VERSION=2.8.15 \
            AOM_VERSION=v1.0.0 \
            FDKAAC_VERSION=0.1.5 \
            FONTCONFIG_VERSION=2.12.4 \
            FREETYPE_VERSION=2.5.5 \
            FRIBIDI_VERSION=0.19.7 \
            KVAZAAR_VERSION=1.2.0 \
            LAME_VERSION=3.100 \
            LIBASS_VERSION=0.13.7 \
            LIBVIDSTAB_VERSION=1.1.0 \
            OGG_VERSION=1.3.2 \
            OPENCOREAMR_VERSION=0.1.5 \
            OPUS_VERSION=1.2 \
            OPENJPEG_VERSION=2.1.2 \
            THEORA_VERSION=1.1.1 \
            VORBIS_VERSION=1.3.5 \
            VPX_VERSION=1.8.0 \
            WEBP_VERSION=1.0.2 \
            X264_VERSION=20170226-2245-stable \
            X265_VERSION=3.1.1 \
            XVID_VERSION=1.3.4 \
            SRC=/usr/local

ARG         FREETYPE_SHA256SUM="5d03dd76c2171a7601e9ce10551d52d4471cf92cd205948e60289251daddffa8 freetype-2.5.5.tar.gz"
ARG         FRIBIDI_SHA256SUM="3fc96fa9473bd31dcb5500bdf1aa78b337ba13eb8c301e7c28923fea982453a8 0.19.7.tar.gz"
ARG         LIBASS_SHA256SUM="8fadf294bf701300d4605e6f1d92929304187fca4b8d8a47889315526adbafd7 0.13.7.tar.gz"
ARG         LIBVIDSTAB_SHA256SUM="14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb v1.1.0.tar.gz"
ARG         OGG_SHA256SUM="e19ee34711d7af328cb26287f4137e70630e7261b17cbe3cd41011d73a654692 libogg-1.3.2.tar.gz"
ARG         OPUS_SHA256SUM="77db45a87b51578fbc49555ef1b10926179861d854eb2613207dc79d9ec0a9a9 opus-1.2.tar.gz"
ARG         THEORA_SHA256SUM="40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b libtheora-1.1.1.tar.gz"
ARG         VORBIS_SHA256SUM="6efbcecdd3e5dfbf090341b485da9d176eb250d893e3eb378c428a2db38301ce libvorbis-1.3.5.tar.gz"
ARG         XVID_SHA256SUM="4e9fd62728885855bc5007fe1be58df42e5e274497591fec37249e1052ae316f xvidcore-1.3.4.tar.gz"



RUN      buildDeps="autoconf \
                    automake \
                    cmake \
                    curl \
                    bzip2 \
                    libexpat1-dev \
                    g++ \
                    gcc \
                    git \
                    gperf \
                    libtool \
                    make \
                    nasm \
                    perl \
                    pkg-config \
                    python \
                    libssl-dev \
                    yasm \
                    zlib1g-dev" && \
        apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ${buildDeps}

RUN \ 
	DIR=/tmp/nv-codec-headers && \
	git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git ${DIR} && \
	cd ${DIR} && \
	git checkout n${NVIDIA_HEADERS_VERSION} && \ 
	sed -i 's@/usr/local@'"$PREFIX"'@' Makefile && \
	make && \
	make install  && \
    rm -rf ${DIR}

## opencore-amr https://sourceforge.net/projects/opencore-amr/
RUN \
        DIR=/tmp/opencore-amr && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://versaweb.dl.sourceforge.net/project/opencore-amr/opencore-amr/opencore-amr-${OPENCOREAMR_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        ./configure --prefix="${PREFIX}" --enable-shared  && \
        make && \
        make install && \
        rm -rf ${DIR}
## x264 http://www.videolan.org/developers/x264.html
RUN \
        DIR=/tmp/x264 && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${X264_VERSION}.tar.bz2 | \
        tar -jx --strip-components=1 && \
        ./configure --prefix="${PREFIX}" --enable-shared --enable-pic --disable-cli && \
        make && \
        make install && \
        rm -rf ${DIR}
### x265 http://x265.org/
RUN \
        DIR=/tmp/x265 && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://download.videolan.org/pub/videolan/x265/x265_${X265_VERSION}.tar.gz  | \
        tar -zx && \
        cd x265_${X265_VERSION}/build/linux && \
        sed -i "/-DEXTRA_LIB/ s/$/ -DCMAKE_INSTALL_PREFIX=\${PREFIX}/" multilib.sh && \
        sed -i "/^cmake/ s/$/ -DENABLE_CLI=OFF/" multilib.sh && \
        ./multilib.sh && \
        make -C 8bit install && \
        rm -rf ${DIR}
### libogg https://www.xiph.org/ogg/
RUN \
        DIR=/tmp/ogg && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO http://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz && \
        echo ${OGG_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f libogg-${OGG_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" --enable-shared  && \
        make && \
        make install && \
        rm -rf ${DIR}
### libopus https://www.opus-codec.org/
RUN \
        DIR=/tmp/opus && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://archive.mozilla.org/pub/opus/opus-${OPUS_VERSION}.tar.gz && \
        echo ${OPUS_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f opus-${OPUS_VERSION}.tar.gz && \
        autoreconf -fiv && \
        ./configure --prefix="${PREFIX}" --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
### libvorbis https://xiph.org/vorbis/
RUN \
        DIR=/tmp/vorbis && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz && \
        echo ${VORBIS_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f libvorbis-${VORBIS_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
### libtheora http://www.theora.org/
RUN \
        DIR=/tmp/theora && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.gz && \
        echo ${THEORA_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f libtheora-${THEORA_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
### libvpx https://www.webmproject.org/code/
RUN \
        DIR=/tmp/vpx && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://codeload.github.com/webmproject/libvpx/tar.gz/v${VPX_VERSION} | \
        tar -zx --strip-components=1 && \
        ./configure --prefix="${PREFIX}" --enable-vp8 --enable-vp9 --enable-vp9-highbitdepth --enable-pic --enable-shared \
        --disable-debug --disable-examples --disable-docs --disable-install-bins  && \
        make && \
        make install && \
        rm -rf ${DIR}
### libwebp https://developers.google.com/speed/webp/
RUN \
        DIR=/tmp/vebp && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${WEBP_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        ./configure --prefix="${PREFIX}" --enable-shared  && \
        make && \
        make install && \
        rm -rf ${DIR}
### libmp3lame http://lame.sourceforge.net/
RUN \
        DIR=/tmp/lame && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://versaweb.dl.sourceforge.net/project/lame/lame/$(echo ${LAME_VERSION} | sed -e 's/[^0-9]*\([0-9]*\)[.]\([0-9]*\)[.]\([0-9]*\)\([0-9A-Za-z-]*\)/\1.\2/')/lame-${LAME_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --enable-shared --enable-nasm --enable-pic --disable-frontend && \
        make && \
        make install && \
        rm -rf ${DIR}
### xvid https://www.xvid.com/
RUN \
        DIR=/tmp/xvid && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO http://downloads.xvid.org/downloads/xvidcore-${XVID_VERSION}.tar.gz && \
        echo ${XVID_SHA256SUM} | sha256sum --check && \
        tar -zx -f xvidcore-${XVID_VERSION}.tar.gz && \
        cd xvidcore/build/generic && \
        ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --datadir="${DIR}" --enable-shared --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
### fdk-aac https://github.com/mstorsjo/fdk-aac
RUN \
        DIR=/tmp/fdk-aac && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://github.com/mstorsjo/fdk-aac/archive/v${FDKAAC_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        autoreconf -fiv && \
        ./configure --prefix="${PREFIX}" --enable-shared --datadir="${DIR}" && \
        make && \
        make install && \
        rm -rf ${DIR}
## openjpeg https://github.com/uclouvain/openjpeg
RUN \
        DIR=/tmp/openjpeg && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://github.com/uclouvain/openjpeg/archive/v${OPENJPEG_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        cmake -DBUILD_THIRDPARTY:BOOL=ON -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
        make && \
        make install && \
        rm -rf ${DIR}
## freetype https://www.freetype.org/
RUN  \
        DIR=/tmp/freetype && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://download.savannah.gnu.org/releases/freetype/freetype-${FREETYPE_VERSION}.tar.gz && \
        echo ${FREETYPE_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f freetype-${FREETYPE_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
## libvstab https://github.com/georgmartius/vid.stab
RUN  \
        DIR=/tmp/vid.stab && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/georgmartius/vid.stab/archive/v${LIBVIDSTAB_VERSION}.tar.gz &&\
        echo ${LIBVIDSTAB_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f v${LIBVIDSTAB_VERSION}.tar.gz && \
        cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
        make && \
        make install && \
        rm -rf ${DIR}
## fridibi https://www.fribidi.org/
# + https://github.com/fribidi/fribidi/issues/8
RUN  \
        DIR=/tmp/fribidi && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/fribidi/fribidi/archive/${FRIBIDI_VERSION}.tar.gz && \
        echo ${FRIBIDI_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f ${FRIBIDI_VERSION}.tar.gz && \
        sed -i 's/^SUBDIRS =.*/SUBDIRS=gen.tab charset lib/' Makefile.am && \
        ./bootstrap --no-config && \
        ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
        make -j 1 && \
        make install && \
        rm -rf ${DIR}
## fontconfig https://www.freedesktop.org/wiki/Software/fontconfig/
RUN  \
        DIR=/tmp/fontconfig && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://www.freedesktop.org/software/fontconfig/release/fontconfig-${FONTCONFIG_VERSION}.tar.bz2 &&\
        tar -jx --strip-components=1 -f fontconfig-${FONTCONFIG_VERSION}.tar.bz2 && \
        ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
## libass https://github.com/libass/libass
RUN  \
        DIR=/tmp/libass && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/libass/libass/archive/${LIBASS_VERSION}.tar.gz &&\
        echo ${LIBASS_SHA256SUM} | sha256sum --check && \
        tar -zx --strip-components=1 -f ${LIBASS_VERSION}.tar.gz && \
        ./autogen.sh && \
        ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
## kvazaar https://github.com/ultravideo/kvazaar
RUN \
        DIR=/tmp/kvazaar && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO https://github.com/ultravideo/kvazaar/archive/v${KVAZAAR_VERSION}.tar.gz &&\
        tar -zx --strip-components=1 -f v${KVAZAAR_VERSION}.tar.gz && \
        ./autogen.sh && \
        ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}

RUN \
	DIR=/tmp/aom && \
        git clone --branch ${AOM_VERSION} --depth 1 https://aomedia.googlesource.com/aom ${DIR} ; \
        cd ${DIR} ; \
        rm -rf CMakeCache.txt CMakeFiles ; \
        mkdir -p ./aom_build ; \
        cd ./aom_build ; \
        cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 ..; \
        make ; \
        make install ; \
        rm -rf ${DIR}

## ffmpeg https://ffmpeg.org/
RUN  \
        DIR=/tmp/ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
        curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2



RUN \
        DIR=/tmp/ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
        ./configure \
        --disable-debug \
        --disable-doc \
        --disable-ffplay \
      --enable-nvenc \
        --enable-shared \
        --enable-avresample \
        --enable-libopencore-amrnb \
        --enable-libopencore-amrwb \
        --enable-gpl \
        --enable-libass \
        --enable-libfreetype \
        --enable-libvidstab \
        --enable-libmp3lame \
         \
        --enable-libopus \
        --enable-libtheora \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libwebp \
        --enable-libx265 \
        --enable-libxvid \
        --enable-libx264 \
        --enable-nonfree \
        --enable-openssl \
        --enable-libfdk_aac \
         \
        \
        --enable-postproc \
        --enable-small \
        --enable-version3 \
        --extra-cflags="-I${PREFIX}/include -I${PREFIX}/include/ffnvcodec -I/usr/local/cuda/include/" \
        --extra-ldflags="-L${PREFIX}/lib -L/usr/local/cuda/lib64/ -L/usr/local/cuda/lib32/" \
        --extra-libs=-ldl \
        --prefix="${PREFIX}" && \
        make && \
        make install && \
        make distclean && \
        hash -r && \
        cd tools && \
        make qt-faststart && \
        cp qt-faststart ${PREFIX}/bin

## cleanup
RUN \
        ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp {} /usr/local/lib/ && \
        cp ${PREFIX}/bin/* /usr/local/bin/ && \
        cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
        LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf



FROM        runtime-base AS release
MAINTAINER  Julien Rottenberg <julien@rottenberg.info>

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]
ENV         LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"

COPY --from=build /usr/local/bin /usr/local/bin/
COPY --from=build /usr/local/share /usr/local/share/
COPY --from=build /usr/local/lib /usr/local/lib/

# Let's make sure the app built correctly
# Convenient to verify on https://hub.docker.com/r/jrottenberg/ffmpeg/builds/ console output

=======
=======
>>>>>>> fix extra comma
FROM        nvidia/cuda:10.1-runtime-ubuntu18.04 AS base

ENV     NVIDIA_DRIVER_CAPABILITIES=video

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends libva2 libva-drm2 i965-va-driver  ca-certificates expat libgomp1 libuuid1 libssl1.0 && \
        apt-get autoremove -y && \
        apt-get clean -y 

FROM base as build

WORKDIR     /tmp/workdir

ARG PREFIX=/tmp/build 
ARG MAKEFLAGS=-j6
ARG PKG_CONFIG_PATH=/tmp/build/lib/pkgconfig
ARG C_INCLUDE_PATH=/tmp/build/include/ffnvcodec

RUN apt-get -yqq update && \
    apt-get install -yq --no-install-recommends \
        libva-dev  \
        autoconf \
        automake \
        cmake \
        curl \
        bzip2 \
        libexpat1-dev \
        g++ \
        gcc \
        git \
        gperf \
        libtool \
        make \
        nasm \
        perl \
        pkg-config \
        python \
        libssl1.0-dev \
        yasm \
        zlib1g-dev \
        uuid-dev 

ARG	FFMPEG_VERSION=2.8.15
ARG	LIBOPENCORE_AMR_VERSION=0.1.5
ARG	LIBX264_VERSION=20190526-2245-stable
ARG	LIBX265_VERSION=3.0
ARG	LIBOGG_VERSION=1.3.3
ARG	LIBOPUS_VERSION=1.3.1
ARG	LIBVORBIS_VERSION=1.3.6
ARG	LIBTHEORA_VERSION=1.1.1
ARG	LIBVPX_VERSION=1.8.0
ARG	LIBMP3LAME_VERSION=3.100
ARG	LIBXVID_VERSION=1.3.5
ARG	LIBFDK_AAC_VERSION=0.1.6
ARG	LIBOPENJPEG_VERSION=1.5.2
ARG	LIBFREETYPE_VERSION=2.10.0
ARG	LIBVIDSTAB_VERSION=1.1.0
ARG	LIBFRIBIDI_VERSION=0.19.7
ARG	LIBFONTCONFIG_VERSION=2.13.1
ARG	LIBFREETYPE_VERSION=2.10.0
ARG	LIBFRIBIDI_VERSION=0.19.7
ARG	LIBFONTCONFIG_VERSION=2.13.1
ARG	LIBASS_VERSION=0.14.0
ARG	LIBKVAZAAR_VERSION=0.6.1
ARG	NVENC_VERSION=8.2.15.8

ARG	LIBOGG_SHA256SUM=c2e8a485110b97550f453226ec644ebac6cb29d1caef2902c007edab4308d985
ARG	LIBOPUS_SHA256SUM=65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d
ARG	LIBVORBIS_SHA256SUM=6ed40e0241089a42c48604dc00e362beee00036af2d8b3f46338031c9e0351cb
ARG	LIBTHEORA_SHA256SUM=40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b
ARG	LIBVIDSTAB_SHA256SUM=14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb
ARG	LIBFRIBIDI_SHA256SUM=3fc96fa9473bd31dcb5500bdf1aa78b337ba13eb8c301e7c28923fea982453a8
ARG	LIBFRIBIDI_SHA256SUM=3fc96fa9473bd31dcb5500bdf1aa78b337ba13eb8c301e7c28923fea982453a8

## opencore-amr https://sourceforge.net/projects/opencore-amr/
RUN \
    DIR=opencore-amr && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \ 
    curl -sL https://kent.dl.sourceforge.net/project/opencore-amr/opencore-amr/opencore-amr-${LIBOPENCORE_AMR_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    ./configure --prefix="${PREFIX}" --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
## x264 http://www.videolan.org/developers/x264.html
RUN \
    DIR=x264 && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sL https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${LIBX264_VERSION}.tar.bz2 | \
    tar -jx --strip-components=1 && \
    ./configure --prefix="${PREFIX}" --enable-shared --enable-pic && \
    make && \
    make install && \
    rm -rf ${DIR}
### x265 http://x265.org/
RUN \
    DIR=x265 && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sL https://download.videolan.org/pub/videolan/x265/x265_${LIBX265_VERSION}.tar.gz  | \
    tar -zx && \
    cd x265_${LIBX265_VERSION}/build/linux && \
    sed -i "/-DEXTRA_LIB/ s/$/ -DCMAKE_INSTALL_PREFIX=\${PREFIX}/" multilib.sh && \
    sed -i "/^cmake/ s/$/ -DENABLE_CLI=ON/" multilib.sh && \
    ./multilib.sh && \
    make -C 8bit install && \
    rm -rf ${DIR}
## libogg https://www.xiph.org/ogg/
RUN \
    DIR=ogg && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO http://downloads.xiph.org/releases/ogg/libogg-${LIBOGG_VERSION}.tar.gz && \
    echo "${LIBOGG_SHA256SUM}  libogg-${LIBOGG_VERSION}.tar.gz" | sha256sum --check && \
    tar -zx --strip-components=1 -f libogg-${LIBOGG_VERSION}.tar.gz && \
    ./configure --prefix="${PREFIX}" --enable-shared  && \
    make && \
    make install && \
    rm -rf ${DIR}
RUN \
    DIR=opus && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://archive.mozilla.org/pub/opus/opus-${LIBOPUS_VERSION}.tar.gz && \
    echo "${LIBOPUS_SHA256SUM}  opus-${LIBOPUS_VERSION}.tar.gz"| sha256sum --check && \
    tar -zx --strip-components=1 -f opus-${LIBOPUS_VERSION}.tar.gz && \
    autoreconf -fiv && \
    ./configure --prefix="${PREFIX}" --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
### libvorbis https://xiph.org/vorbis/
RUN \
    DIR=vorbis && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO http://downloads.xiph.org/releases/vorbis/libvorbis-${LIBVORBIS_VERSION}.tar.gz && \
    echo "${LIBVORBIS_SHA256SUM}  libvorbis-${LIBVORBIS_VERSION}.tar.gz" | sha256sum --check && \
    tar -zx --strip-components=1 -f libvorbis-${LIBVORBIS_VERSION}.tar.gz && \
    ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
### libtheora http://www.theora.org/
RUN \
        DIR=theora && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${LIBTHEORA_VERSION}.tar.gz && \
        echo "${LIBTHEORA_SHA256SUM}  libtheora-${LIBTHEORA_VERSION}.tar.gz" | sha256sum --check && \
        tar -zx --strip-components=1 -f libtheora-${LIBTHEORA_VERSION}.tar.gz && \
        ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
### libvpx https://www.webmproject.org/code/
RUN \
    DIR=vpx && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sL https://codeload.github.com/webmproject/libvpx/tar.gz/v${LIBVPX_VERSION} | \
    tar -zx --strip-components=1 && \
    ./configure --prefix="${PREFIX}" --enable-vp8 --enable-vp9 --enable-vp9-highbitdepth --enable-pic --enable-shared \
    --disable-debug --disable-examples --disable-docs && \
    make && \
    make install && \
    rm -rf ${DIR}

### libmp3lame http://lame.sourceforge.net/
RUN \
    DIR=lame && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sL https://kent.dl.sourceforge.net/project/lame/lame/$(echo ${LIBMP3LAME_VERSION} | sed -e 's/[^0-9]*\([0-9]*\)[.]\([0-9]*\)[.]\([0-9]*\)\([0-9A-Za-z-]*\)/\1.\2/')/lame-${LIBMP3LAME_VERSION}.tar.gz | \
    tar -zx --strip-components=1 && \
    ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --enable-shared --enable-nasm --enable-pic && \
    make && \
    make install && \
    rm -rf ${DIR}
### xvid https://www.xvid.com/
RUN \
        DIR=xvid && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sLO http://downloads.xvid.org/downloads/xvidcore-${LIBXVID_VERSION}.tar.gz && \
        tar -zx -f xvidcore-${LIBXVID_VERSION}.tar.gz && \
        cd xvidcore/build/generic && \
        ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --datadir="${DIR}" --enable-shared --enable-shared && \
        make && \
        make install && \
        rm -rf ${DIR}
### fdk-aac https://github.com/mstorsjo/fdk-aac
RUN \
        DIR=fdk-aac && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        curl -sL https://github.com/mstorsjo/fdk-aac/archive/v${LIBFDK_AAC_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        autoreconf -fiv && \
        ./configure --prefix="${PREFIX}" --enable-shared --datadir="${DIR}" && \
        make && \
        make install && \
        rm -rf ${DIR}
## openjpeg https://github.com/uclouvain/openjpeg
RUN \
        DIR=openjpeg && \
        mkdir -p ${DIR} && \
        cd ${DIR} && \
        if test `echo ${LIBOPENJPEG_VERSION} | tr -d '.'` -ge '210'; then \
                version_prefix='v'; \
        else \
                version_prefix='version.' ;\
        fi && \
        curl -sL https://github.com/uclouvain/openjpeg/archive/${version_prefix}${LIBOPENJPEG_VERSION}.tar.gz | \
        tar -zx --strip-components=1 && \
        cmake -DBUILD_THIRDPARTY:BOOL=ON -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
        make && \
        make install && \
        rm -rf ${DIR}
## freetype https://www.freetype.org/
RUN  \
    DIR=freetype && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://download.savannah.gnu.org/releases/freetype/freetype-${LIBFREETYPE_VERSION}.tar.gz && \
    tar -zx --strip-components=1 -f freetype-${LIBFREETYPE_VERSION}.tar.gz && \
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
## libvstab https://github.com/georgmartius/vid.stab
RUN  \
    DIR=vid.stab && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://github.com/georgmartius/vid.stab/archive/v${LIBVIDSTAB_VERSION}.tar.gz &&\
    echo "${LIBVIDSTAB_SHA256SUM}  v${LIBVIDSTAB_VERSION}.tar.gz" | sha256sum --check && \
    tar -zx --strip-components=1 -f v${LIBVIDSTAB_VERSION}.tar.gz && \
    cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
    make && \
    make install && \
    rm -rf ${DIR}
## fridibi https://www.fribidi.org/
# + https://github.com/fribidi/fribidi/issues/8
RUN  \
    DIR=fribidi && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://github.com/fribidi/fribidi/archive/${LIBFRIBIDI_VERSION}.tar.gz && \
    echo "${LIBFRIBIDI_SHA256SUM}  ${LIBFRIBIDI_VERSION}.tar.gz" | sha256sum --check && \
    tar -zx --strip-components=1 -f ${LIBFRIBIDI_VERSION}.tar.gz && \
    sed -i 's/^SUBDIRS =.*/SUBDIRS=gen.tab charset lib/' Makefile.am && \
    ./bootstrap --no-config && \
    ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
    make -j 1 && \
    make install && \
    rm -rf ${DIR}
## fontconfig https://www.freedesktop.org/wiki/Software/fontconfig/
RUN  \
    DIR=fontconfig && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://www.freedesktop.org/software/fontconfig/release/fontconfig-${LIBFONTCONFIG_VERSION}.tar.bz2 &&\
    tar -jx --strip-components=1 -f fontconfig-${LIBFONTCONFIG_VERSION}.tar.bz2 && \
    ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
## freetype https://www.freetype.org/
RUN  \
    DIR=freetype && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://download.savannah.gnu.org/releases/freetype/freetype-${LIBFREETYPE_VERSION}.tar.gz && \
    tar -zx --strip-components=1 -f freetype-${LIBFREETYPE_VERSION}.tar.gz && \
    ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
## fridibi https://www.fribidi.org/
# + https://github.com/fribidi/fribidi/issues/8
RUN  \
    DIR=fribidi && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://github.com/fribidi/fribidi/archive/${LIBFRIBIDI_VERSION}.tar.gz && \
    echo "${LIBFRIBIDI_SHA256SUM}  ${LIBFRIBIDI_VERSION}.tar.gz" | sha256sum --check && \
    tar -zx --strip-components=1 -f ${LIBFRIBIDI_VERSION}.tar.gz && \
    sed -i 's/^SUBDIRS =.*/SUBDIRS=gen.tab charset lib/' Makefile.am && \
    ./bootstrap --no-config && \
    ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
    make -j 1 && \
    make install && \
    rm -rf ${DIR}
## fontconfig https://www.freedesktop.org/wiki/Software/fontconfig/
RUN  \
    DIR=fontconfig && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://www.freedesktop.org/software/fontconfig/release/fontconfig-${LIBFONTCONFIG_VERSION}.tar.bz2 &&\
    tar -jx --strip-components=1 -f fontconfig-${LIBFONTCONFIG_VERSION}.tar.bz2 && \
    ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
RUN  \
    DIR=libass && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://github.com/libass/libass/archive/${LIBASS_VERSION}.tar.gz &&\
    tar -zx --strip-components=1 -f ${LIBASS_VERSION}.tar.gz && \
    ./autogen.sh && \
    ./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
    make && \
    make install && \
    rm -rf ${DIR}
## kvazaar https://github.com/ultravideo/kvazaar
RUN \
    DIR=kvazaar && \
    mkdir -p ${DIR} && \
    cd ${DIR} && \
    curl -sLO https://github.com/ultravideo/kvazaar/archive/v${LIBKVAZAAR_VERSION}.tar.gz &&\
    tar -zx --strip-components=1 -f v${LIBKVAZAAR_VERSION}.tar.gz && \
    if [ -e ./autogen.sh ]; then \
        ./autogen.sh && \
        ./configure -prefix="${PREFIX}" --disable-static --enable-shared ; \
    else \
        cd src ; \
    fi && \
    make && \
    make install && \
    rm -rf ${DIR}

RUN \ 
	DIR=nv-codec-headers && \
	git clone --branch n${NVENC_VERSION} --depth=1 https://git.videolan.org/git/ffmpeg/nv-codec-headers.git ${DIR} && \
	cd ${DIR} && \
	sed -i 's@/usr/local@'"$PREFIX"'@' Makefile && \
	make && \
	make install  && \
    rm -rf ${DIR}
RUN \
        DIR=ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
        curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
        ./configure \
        --disable-debug \
        --disable-doc \
        --disable-ffplay \
        --enable-shared \
        --enable-avresample \
        --enable-openssl \
        --enable-postproc \
        --enable-small \
        --extra-cflags="-I${PREFIX}/include -I/usr/local/include" \
        --extra-ldflags="-L${PREFIX}/lib -L/usr/local/lib" \
        --enable-libopencore-amrnb \
	--enable-libopencore-amrwb \
	--enable-version3 \
	--enable-libx264 \
	--enable-libx265 \
	--enable-libopus \
	--enable-libvorbis \
	--enable-libtheora \
	--enable-libvpx \
	--enable-libmp3lame \
	--enable-libxvid \
	--enable-libfdk_aac \
	--enable-nonfree \
	--enable-libopenjpeg \
	--enable-libfreetype \
	--enable-libvidstab \
	--enable-gpl \
	--enable-libass \
	--enable-libkvazaar \
	--enable-vaapi \
	--enable-nvenc \
	--enable-nonfree \
        --prefix="${PREFIX}" && \
        make && \
        make install && \
        make distclean && \
        hash -r && \
        cd tools && \
        make qt-faststart && \
        cp qt-faststart ${PREFIX}/bin

RUN \
    if false; then \
        cp -r ${PREFIX}/lib/*so* /usr/local/lib/ && \
        cp ${PREFIX}/bin/* /usr/local/bin/ ; \
    else \
        LD_LIBRARY_PATH=${PREFIX}/lib ldd ${PREFIX}/bin/ffmpeg | \
        grep ${PREFIX} | \
        cut -d ' ' -f 3 | \
        xargs -i cp {} /usr/local/lib/ && \
        cp ${PREFIX}/bin/ff* /usr/local/bin/ ; \
    fi && \
    if true; then \
        for lib in /usr/local/lib/*.so* /usr/local/bin/*; do strip --strip-all $lib; done ; \
    fi && \
    cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
    LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf

FROM        base AS release
MAINTAINER  Julien Rottenberg <julien@rottenberg.info>

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]

COPY --from=build /usr/local /usr/local
RUN test "base" = "base" && ldconfig /usr/local/lib /usr/local/lib64

# Let's make sure the app built correctly
# Convenient to verify on https://hub.docker.com/r/jrottenberg/ffmpeg/builds/ console output
<<<<<<< HEAD
>>>>>>> fix extra comma
=======
>>>>>>> fix extra comma
