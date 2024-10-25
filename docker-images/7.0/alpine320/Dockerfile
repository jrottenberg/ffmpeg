# ffmpeg - http://ffmpeg.org/download.html
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#

FROM        alpine:3.20 AS builder

RUN         apk add --no-cache --update libgcc libstdc++ ca-certificates openssl expat git less tree file vim bash

WORKDIR     /tmp/workdir

COPY        generate-source-of-truth-ffmpeg-versions.py /tmp/workdir
COPY        download_tarballs.sh /tmp/workdir
COPY        build_source.sh /tmp/workdir
COPY        install_ffmpeg.sh /tmp/workdir

RUN         chmod +x /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py && \
            chmod +x /tmp/workdir/download_tarballs.sh && \
            chmod +x /tmp/workdir/build_source.sh && \
            chmod +x /tmp/workdir/install_ffmpeg.sh

ENV         ENV MAKEFLAGS="-j2"
ENV PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib/aarch64-linux-gnu/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"

ENV PREFIX="/opt/ffmpeg"
ENV LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64:/opt/ffmpeg/lib/aarch64-linux-gnu"


# FFMPEG_VERSION=7.0.2 \
#     LIBVMAF_VERSION=2.3.1 \
#     KVAZAAR_VERSION=2.0.0 \
#     LIBPTHREAD_STUBS_VERSION=0.4 \
#     LIBBLURAY_VERSION=1.1.2 \
#     LIBARIBB24_VERSION=1.0.3 \

# ARG         LIBARIBB24_SHA256SUM="f61560738926e57f9173510389634d8c06cabedfa857db4b28fb7704707ff128 v1.0.3.tar.gz"

# ARG         MAKEFLAGS="-j2"
# ARG         PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig"
# ARG         PREFIX="/opt/ffmpeg"
# ARG         LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64"


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
                    # https://www.x.org/archive/individual/proto/
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
                    zimg-dev \
                    dav1d \
                    libdav1d \
                    dav1d-dev \
                    svt-av1 \
                    svt-av1-dev \
                    libSvtAv1Enc \
                    libSvtAv1Dec" && \
            apk add --no-cache --update ${libDeps}


RUN     buildDeps="autoconf \
                   automake \
                   bash \
                   binutils \
                   bzip2 \
                   cmake \
                   coreutils \
                   curl \
                   wget \
                   jq \
                   diffutils \
                   expat-dev \
                   file \
                   g++ \
                   gcc \
                   gperf \
                   libtool \
                   make \
                   meson \
                   ninja-build \
                   nasm \
                   openssl-dev \
                   python3 \
                   tar \
                   xz \
                   xcb-proto \
                   yasm \
                   zlib-dev \
                   alpine-sdk \
                   linux-headers" && \
        apk add --no-cache --update ${buildDeps}
# Note: pass '--library-list lib1,lib2,lib3 for more control.
#       Here we have 3 libs that we have to build from source
# vmaf
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list kvazaar,libvmaf
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# # libevent && libevent-dev has usr/lib/libevent_pthreads ???
# ## libbluray - Requires libxml, freetype, and fontconfig
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libpthread-stubs,libbluray,libaribb24
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list ffmpeg
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh || true

## when  debugging you can pass in || true to the end of the command
## to keep the build going even if one of the steps fails
RUN /tmp/workdir/install_ffmpeg.sh || true


# ## libvmaf https://github.com/Netflix/vmaf
# RUN \
#         if which meson || false; then \
#         echo "Building VMAF." && \
#         DIR=/tmp/vmaf && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         curl -sLO https://github.com/Netflix/vmaf/archive/v${LIBVMAF_VERSION}.tar.gz && \
#         tar -xz --strip-components=1 -f v${LIBVMAF_VERSION}.tar.gz && \
#         cd /tmp/vmaf/libvmaf && \
#         meson build --buildtype release --prefix=${PREFIX} && \
#         ninja -vC build && \
#         ninja -vC build install && \
#         mkdir -p ${PREFIX}/share/model/ && \
#         cp -r /tmp/vmaf/model/* ${PREFIX}/share/model/ && \
#         rm -rf ${DIR}; \
#         else \
#         echo "VMAF skipped."; \
#         fi

