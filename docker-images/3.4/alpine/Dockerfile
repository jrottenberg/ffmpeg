FROM alpine:3.7 as base

WORKDIR /tmp/workdir

RUN set -e ; \
apk add --no-cache --update libgcc libstdc++ ca-certificates libcrypto1.0 libssl1.0 libgomp expat freetype fontconfig fribidi

FROM base AS build

ARG PKG_CONFIG_PATH='/opt/ffmpeg/lib/pkgconfig'
ARG LD_LIBRARY_PATH='/opt/ffmpeg/lib'
ARG PREFIX='/opt/ffmpeg'
ARG MAKEFLAGS='-j2'

ENV FFMPEG_VERSION=3.4.2 \
	FFMPEG_GPG=FCF986EA15E6E293A5644F10B4322F04D67658D8 \
	    SRC=/usr/local

RUN set -e ;\
apk add --no-cache --update autoconf automake binutils bzip2 cmake curl coreutils expat-dev file fontconfig-dev freetype-dev fribidi-dev g++ gcc gnupg gperf libtool make nasm openssl-dev python tar yasm zlib-dev


ARG OGG_SHA256SUM=e19ee34711d7af328cb26287f4137e70630e7261b17cbe3cd41011d73a654692
ARG OGG_VERSION=1.3.2
RUN set -e; \
dir=/tmp/ogg ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO http://downloads.xiph.org/releases/ogg/libogg-${OGG_VERSION}.tar.gz ; \
echo "${OGG_SHA256SUM}  libogg-${OGG_VERSION}.tar.gz" | sha256sum --check ; \
tar -zx --strip-components=1 -f libogg-${OGG_VERSION}.tar.gz ; \
./configure --prefix="${PREFIX}" --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir} 



ARG OPENCOREAMR_SHA1SUM=bef4d1e3a8a155b47569b6691a223843b33e279e
ARG OPENCOREAMR_VERSION=0.1.5 
RUN set -e; \
dir=/tmp/opencore-amr ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO https://10gbps-io.dl.sourceforge.net/project/opencore-amr/opencore-amr/opencore-amr-${OPENCOREAMR_VERSION}.tar.gz ; \
echo "${OPENCOREAMR_SHA1SUM}  opencore-amr-${OPENCOREAMR_VERSION}.tar.gz" | \
sha1sum --check ; \
tar -zx --strip-components=1 -f opencore-amr-${OPENCOREAMR_VERSION}.tar.gz ; \
./configure --prefix="${PREFIX}" --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir} 



ARG OPUS_SHA256SUM=cfafd339ccd9c5ef8d6ab15d7e1a412c054bf4cb4ecbbbcc78c12ef2def70732
ARG OPUS_VERSION=1.2.1
RUN set -e; \
dir=/tmp/opus ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO https://archive.mozilla.org/pub/opus/opus-${OPUS_VERSION}.tar.gz ; \
echo "${OPUS_SHA256SUM}  opus-${OPUS_VERSION}.tar.gz" | sha256sum --check  ; \
tar -zx --strip-components=1 -f opus-${OPUS_VERSION}.tar.gz ; \
autoreconf -fiv ; \
./configure --prefix="${PREFIX}" --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir} 



ARG X264_VERSION=20180210-2245-stable
RUN set -e ;\
dir=/tmp/x264 ;\
mkdir -p ${dir} ;\
cd ${dir} ;\
curl -sL https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-${X264_VERSION}.tar.bz2 | tar -jx --strip-components=1 ; \
./configure --prefix="${PREFIX}" --enable-shared --enable-pic --disable-cli ; \
make ; \
make install ; \
rm -rf ${dir}



ARG X265_MD5SUM=4d318be1f19b58985432a144bd054572
ARG X265_VERSION=2.6
RUN set -e; \
dir=/tmp/x265 ; \
mkdir -p ${dir} ; \
curl -sLO https://download.videolan.org/pub/videolan/x265/x265_${X265_VERSION}.tar.gz ; \
echo "${X265_MD5SUM}  x265_${X265_VERSION}.tar.gz" | md5sum --check ; \
tar -zx --strip-component=1 -f x265_${X265_VERSION}.tar.gz ; \
cd build/linux ; \
sed -i "/-DEXTRA_LIB/ s/$/ -DCMAKE_INSTALL_PREFIX=\${PREFIX}/" multilib.sh ; \
sed -i "/^cmake/ s/$/ -DENABLE_CLI=OFF/" multilib.sh ; \
./multilib.sh ; \
make -C 8bit install ; \
rm -rf ${dir}



