# ffmpeg - http://ffmpeg.org/download.html
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#
# Stage 1: Build
FROM       ubuntu:24.04 AS builder


WORKDIR     /tmp/workdir

COPY generate-source-of-truth-ffmpeg-versions.py /tmp/workdir
COPY download_tarballs.sh /tmp/workdir
COPY build_source.sh /tmp/workdir

ENV         FFMPEG_VERSION=6.1.2 \
    AOM_VERSION=v3.10.0 \
    SVTAV1_VERSION=2.2.1 \
    CHROMAPRINT_VERSION=1.5.0 \
    FDKAAC_VERSION=2.0.3 \
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
    OGG_VERSION=1.3.5 \
    OPENCOREAMR_VERSION=0.1.6 \
    OPUS_VERSION=1.5.2 \
    OPENJPEG_VERSION=2.5.2 \
    PYTHON=python3 \
    THEORA_VERSION=1.1.1 \
    VORBIS_VERSION=1.3.7 \
    VPX_VERSION=1.14.1 \
    WEBP_VERSION=1.4.0 \
    X264_VERSION=20191217-2245-stable \
    X265_VERSION=4.0 \
    XAU_VERSION=1.0.9 \
    XORG_MACROS_VERSION=1.19.2 \
    XPROTO_VERSION=7.0.31 \
    XVID_VERSION=1.3.7 \
    LIBXML2_VERSION=2.9.12 \
    LIBBLURAY_VERSION=1.1.2 \
    LIBZMQ_VERSION=4.3.5 \
    LIBSRT_VERSION=1.5.3 \
    LIBARIBB24_VERSION=1.0.3 \
    LIBPNG_VERSION=1.6.9 \
    LIBVMAF_VERSION=3.0.0 \
    ZIMG_VERSION=3.0.5 \
    SRC=/usr/local

ARG         FREETYPE_SHA256SUM="5eab795ebb23ac77001cfb68b7d4d50b5d6c7469247b0b01b2c953269f658dac freetype-2.10.4.tar.gz"
ARG         FRIBIDI_SHA256SUM="3fc96fa9473bd31dcb5500bdf1aa78b337ba13eb8c301e7c28923fea982453a8 0.19.7.tar.gz"
ARG         LIBASS_SHA256SUM="8fadf294bf701300d4605e6f1d92929304187fca4b8d8a47889315526adbafd7 0.13.7.tar.gz"
ARG         LIBVIDSTAB_SHA256SUM="14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb v1.1.0.tar.gz"
# ARG         OGG_SHA256SUM="0eb4b4b9420a0f51db142ba3f9c64b333f826532dc0f48c6410ae51f4799b664 libogg-1.3.4.tar.gz"
ARG         OPUS_SHA256SUM="65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1 opus-1.5.2.tar.gz"
ARG         THEORA_SHA256SUM="40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b libtheora-1.1.1.tar.gz"
ARG         VORBIS_SHA256SUM="0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab libvorbis-1.3.7.tar.gz"
ARG         LIBBLURAY_SHA256SUM="a3dd452239b100dc9da0d01b30e1692693e2a332a7d29917bf84bb10ea7c0b42 libbluray-1.1.2.tar.bz2"
ARG         LIBARIBB24_SHA256SUM="f61560738926e57f9173510389634d8c06cabedfa857db4b28fb7704707ff128 v1.0.3.tar.gz"

ARG         MAKEFLAGS="-j2"
ARG         PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"
ARG         PREFIX="/opt/ffmpeg"
ARG         LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"


ARG DEBIAN_FRONTEND=noninteractive
RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends curl jq python3 python3-requests less tree && \
        chmod +x /tmp/workdir/download_tarballs.sh && \
        chmod +x /tmp/workdir/build_source.sh


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
                    libnuma-dev \
                    openssl \
                    expat \
                    libgomp1" && \
        apt-get -yqq update 