# ## kvazaar https://github.com/ultravideo/kvazaar
# RUN \
#         DIR=/tmp/kvazaar && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         curl -sLO https://github.com/ultravideo/kvazaar/archive/v${KVAZAAR_VERSION}.tar.gz && \
#         tar -zx --strip-components=1 -f v${KVAZAAR_VERSION}.tar.gz && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# # libevent && libevent-dev has usr/lib/libevent_pthreads ???
# RUN \
#         DIR=/tmp/libpthread-stubs && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         curl -sLO https://xcb.freedesktop.org/dist/libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}.tar.gz && \
#         tar -zx --strip-components=1 -f libpthread-stubs-${LIBPTHREAD_STUBS_VERSION}.tar.gz && \
#         ./configure --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}


# ## libbluray - Requires libxml, freetype, and fontconfig
# RUN \
#         DIR=/tmp/libbluray && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         curl -sLO https://download.videolan.org/pub/videolan/libbluray/${LIBBLURAY_VERSION}/libbluray-${LIBBLURAY_VERSION}.tar.bz2 && \
#         echo ${LIBBLURAY_SHA256SUM} | sha256sum --check && \
#         tar -jx --strip-components=1 -f libbluray-${LIBBLURAY_VERSION}.tar.bz2 && \
#         ./configure --prefix="${PREFIX}" --disable-examples --disable-bdjava-jar --disable-static --enable-shared && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## libaribb24
# RUN \
#         DIR=/tmp/b24 && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         curl -sLO https://github.com/nkoriyama/aribb24/archive/v${LIBARIBB24_VERSION}.tar.gz && \
#         echo ${LIBARIBB24_SHA256SUM} | sha256sum --check && \
#         tar -xz --strip-components=1 -f v${LIBARIBB24_VERSION}.tar.gz && \

#         autoreconf -fiv && \
#         ./configure CFLAGS="-I${PREFIX}/include -fPIC" --prefix="${PREFIX}" && \
#         make && \
#         make install && \
#         rm -rf ${DIR}

# ## Download ffmpeg https://ffmpeg.org/
# RUN  \
#         DIR=/tmp/ffmpeg && mkdir -p ${DIR} && cd ${DIR} && \
#         curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
#         tar -jx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.bz2
#         # ./configure     --disable-debug  --disable-doc    --disable-ffplay   --enable-shared --enable-gpl  --extra-libs=-ldl && \
#         # make ;  make install


# # ## Build ffmpeg https://ffmpeg.org/
# RUN  \
#         DIR=/tmp/ffmpeg && cd ${DIR} && \
#         ./configure \
#         % % FFMPEG_CONFIG_FLAGS % % && \
#         make clean && \
#         make && \
#         make install && \
#         make tools/zmqsend && cp tools/zmqsend ${PREFIX}/bin/ && \
#         make distclean && \
#         hash -r && \
#         cd tools && \
#         make qt-faststart && cp qt-faststart ${PREFIX}/bin/


# RUN \
#     ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp {} /usr/local/lib/ && \
#     for lib in /usr/local/lib/*.so.*; do ln -sf "${lib##*/}" "${lib%%.so.*}".so; done && \
#     cp ${PREFIX}/bin/* /usr/local/bin/ && \
#     cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ && \
#     LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf && \
#     mkdir -p /usr/local/include && \
#     cp -r ${PREFIX}/include/libav* ${PREFIX}/include/libpostproc ${PREFIX}/include/libsw* /usr/local/include && \
#     mkdir -p /usr/local/lib/pkgconfig && \
#     for pc in ${PREFIX}/lib/pkgconfig/libav*.pc ${PREFIX}/lib/pkgconfig/libpostproc.pc ${PREFIX}/lib/pkgconfig/libsw*.pc; do \
#         sed "s:${PREFIX}:/usr/local:g" <"$pc" >/usr/local/lib/pkgconfig/"${pc##*/}"; \
#     done

### Release Stage
# FROM        alpine:3.20 AS release
# RUN         apk add --no-cache --update bash less tree file vim
# COPY        --from=builder /usr/local /usr/local

LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]
