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

ENV FFMPEG_VERSION=7.1

ENV MAKEFLAGS="-j2"
ENV PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib/aarch64-linux-gnu/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"

ENV PREFIX="/opt/ffmpeg"
ENV LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64:/opt/ffmpeg/lib/aarch64-linux-gnu"


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
                    font-dejavu \
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

RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list ffmpeg-7.1
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# when  debugging you can pass in || true to the end of the command
# to keep the build going even if one of the steps fails
RUN /tmp/workdir/install_ffmpeg.sh


### Release Stage
FROM        alpine:3.20 AS release
# RUN         apk add --no-cache --update bash less tree file vim
# Copy fonts and fontconfig from builder
COPY        --from=builder /usr/share/fonts /usr/share/fonts
COPY        --from=builder /usr/share/fontconfig /usr/share/fontconfig
COPY        --from=builder /usr/bin/fc-* /usr/bin/

# Copy rest of the content
COPY        --from=builder /usr/local /usr/local
COPY        --from=builder /tmp/fakeroot/ /

LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["/bin/ffmpeg"]