#        apt-get install -yq --no-install-recommends ${buildDeps}

# Download all of the dependencies on the first pass
# there is no point in waiting for all of the build time cpu, if we can't download everything we need to continue
# SHELL ["/bin/bash", "-c"]

# Define library URLs as individual environment variables
# ENV OPENCORE_AMR_URL="https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-${OPENCOREAMR_VERSION}.tar.gz"
# ENV X264_URL="https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${X264_VERSION}.tar.bz2"
# ENV X265_URL="http://ftp.videolan.org/pub/videolan/x265/x265_${X265_VERSION}.tar.gz"
# ... (define environment variables for all libraries)

# RUN \
#   echo "Downloading all of the libraries" && \
#   DIR=/tmp && \
#   mkdir -p "${DIR}"; cd "${DIR}" && \
#   for LIB in "${OPENCORE_AMR_URL}" "${X264_URL}" "${X265_URL}"; do echo "$LIB"; done

#   curl -sLO --retry 5 
# RUN \ 
#         echo "Downloading all of the libraries" && \
#         DIR=/tmp && \
#         mkdir -p ${DIR}; cd ${DIR} && \
#         curl -LO --retry 5 https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-${OPENCOREAMR_VERSION}.tar.gz \
#         curl -LO --retry 5 https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${X264_VERSION}.tar.bz2 \
#         curl -LO --retry 5 http://ftp.videolan.org/pub/videolan/x265/x265_${X265_VERSION}.tar.gz \
#         curl -LO --retry 5 https://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/xiph/opus/releases/download/v${OPUS_VERSION}/opus-${OPUS_VERSION}.tar.gz \
#         curl -LO --retry 5 http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz \
#         curl -LO --retry 5 https://chromium.googlesource.com/webm/libvpx.git/+archive/v${VPX_VERSION}.tar.gz \
#         curl -LO --retry 5 https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${WEBP_VERSION}.tar.gz \
#         curl -LO --retry 5 https://sourceforge.net/projects/lame/files/lame/${LAME_VERSION}/lame-${LAME_VERSION}.tar.gz \
#         curl -LO --retry 5 https://downloads.xvid.com/downloads/xvidcore-${XVID_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/mstorsjo/fdk-aac/archive/refs/tags/v${FDKAAC_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/uclouvain/openjpeg/archive/refs/tags/v${OPENJPEG_VERSION}.tar.gz \
#         curl -LO --retry 5 https://download.savannah.gnu.org/releases/freetype/freetype-${FREETYPE_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/georgmartius/vid.stab/archive/v${LIBVIDSTAB_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/fribidi/fribidi/archive/${FRIBIDI_VERSION}.tar.gz \
#         curl -LO --retry 5 https://www.freedesktop.org/software/fontconfig/release/fontconfig-${FONTCONFIG_VERSION}.tar.bz2 \
#         curl -LO --retry 5 https://github.com/libass/libass/archive/${LIBASS_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/ultravideo/kvazaar/releases/download/v${KVAZAAR_VERSION}/kvazaar-${KVAZAAR_VERSION}.tar.gz \
#         curl -LO --retry 5 https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v${SVTAV1_VERSION}/SVT-AV1-v${SVTAV1_VERSION}.tar.gz \
#         # curl -LO --retry 5 https://code.videolan.org/videolan/dav1d/-/archive/${DAV1D_VERSION}/dav1d-${DAV1D_VERSION}.tar.gz \
#         curl -LO --retry 5 https://www.x.org/releases/individual/util/util-macros-${XORG_MACROS_VERSION}.tar.gz \
#         curl -LO --retry 5 https://www.x.org/releases/individual/proto/xproto-${XPROTO_VERSION}.tar.gz \
#         curl -LO --retry 5 https://www.x.org/releases/individual/lib/libXau-${XAU_VERSION}.tar.gz \
#         curl -LO --retry 5 https://www.x.org/releases/individual/lib/libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}.tar.gz \
#         curl -LO --retry 5 ftp://xmlsoft.org/libxml2/libxml2-${LIBXML2_VERSION}.tar.gz \
#         curl -LO --retry 5 https://download.videolan.org/pub/videolan/libbluray/${LIBBLURAY_VERSION}/libbluray-${LIBBLURAY_VERSION}.tar.bz2 \
#         curl -LO --retry 5 https://github.com/zeromq/libzmq/releases/download/v${LIBZMQ_VERSION}/zeromq-${LIBZMQ_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/nkoriyama/aribb24/archive/v${LIBARIBB24_VERSION}.tar.gz -o aribb24-v${LIBARIBB24_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/sekrit-twc/zimg/archive/release-${ZIMG_VERSION}.tar.gz \
#         curl -LO --retry 5 http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.bz2 \
#         curl -LO --retry 5 https://github.com/Haivision/srt/archive/refs/tags/v${LIBSRT_VERSION}.tar.gz -o srt-v${LIBSRT_VERSION}.tar.gz \
#         curl -LO --retry 5 https://github.com/Netflix/vmaf/archive/refs/tags/v${LIBVMAF_VERSION}.tar.gz -o vmaf-v${LIBVMAF_VERSION}.tar.gz \
#         curl -LO --retry 5 https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2


