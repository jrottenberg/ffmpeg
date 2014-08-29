# ffmpeg
#
# VERSION               0.0.1
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
FROM          centos:centos6
MAINTAINER    Julien Rottenberg <julien@rottenberg.info>



RUN           yum install -y  --disableplugin=fastestmirror autoconf automake gcc gcc-c++ git libtool make nasm pkgconfig zlib-devel tar bzip2


ENV           FFMPEG_VERSION 2.3.3
ENV           YASM_VERSION   1.2.0
ENV           LAME_VERSION   3.99.5


ENV           SRC            /opt/src



RUN           mkdir ${SRC}



# yasm
RUN           cd ${SRC} && \
              curl -O http://www.tortall.net/projects/yasm/releases/yasm-${YASM_VERSION}.tar.gz && \
              tar xzvf yasm-${YASM_VERSION}.tar.gz && \
              cd yasm-${YASM_VERSION} && \
              ./configure --prefix="$SRC" --bindir="/usr/local/bin" && \
              make && \
              make install && \
              make distclean

# x264
RUN           cd ${SRC} && \
              git clone --depth 1 git://git.videolan.org/x264 && \
              cd x264 && \
              ./configure --prefix="$SRC" --bindir="/usr/local/bin" --enable-static && \
              make && \
              make install && \
              make distclean

# libmp3lame
RUN           cd ${SRC} && \
              curl -L -O http://downloads.sourceforge.net/project/lame/lame/${LAME_VERSION%.*}/lame-${LAME_VERSION}.tar.gz  && \
              tar xzvf lame-${LAME_VERSION}.tar.gz  && \
              cd lame-${LAME_VERSION} && \
              ./configure --prefix="${SRC}" --bindir="/usr/local/bin" --disable-shared --enable-nasm && \
              make && \
              make install && \
              make distclean


# ffmpeg
RUN           cd ${SRC} && \
              curl -O http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2 && \
              tar xjvf ffmpeg-${FFMPEG_VERSION}.tar.bz2

RUN           cd ${SRC}/ffmpeg-${FFMPEG_VERSION} && \
              PKG_CONFIG_PATH="${SRC}/lib/pkgconfig" && \
              export PKG_CONFIG_PATH && \
              ./configure --prefix="${SRC}" --extra-cflags="-I${SRC}/include" --extra-ldflags="-L${SRC}/lib" --bindir="/usr/local/bin" \
              --extra-libs=-ldl --enable-version3 --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-libxvid --enable-gpl \
              --enable-postproc --enable-nonfree --enable-avresample && \
              make && \
              make install && \
              make distclean && \
              hash -r


RUN           ls -lsa               /usr/local/bin ${SRC}
RUN           /usr/local/bin/ffmpeg