ARG OPENJPEG_VERSION=2.2.0
RUN set -e; \
dir=/tmp/openjpeg ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sL https://github.com/uclouvain/openjpeg/archive/v${OPENJPEG_VERSION}.tar.gz | \
tar -zx --strip-components=1 ; \
cmake -DBUILD_THIRDPARTY:BOOL=ON -DCMAKE_INSTALL_PREFIX="${PREFIX}" . ; \
make ; \
make install ; \
rm -rf ${dir}



ARG FDKAAC_VERSION=0.1.5
RUN set -e; \
dir=/tmp/fdkaac ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sL https://github.com/mstorsjo/fdk-aac/archive/v${FDKAAC_VERSION}.tar.gz | \
tar -zx --strip-components=1 ; \
autoreconf -fiv ; \
./configure --prefix="${PREFIX}" --enable-shared --datadir="${PWD}" ; \
make ; \
make install ; \
rm -rf ${dir}


	
ARG LAME_VERSION=3.100
RUN set -e; \
dir=/tmp/lame ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sL https://10gbps-io.dl.sourceforge.net/project/lame/lame/$(echo ${LAME_VERSION} | sed -E 's/([0-9]+\.[0-9]+)/\1/')/lame-${LAME_VERSION}.tar.gz | \
tar -zx --strip-components=1 ; \
./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --enable-shared --enable-nasm --enable-pic --disable-frontend ; \
make ; \
make install ; \
rm -rf ${dir}



ARG ASS_SHA256SUM=8fadf294bf701300d4605e6f1d92929304187fca4b8d8a47889315526adbafd7
ARG ASS_VERSION=0.13.7
RUN set -e; \
dir=/tmp/ass ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO https://github.com/libass/libass/archive/${ASS_VERSION}.tar.gz ; \
echo "${ASS_SHA256SUM}  ${ASS_VERSION}.tar.gz" | sha256sum --check  ; \
tar -zx --strip-components=1 -f ${ASS_VERSION}.tar.gz ; \
./autogen.sh ; \
./configure -prefix="${PREFIX}" --disable-static --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir}


    
ARG THEORA_SHA256SUM=40952956c47811928d1e7922cda3bc1f427eb75680c3c37249c91e949054916b
ARG THEORA_VERSION=1.1.1
RUN set -e; \
dir=/tmp/theora ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO http://downloads.xiph.org/releases/theora/libtheora-${THEORA_VERSION}.tar.gz ; \
echo "${THEORA_SHA256SUM}  libtheora-${THEORA_VERSION}.tar.gz"| sha256sum --check ; \
tar -zx --strip-components=1 -f libtheora-${THEORA_VERSION}.tar.gz ; \
sed -i 's/png_\(sizeof\)/\1/g' examples/png2theora.c ; \
./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir}


    
ARG VORBIS_SHA256SUM=6efbcecdd3e5dfbf090341b485da9d176eb250d893e3eb378c428a2db38301ce
ARG VORBIS_VERSION=1.3.5
RUN set -e; \
dir=/tmp/vorbis ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO http://downloads.xiph.org/releases/vorbis/libvorbis-${VORBIS_VERSION}.tar.gz ; \
echo "${VORBIS_SHA256SUM}  libvorbis-${VORBIS_VERSION}.tar.gz" | sha256sum --check  ; \
tar -zx --strip-components=1 -f libvorbis-${VORBIS_VERSION}.tar.gz ; \
./configure --prefix="${PREFIX}" --with-ogg="${PREFIX}" --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir}


	
ARG VPX_VERSION=1.6.1
RUN set -e; \
dir=/tmp/vpx ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sL https://codeload.github.com/webmproject/libvpx/tar.gz/v${VPX_VERSION} | \
tar -zx --strip-components=1 ; \
./configure --prefix="${PREFIX}" --enable-vp8 --enable-vp9 --enable-pic --enable-shared \
--disable-debug --disable-examples --disable-docs --disable-install-bins ; \
make ; \
make install ; \
rm -rf ${dir}


    
ARG XVID_SHA256SUM=4e9fd62728885855bc5007fe1be58df42e5e274497591fec37249e1052ae316f
ARG XVID_VERSION=1.3.4
RUN set -e; \
dir=/tmp/xvid ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO http://downloads.xvid.org/downloads/xvidcore-${XVID_VERSION}.tar.gz ; \
echo "${XVID_SHA256SUM}  xvidcore-${XVID_VERSION}.tar.gz" | sha256sum --check ; \
tar -zx -f xvidcore-${XVID_VERSION}.tar.gz ; \
cd xvidcore/build/generic ; \
./configure --prefix="${PREFIX}" --bindir="${PREFIX}/bin" --datadir="${PWD}" --enable-shared --enable-shared ; \
make ; \
make install ; \
rm -rf ${dir}