RUN \
        python3 /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --mode manifest --output generated_build_manifest.json


RUN \
        /tmp/workdir/download_tarballs.sh

RUN \
        /tmp/workdir/build_source.sh

## opencore-amr https://sourceforge.net/projects/opencore-amr/
# DIR=/tmp/opencore-amr && \
# echo "Building opencore-amr-${OPENCOREAMR_VERSION}" && \
# local data=$(jq -r '.[] | select(.library_name == "'${lib_name}'")' $manifestJsonFile)
# build_dir=$(echo "$data" | jq -r '.build_dir')
# tarball_name=$(echo "$data" | jq -r '.tarball_name')
# SHELL ["/bin/bash"]
# ENV manifestJsonFile="/tmp/workdir/generated_build_manifest.json"
# RUN \
#         DATA=$(jq -r '.[] | select(.library_name == "opencore-amr")' ${manifestJsonFile}) && \
#         DIR=$(echo "$DATA" | jq -r '.build_dir') && \
#         TARBALL_NAME=$(echo "$DATA" | jq -r '.tarball_name') && \
#         echo "DIR: ${DIR} TARBALL_NAME: ${TARBALL_NAME}"
        # mkdir -p ${DIR}; cd ${DIR} && \
        # tar -zx --strip-components=1 -f ${TARBALL_NAME} && \
        # ./configure --prefix="${PREFIX}" --enable-shared  && \
        # make && \
        # make install && \
        # rm -rf ${DIR}

# ## x264 http://www.videolan.org/developers/x264.html
# RUN \
#         echo "Building x264-snapshot-${X264_VERSION}" && \
#         DIR=/tmp/x264 && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         tar -jx --strip-components=1 -f x264-snapshot-${X264_VERSION}.tar.bz2 && \
#         ./configure --prefix="${PREFIX}" --enable-shared --enable-pic --disable-cli && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## x265 http://x265.org/ ( videolan )
# RUN \
#         echo "Building x265_${X265_VERSION}" && \
#         DIR=/tmp/x265 && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         tar -zx x265_${X265_VERSION}.tar.gz && \
#         cd x265_${X265_VERSION}/build/linux && \
#         sed -i "/-DEXTRA_LIB/ s/$/ -DCMAKE_INSTALL_PREFIX=\${PREFIX}/" multilib.sh && \
#         sed -i "/^cmake/ s/$/ -DENABLE_CLI=OFF/" multilib.sh && \
#         ./multilib.sh && \
#         make -C 8bit install && \
#         rm -rf ${DIR}

