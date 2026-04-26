# ffmpeg - http://ffmpeg.org/download.html
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#

FROM        alpine:3.20 AS builder

RUN         apk add --no-cache --update libgcc libstdc++ ca-certificates openssl expat git libgomp less tree file vim bash
# apt-get install -yq --no-install-recommends curl jq python3 python3-requests less tree file vim && \


ENV FFMPEG_VERSION=8.0.1

ENV MAKEFLAGS="-j2"
ENV PKG_CONFIG_PATH="/opt/ffmpeg/share/pkgconfig:/opt/ffmpeg/lib/pkgconfig:/opt/ffmpeg/lib64/pkgconfig:/opt/ffmpeg/lib/x86_64-linux-gnu/pkgconfig:/opt/ffmpeg/lib/aarch64-linux-gnu/pkgconfig:/usr/lib/x86_64-linux-gnu/pkgconfig:/usr/lib/pkgconfig"

ENV PREFIX="/opt/ffmpeg"
ENV LD_LIBRARY_PATH="/opt/ffmpeg/lib:/opt/ffmpeg/lib64:/opt/ffmpeg/lib/aarch64-linux-gnu"



RUN     buildDeps="autoconf \
                   automake \
                   bash \
                   binutils \
                   bzip2 \
                   cmake \
                   coreutils \
                   curl \
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
                   bzip2 \
                   xcb-proto \
                   yasm \
                   zlib-dev \
                   alpine-sdk \
                   linux-headers\
                   ## https://www.fribidi.org/
                   fribidi \
                   fribidi-static \
                   fribidi-dev\
                   font-dejavu \
                   # https://github.com/libass/libass
                   libass \
                   libass-dev\
                   # https://www.x.org/archive/individual/proto/
                   xorgproto \
                   # https://git.code.sf.net/p/libpng/code
                   libpng \
                   libpng-static \
                   libpng-utils \
                   libpng-dev\
                   dav1d \
                   libdav1d \
                   dav1d-dev" && \
        apk add --no-cache --update ${buildDeps}

WORKDIR     /tmp/workdir

COPY        generate-source-of-truth-ffmpeg-versions.py /tmp/workdir
COPY        download_tarballs.sh /tmp/workdir
COPY        build_source.sh /tmp/workdir
COPY        install_ffmpeg.sh /tmp/workdir

# Note: pass '--library-list' to 'generate-source-of-truth-ffmpeg-versions.py'
#       ex: '--library-list lib1,lib2,lib3'
#  for more control over the build process, and how the docker layers are cached

# RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libopencore-amr,libx264,libx265,libogg,libopus,libvorbis,libvpx,libwebp,libmp3lame,libxvid,libfdk-aac,openjpeg,freetype,libvidstab,fribidi,fontconfig,libass,kvazaar,aom,libsvtav1,xorg-macros,xproto,libxau,libpthread-stubs,libxml2,libbluray,libzmq,libpng,libaribb24,zimg,libtheora,libsrt,libvmaf,ffmpeg
# dont do this 👆 where all of the libs are built at one time.
# by splitting them up into batches we allow docker to cache the layers ( which is a lifesaver when debugging )
# I left this line in here, as it shows the proper order of the libraries that need to be built. ( what worked )
# there are only a few build deps. I remember that libtheora needed libogg.

# RUN \
#         echo "Installing dependencies..." && \
#         apt-get install -yq --no-install-recommends ${FRIBIDI_PKGS} ${LIBASS_PKGS} ${XORG_MACROS_PKGS} ${XAU_PKGS} ${XML2_PKGS} ${PNG_PKGS}
# apt-get install -yq --no-install-recommends ${FRIBIDI_PKGS} ${LIBASS_PKGS} ${XORG_MACROS_PKGS} ${XAU_PKGS} ${PTHREADS_STUBS_PKGS} ${XML2_PKGS} ${PNG_PKGS}


# First batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libopencore-amr,libx264,libx265,libogg,libopus
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh


#  additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libvorbis,libvpx,libwebp,libmp3lame
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libxvid,libpthread-stubs
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libfdk-aac,openjpeg,freetype,libvidstab
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
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list whisper
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list aom,xorg-macros,libsvtav1
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
# note: took out 'xproto' because of the configure.guess error
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libxau
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh


# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libxml2,libbluray,libzmq
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libaribb24,zimg
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libtheora
# Note: libtheora is dependant on libogg
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# # additional batch of libraries ( split into docker layers, to allow for caching )
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list libsrt,libvmaf
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# This is a slow one, put it on its own container layer to speed up the build (allowing it to be cached)
RUN /tmp/workdir/generate-source-of-truth-ffmpeg-versions.py --library-list ffmpeg-8.0
## when  debugging you can pass in || true to the end of the next 3 commands
## to keep the build going even if one of the steps fails
RUN /tmp/workdir/download_tarballs.sh
RUN /tmp/workdir/build_source.sh

# TODO add a strip and fakeroot argument
RUN /tmp/workdir/install_ffmpeg.sh --strip


### Release Stage
FROM        alpine:3.20 AS release
# RUN         apk add --no-cache --update bash less tree file vim
# Copy fonts and fontconfig from builder
COPY        --from=builder /usr/share/fonts /usr/share/fonts
COPY        --from=builder /usr/share/fontconfig /usr/share/fontconfig
# Probably don't want the fc-* utilities in the scratch image
# COPY        --from=builder /usr/bin/fc-* /usr/bin/

# Copy rest of the content
COPY        --from=builder /usr/local /usr/local
COPY        --from=builder /tmp/fakeroot/ /

LABEL       org.opencontainers.image.authors="julien@rottenberg.info" \
            org.opencontainers.image.source=https://github.com/jrottenberg/ffmpeg

ENV         LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64

CMD         ["--help"]
ENTRYPOINT  ["/bin/ffmpeg"]