ARG VIDSTAB_SHA256SUM=14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb
ARG VIDSTAB_VERSION=1.1.0
RUN set -e; \
dir=/tmp/vidstab ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO https://github.com/georgmartius/vid.stab/archive/v${VIDSTAB_VERSION}.tar.gz ; \
echo "${VIDSTAB_SHA256SUM}  v${VIDSTAB_VERSION}.tar.gz" | sha256sum --check  ; \
tar -zx --strip-components=1 -f v${VIDSTAB_VERSION}.tar.gz ; \
cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" . ; \
make ; \
make install ; \
rm -rf ${dir}



ARG KVAZAAR_VERSION=1.2.0
RUN set -e; \
dir=/tmp/kvazaar ; \
mkdir -p ${dir} ; \
cd ${dir} ; \
curl -sLO https://github.com/ultravideo/kvazaar/archive/v${KVAZAAR_VERSION}.tar.gz &&\
tar -zx --strip-components=1 -f v${KVAZAAR_VERSION}.tar.gz && \
./autogen.sh && \
./configure -prefix="${PREFIX}" --disable-static --enable-shared && \
make && \
make install ; \
rm -rf ${dir}


RUN  set -e ;\
dir=$(mktemp -d) ;\
cd ${dir} ; \
curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz ; \
curl -sLO https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz.asc ; \
gpg --batch --keyserver ipv4.pool.sks-keyservers.net --recv-keys ${FFMPEG_GPG}; \
gpg --batch --verify ffmpeg-3.4.2.tar.gz.asc ffmpeg-${FFMPEG_VERSION}.tar.gz ; \
tar -zx --strip-components=1 -f ffmpeg-${FFMPEG_VERSION}.tar.gz ; \
./configure \
--disable-debug \
--disable-doc \
--disable-ffplay \
--enable-shared \
--enable-avresample \
--enable-gpl \
--enable-nonfree \
--enable-postproc \
--enable-small \
--enable-version3 \
--enable-libfreetype \
--enable-libopencore-amrnb --enable-libopencore-amrwb \
--enable-libopus \
--enable-libx264 \
--enable-libx265 \
--enable-libass \
--enable-libvidstab \
--enable-libmp3lame \
--enable-libopenjpeg \
--enable-libtheora \
--enable-libvorbis \
--enable-libvpx \
--enable-libxvid \
--enable-libfdk_aac \
--enable-libkvazaar \
--extra-cflags="-I${PREFIX}/include" \
--extra-ldflags="-L${PREFIX}/lib" \
--extra-libs=-ldl \
--prefix="${PREFIX}" ; \
make ; \
make install ; \
make distclean ; \
hash -r ; \
cd tools ; \
make qt-faststart ; \
cp qt-faststart ${PREFIX}/bin

RUN set -e ;\
ldd ${PREFIX}/bin/ffmpeg | grep opt/ffmpeg | cut -d ' ' -f 3 | xargs -i cp {} /usr/local/lib/ ; \
cp ${PREFIX}/bin/* /usr/local/bin/ ; \
cp -r ${PREFIX}/share/ffmpeg /usr/local/share/ ; \
LD_LIBRARY_PATH=/usr/local/lib ffmpeg -buildconf



FROM        base

CMD         ["--help"]
ENTRYPOINT  ["ffmpeg"]

ENV         LD_LIBRARY_PATH=/usr/local/lib

COPY --from=build /usr/local /usr/local/