# ## libogg https://www.xiph.org/ogg/ ( xiph )
# RUN \
#         echo "Building libogg-${OGG_VERSION}" && \
#         DIR=/tmp/ogg && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz && \
#         # echo ${OGG_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f ../libogg-${OGG_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --enable-shared  && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### libopus https://www.opus-codec.org/ ( xiph )
# #   https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libopus
# RUN \
#         echo "Building opus-${OPUS_VERSION}" && \
#         DIR=/tmp/opus && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://github.com/xiph/opus/releases/download/v${OPUS_VERSION}/opus-${OPUS_VERSION}.tar.gz | \
#         tar -zx --strip-components=1 ../opus-${OPUS_VERSION}.tar.gz && \
#         # echo ${OPUS_SHA256SUM} | sha256sum --check && \
#         ./configure --prefix="${PREFIX}" --enable-shared && \
#         # ./configure --prefix="$HOME/ffmpeg_build" --disable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### libvorbis https://xiph.org/vorbis/ ( xiph )
# RUN \
#         echo "Building libvorbis-${VORBIS_VERSION}" && \
#         DIR=/tmp/vorbis && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz && \
#         cp ../libvorbis-${VORBIS_VERSION}.tar.gz . && \
#         echo ${VORBIS_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f libvorbis-${VORBIS_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### libvpx https://www.webmproject.org/code/
# #          https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libvpx
# ### configure w/ --as=yasm ??
# ### double check that this came from the correct place.
# RUN \
#         echo "Building libvpx-${VPX_VERSION}" && \
#         DIR=/tmp/vpx && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://chromium.googlesource.com/webm/libvpx.git/+archive/v${VPX_VERSION}.tar.gz | \
#         tar -zxm ../v${VPX_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --enable-vp8 --enable-vp9 --enable-vp9-highbitdepth --enable-pic --enable-shared \
#         --disable-debug --disable-examples --disable-docs --disable-install-bins  && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### libwebp https://developers.google.com/speed/webp/
# RUN \
#         echo "Building libwebp-${WEBP_VERSION}" && \
#         DIR=/tmp/webp && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-${WEBP_VERSION}.tar.gz | \
#         tar -zx --strip-components=1 -f ../libwebp-${WEBP_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --enable-shared  && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### libmp3lame http://lame.sourceforge.net/
# RUN \
#         echo "Building lame-${LAME_VERSION}" && \
#         DIR=/tmp/lame && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://sourceforge.net/projects/lame/files/lame/${LAME_VERSION}/lame-${LAME_VERSION}.tar.gz/download | \
#         tar -zx --strip-components=1 -f ../lame-${LAME_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --enable-shared --enable-nasm --disable-frontend && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### xvid (xvidcore) https://www.xvid.com/
# RUN \
#         echo "Building xvidcore-${XVID_VERSION}" && \
#         DIR=/tmp/xvid && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://downloads.xvid.com/downloads/xvidcore-${XVID_VERSION}.tar.gz && \
#         tar -zx -f ../xvidcore-${XVID_VERSION}.tar.gz && \
#         cd xvidcore/build/generic && \
#         ./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### fdk-aac https://github.com/mstorsjo/fdk-aac
# #   https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libfdk-aac
# # might not need --datadir anymore
# RUN \
#         echo "Building fdk-aac-${FDKAAC_VERSION}" && \
#         DIR=/tmp/fdk-aac && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://github.com/mstorsjo/fdk-aac/archive/refs/tags/v${FDKAAC_VERSION}.tar.gz | \
#         tar -zx --strip-components=1 -f ../fdk-aac-${FDKAAC_VERSION}.tar.gz && \
#         autoreconf -fiv && \
#         ./configure --prefix="${PREFIX}" --enable-shared --datadir="${DIR}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## openjpeg https://github.com/uclouvain/openjpeg
# RUN \
#         echo "Building openjpeg-${OPENJPEG_VERSION}" && \
#         DIR=/tmp/openjpeg && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://github.com/uclouvain/openjpeg/archive/refs/tags/v${OPENJPEG_VERSION}.tar.gz | \
#         tar -zx --strip-components=1 -f ../openjpeg-${OPENJPEG_VERSION}.tar.gz && \
#         # cmake -DBUILD_THIRDPARTY:BOOL=ON -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
#         cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## freetype https://www.freetype.org/
# # make sure to pass in --no-install-recommends for this one its globbie
# RUN  \
#         echo "Building freetype-${FREETYPE_VERSION}" && \
#         DIR=/tmp/freetype && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://download.savannah.gnu.org/releases/freetype/freetype-${FREETYPE_VERSION}.tar.gz && \
#         cp ../freetype-${FREETYPE_VERSION}.tar.gz . && \
#         echo ${FREETYPE_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f freetype-${FREETYPE_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libvidstab https://github.com/georgmartius/vid.stab
# RUN  \
#         echo "Building libvidstab-${LIBVIDSTAB_VERSION}" && \
#         DIR=/tmp/vid.stab && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/georgmartius/vid.stab/archive/v${LIBVIDSTAB_VERSION}.tar.gz && \
#         cp ../v${LIBVIDSTAB_VERSION}.tar.gz . && \
#         echo ${LIBVIDSTAB_SHA256SUM} | sha256sum --check &&  \
#         tar -zx --strip-components=1 -f v${LIBVIDSTAB_VERSION}.tar.gz && \
#         cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## fridibi https://www.fribidi.org/
# RUN  \
#         echo "Building fribidi-${FRIBIDI_VERSION}" && \
#         DIR=/tmp/fribidi && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/fribidi/fribidi/archive/${FRIBIDI_VERSION}.tar.gz && \
#         cp ../${FRIBIDI_VERSION}.tar.gz . && \
#         echo ${FRIBIDI_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f ${FRIBIDI_VERSION}.tar.gz && \
#         sed -i 's/^SUBDIRS =.*/SUBDIRS=gen.tab charset lib bin/' Makefile.am && \
#         ./bootstrap --no-config --auto && \
#         ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make -j1 && \
#         make install && \
#         rm -rf ${DIR}

