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

ENV         FFMPEG_VERSION=5.1.6

ARG         MAKEFLAGS="-j2"
ARG         PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"
ARG         PREFIX="/opt/ffmpeg"
ARG         LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"


ARG DEBIAN_FRONTEND=noninteractive
RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends curl jq python3 python3-requests less tree file && \
        chmod +x /tmp/workdir/download_tarballs.sh && \
        chmod +x /tmp/workdir/build_source.sh



RUN      buildDeps="autoconf \
                    automake \
                    cmake \
                    build-essential \
                    texinfo \
                    curl \
                    wget \
                    tar \
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
                    libdav1d-dev \
                    openssl \
                    libssl-dev \
                    expat \
                    libgomp1" && \
        apt-get -yqq update && \
        apt-get install -yq --no-install-recommends ${buildDeps}

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
