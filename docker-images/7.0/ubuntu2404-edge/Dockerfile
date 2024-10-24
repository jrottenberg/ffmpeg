# ffmpeg - http://ffmpeg.org/download.html
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#
# Stage 1: Build
FROM       ubuntu:24.04 AS builder
# FROM jsheffie/ffmpeg-devel:1.0 AS builder

WORKDIR     /tmp/workdir

COPY generate-source-of-truth-ffmpeg-versions.py /tmp/workdir
COPY download_tarballs.sh /tmp/workdir
COPY build_source.sh /tmp/workdir
COPY install_ffmpeg.sh /tmp/workdir

ENV FFMPEG_VERSION=7.0.2

# fribidi
ARG FRIBIDI_PKGS="libfribidi-dev libfribidi0"
# libass
ARG LIBASS_PKGS="libass-dev libass9"
# xorg-macros
ARG XORG_MACROS_PKGS="libxcb-shm0-dev libxcb-shm0 libxcb-xfixes0 libxcb-xfixes0-dev"
# libxau
ARG XAU_PKGS="libxau-dev libxau6"
# libpthread-stubs
ARG PTHREADS_STUBS_PKGS="libpthread-stubs0-dev"
# libxml2 ( started giving me download problems, so I went back to the debian package's version )
ARG XML2_PKGS="libxml2-dev libxml2"
# libpng
ARG PNG_PKGS="libpng-dev libpng16-16t64"

ENV MAKEFLAGS="-j2"
ENV PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib/aarch64-linux-gnu/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"
ENV PREFIX="/opt/ffmpeg"
ENV LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64:/opt/ffmpeg/lib/aarch64-linux-gnu"


ARG DEBIAN_FRONTEND=noninteractive
RUN     chmod +x /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py && \
        chmod +x /tmp/workdir/download_tarballs.sh && \
        chmod +x /tmp/workdir/build_source.sh && \
        chmod +x /tmp/workdir/install_ffmpeg.sh

RUN     apt-get -yqq update && \
        apt-get install -yq --no-install-recommends curl jq python3 python3-requests less tree file vim && \
        chmod +x /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py && \
        chmod +x /tmp/workdir/download_tarballs.sh && \
        chmod +x /tmp/workdir/build_source.sh && \
        chmod +x /tmp/workdir/install_ffmpeg.sh


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

# Note: pass '--library-list' to 'generate-source-of-truth-ffmpeg-versions.py'
#       ex: '--library-list lib1,lib2,lib3'
#  for more control over the build process, and how the docker layers are cached

# RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libopencore-amr,libx264,libx265,libogg,libopus,libvorbis,libvpx,libwebp,libmp3lame,libxvid,libfdk-aac,openjpeg,freetype,libvidstab,fribidi,fontconfig,libass,kvazaar,aom,libsvtav1,xorg-macros,xproto,libxau,libpthread-stubs,libxml2,libbluray,libzmq,libpng,libaribb24,zimg,libtheora,libsrt,libvmaf,ffmpeg
# dont do this 👆 where all of the libs are built at one time.
# by splitting them up into batches we allow docker to cache the layers ( which is a lifesaver when debugging )
# I left this line in here, as it shows the proper order of the libraries that need to be built. ( what worked )
# there are only a few build deps. I remember that libtheora needed libogg.

RUN \
        echo "Installing dependencies..." && \
        apt-get install -yq --no-install-recommends ${FRIBIDI_PKGS} ${LIBASS_PKGS} ${XORG_MACROS_PKGS} ${XAU_PKGS} ${PTHREADS_STUBS_PKGS} ${XML2_PKGS} ${PNG_PKGS}


# First batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
libopencore-amr,\
libx264,\
libx265,\
libogg,\
libopus
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh


#  additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
libvorbis,\
libvpx,\
libwebp,\
libmp3lame
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libxvid
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
libfdk-aac,\
openjpeg,\
freetype,\
libvidstab
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list fontconfig
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list kvazaar
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
aom,\
libsvtav1
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list xproto
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh


# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
libbluray,\
libzmq
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
libaribb24,\
zimg,\
libtheora
# Note: libtheora is dependant on libogg
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list \
libsrt,\
libvmaf
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# This is a slow one, put it on its own container layer to speed up the build (allowing it to be cached)
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list ffmpeg
## when  debugging you can pass in || true to the end of the next 3 commands
## to keep the build going even if one of the steps fails
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

RUN /tmp/workdir/install_ffmpeg.sh



# Stage 2: Final Image ( shrink the size back down )
FROM ubuntu:24.04
COPY --from=builder /usr/local /usr/local/

LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]