# ## fontconfig https://www.freedesktop.org/wiki/Software/fontconfig/
# RUN  \
#         echo "Building fontconfig-${FONTCONFIG_VERSION}" && \
#         DIR=/tmp/fontconfig && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://www.freedesktop.org/software/fontconfig/release/fontconfig-${FONTCONFIG_VERSION}.tar.bz2 && \

#         tar -zx --strip-components=1 -f ../fontconfig-${FONTCONFIG_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libass https://github.com/libass/libass
# RUN  \
#         echo "Building libass-${LIBASS_VERSION}" && \
#         DIR=/tmp/libass && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/libass/libass/archive/${LIBASS_VERSION}.tar.gz && \
#         cp ../${LIBASS_VERSION}.tar.gz . && \
#         echo ${LIBASS_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f ${LIBASS_VERSION}.tar.gz && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## kvazaar https://github.com/ultravideo/kvazaar
# RUN \
#         echo "Building kvazaar-${KVAZAAR_VERSION}" && \
#         DIR=/tmp/kvazaar && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/ultravideo/kvazaar/archive/v${KVAZAAR_VERSION}.tar.gz && \
#         tar -zx --strip-components=1 -f ../v${KVAZAAR_VERSION}.tar.gz && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}
# # lib aom 
# # https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libaom
# RUN \
#         echo "Building aom-${AOM_VERSION}" && \
#         DIR=/tmp/aom && \
#         git clone --branch ${AOM_VERSION} --depth 1 https://aomedia.googlesource.com/aom ${DIR} ; \
#         cd ${DIR} ; \
#         mkdir -p ./aom_build ; \
#         cd ./aom_build ; \
#         # cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 ..; \
#         cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 -DENABLE_NASM=on ..; \
#         make ; \
#         make install ; \
#         rm -rf ${DIR}

# ## libsvtav1 https://gitlab.com/AOMediaCodec/SVT-AV1.git
# #            https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libsvtav1
# # RUN \
# #         echo "Installing dependencies libpng" && \
# #         apt-get install -yq libsvtav1enc-dev

# RUN \
#         echo "Building SVT-AV1 v${SVTAV1_VERSION}" && \
#         DIR=/tmp/libsvtav1 && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v${SVTAV1_VERSION}/SVT-AV1-v${SVTAV1_VERSION}.tar.gz && \
#         tar -zx --strip-components=1 -f ../SVT-AV1-v${SVTAV1_VERSION}.tar.gz && \
#         cd Build && \
#         cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${PREFIX}"  -DCMAKE_BUILD_TYPE=Release -DBUILD_DEC=OFF -DBUILD_SHARED_LIBS=OFF ..; \
#         make ; \
#         make install ; \
#         rm -rf ${DIR}

# ## libdav1d https://code.videolan.org/videolan/dav1d
# ## https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libdav1d
# ## installed w/ apt-get in the build stage
# RUN \
#         echo "installing libdav1d-dev with debian packages" && \
#         apt-get install -yq libdav1d-dev

# ## x.org: util-macros (and supporting libraries) for screen capture https://xcb.freedesktop.org/
# RUN \
#         echo "Building x.org: util-macros-${XORG_MACROS_VERSION}" && \
#         DIR=/tmp/xorg-macros && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         tar -Jx --strip-components=1 -f ../util-macros-${XORG_MACROS_VERSION}.tar.zx && \
#         ./configure --srcdir=${DIR} --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## x.org: xproto
# RUN \
#         echo "Building x.org: xproto-${XPROTO_VERSION}" && \
#         DIR=/tmp/xproto && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://www.x.org/archive/individual/proto/xproto-${XPROTO_VERSION}.tar.gz && \
#         tar -zx --strip-components=1 -f ../xproto-${XPROTO_VERSION}.tar.gz && \
#         cp /usr/share/misc/config.guess . && \
#         ./configure --srcdir=${DIR} --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libXau
# RUN \
#         echo "Building x.org: libXau-${XAU_VERSION}" && \
#         DIR=/tmp/libXau && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         tar -Jx --strip-components=1 -f ../libXau-${XAU_VERSION}.tar.xz && \
#         ./configure --srcdir=${DIR} --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libpthread-stubs
# RUN \
#         echo "Building libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}" && \
#         DIR=/tmp/libpthread-stubs && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         tar -Jx --strip-components=1 -f ../libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}.tar.xz && \
#         ./configure --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}


# ## libxml2 - for libbluray
# RUN \
#         echo "Building libxml2-${LIBXML2_VERSION}" && \
#         DIR=/tmp/libxml2 && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         tar -xz --strip-components=1 -f ../libxml2-${LIBXML2_VERSION}.tar.gz && \
#         ./autogen.sh --prefix="${PREFIX}" --with-ftp=no --with-http=no --with-python=no && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libbluray - Requires libxml, freetype, and fontconfig
# RUN \
#         echo "Building libbluray-${LIBBLURAY_VERSION}" && \
#         DIR=/tmp/libbluray && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://download.videolan.org/pub/videolan/libbluray/${LIBBLURAY_VERSION}/libbluray-${LIBBLURAY_VERSION}.tar.bz2 && \
#         cp ../libbluray-${LIBBLURAY_VERSION}.tar.bz2 . && \
#         echo ${LIBBLURAY_SHA256SUM} | sha256sum --check && \
#         tar -jx --strip-components=1 -f libbluray-${LIBBLURAY_VERSION}.tar.bz2 && \
#         ./configure --prefix="${PREFIX}" --disable-examples --disable-bdjava-jar --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libzmq https://github.com/zeromq/libzmq/
# # this one pulls in a bunch of dependencies
# RUN \
#         echo "Building libzmq-${LIBZMQ_VERSION}" && \
#         DIR=/tmp/libzmq && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/zeromq/libzmq/releases/download/v${LIBZMQ_VERSION}/zeromq-${LIBZMQ_VERSION}.tar.gz && \
#         tar -xz --strip-components=1 -f ../zeromq-${LIBZMQ_VERSION}.tar.gz && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" && \
#         make && \
#         make check && \
#         make install && \
#         rm -rf ${DIR}


# ## libpng
# # also pulls in a bunch of stuff
# RUN \
#         echo "Building libpng-${LIBPNG_VERSION}" && \
#         DIR=/tmp/png && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         git clone https://git.code.sf.net/p/libpng/code ${DIR} -b v${LIBPNG_VERSION} --depth 1 && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" && \
#         make check && \
#         make install && \
#         rm -rf ${DIR}

# ## libaribb24
# RUN \
#         echo "Building libaribb24-${LIBARIBB24_VERSION}" && \
#         DIR=/tmp/b24 && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/nkoriyama/aribb24/archive/v${LIBARIBB24_VERSION}.tar.gz && \
#         cp ../v${LIBARIBB24_VERSION}.tar.gz . && \
#         echo ${LIBARIBB24_SHA256SUM} | sha256sum --check && \
#         tar -xz --strip-components=1 -f ../aribb24-v${LIBARIBB24_VERSION}.tar.gz && \
#         autoreconf -fiv && \
#         ./configure CFLAGS="-I${PREFIX}/include -fPIC" --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# # zimg  https://github.com/sekrit-twc/zimg
# RUN \
#         echo "Building zimg-${ZIMG_VERSION}" && \
#         DIR=/tmp/zimg && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sL https://github.com/sekrit-twc/zimg/archive/refs/tags/release-${ZIMG_VERSION}.tar.gz | \
#         tar -zx --strip-components=1 -f ../release-${ZIMG_VERSION}.tar.gz && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" --enable-shared  && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ### libtheora http://www.theora.org/ ( xiph )
# #             https://stackoverflow.com/questions/4810996/how-to-resolve-configure-guessing-build-type-failure
# RUN \
#         echo "Building libtheora-${THEORA_VERSION}" && \
#         DIR=/tmp/theora && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.gz && \
#         cp ../libtheora-${THEORA_VERSION}.tar.bz2 . && \
#         echo ${THEORA_SHA256SUM} | sha256sum --check && \
#         tar -zx --strip-components=1 -f libtheora-${THEORA_VERSION}.tar.gz && \
#         # add sym link for sdl-config
#         # ln -s /usr/bin/sdl2-config /usr/bin/sdl-config && \
#         # currently build does not find sdl-config, and thus no playback support is enabled (probably exacly, the way it was before)
#         # Note: consider installing doxygen so that the api documentation is built
#         #       right now, I did not, so we can keep everything small.
#         # disable examples to advoid the libjpeg sizeof error still in the example code.
#         ./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared --disable-examples && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libsrt https://github.com/Haivision/srt
# # RUN \
# #         echo "installing libsrt-dev with debian package: Secure Reliable Transport UDP streaming library (OpenSSL flavour)" && \
# #         apt-get install -yq libsrt1.5-openssl 
# # libsrt-openssl-dev
# RUN \
#         echo "Adding libssl-dev for libsrt build" && \
#         apt-get install -yq --no-install-recommends libssl-dev 
#         # Note: we can get the config error
#         #       GnuTLS('libgnutls28-dev') and OpenSSL('libssl-dev') must not be enabled at the same time, 
#         #       from a previous build
#         #       so we add libssl-dev and later in the build

#         ## libsrt https://github.com/Haivision/srt
# RUN \
#         echo "Building libsrt-${LIBSRT_VERSION}" && \
#         DIR=/tmp/srt && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/Haivision/srt/archive/refs/tags/v${LIBSRT_VERSION}.tar.gz && \
#         tar -xz --strip-components=1 -f ../srt-v${LIBSRT_VERSION}.tar.gz && \
#         cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . && \
#         make && \
#         make install && \
#         rm -rf ${DIR}



# ## libvmaf https://github.com/Netflix/vmaf
# # https://github.com/Netflix/vmaf/issues/788
# RUN \
#         if which meson || false; then \
#         echo "Building VMAF v${LIBVMAF_VERSION}" && \
#         DIR=/tmp/vmaf && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         # curl -sLO https://github.com/Netflix/vmaf/archive/refs/tags/v${LIBVMAF_VERSION}.tar.gz && \
#         tar -xz --strip-components=1 -f ../vmaf-v${LIBVMAF_VERSION}.tar.gz && \
#         ls -al && \
#         mkdir ./libvmaf/build && \
#         cd ./libvmaf/build && \
#         meson setup -Denable_tests=false -Denable_docs=false --buildtype=release --default-library=static .. --prefix "${PREFIX}" && \
#         ninja && \
#         ninja install && \
#         # meson build --buildtype release --prefix=${PREFIX} && \
#         # ninja -vC build && \
#         # ninja -vC build install && \
#         # mkdir -p ${PREFIX}/share/model/ && \
#         # cp -r /tmp/vmaf/model/* ${PREFIX}/share/model/ && \
#         rm -rf ${DIR}; \
#         else \
#         echo "VMAF skipped."; \
#         fi


# ## Download ffmpeg https://ffmpeg.org/
# RUN  \
#         echo "Building (intial) ffmpeg-${FFMPEG_VERSION}" && \
#         DIR=/tmp/ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
#         # curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
#         tar -jx --strip-components=1 -f ../ffmpeg-${FFMPEG_VERSION}.tar.bz2
# #         ./configure     --disable-debug  --disable-doc    --disable-ffplay   --enable-shared --enable-gpl  --extra-libs=-ldl && \
# #         make ;  make install



# ## Build ffmpeg https://ffmpeg.org/
# RUN  \
#         echo "Building (final) ffmpeg-${FFMPEG_VERSION}" && \
#         DIR=/tmp/ffmpeg && cd ${DIR} && \
#         export PKG_CONFIG_PATH=${PKG_CONFIG_PATH} && \
#         ./configure \
#         %  %  FFMPEG_CONFIG_FLAGS  %  % && \
#         make && \
#         make install && \
#         make tools/zmqsend && cp tools/zmqsend ${PREFIX}/bin/ && \
#         make distclean && \
#         hash -r && \
#         cd tools && \
#         make qt-faststart && cp qt-faststart ${PREFIX}/bin/



## cleanup
# This is used for both the source and packages version ( be robust about looking for libs to copy )
RUN \
        if ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | grep -q . ; then \
                ldd ${PREFIX}/bin/ffmpeg | grep x86_64-linux-gnu | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/; \
        fi && \
        if ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | grep -q . ; then \
                ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp -p {} /usr/local/lib/; \
        fi && \
        for lib in /usr/local/lib/*.so.*; do ln -sf "${lib##*/}" "${lib%%.so.*}".so; done && \
        cp ${PREFIX}/bin/* /usr/local/bin/ && \
        cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
        LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf && \
        cp -r ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include && \
        mkdir -p /usr/local/lib/pkgconfig && \
        for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc  ${PREFIX}/lib/pkgconfig/kvazaar.pc ${PREFIX}/lib/pkgconfig/libsw*.pc; do \
          sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"; \
        done

# # Stage 2: Final Image
FROM ubuntu:24.04
COPY --from=builder /usr/local /usr/local/

LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]

