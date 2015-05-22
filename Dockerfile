# ffmpeg
#
# VERSION               2.6.3-1
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
FROM          centos:centos6
MAINTAINER    Julien Rottenberg <julien@rottenberg.info>





ENV           FFMPEG_VERSION  2.6.3
ENV           MPLAYER_VERSION 1.1.1
ENV           YASM_VERSION    1.3.0
ENV           OGG_VERSION     1.3.2
ENV           VORBIS_VERSION  1.3.4
ENV           LAME_VERSION    3.99.5
ENV           FAAC_VERSION    1.28
ENV           XVID_VERSION    1.3.3
ENV           FDKAAC_VERSION  0.1.3
ENV           SRC             /usr/local
ENV           LD_LIBRARY_PATH ${SRC}/lib
ENV           PKG_CONFIG_PATH ${SRC}/lib/pkgconfig



COPY          run.sh /tmp/run.sh

# See https://github.com/jrottenberg/ffmpeg/blob/master/run.sh
RUN           bash /tmp/run.sh

# Let's make sure the app built correctly
RUN           ffmpeg -buildconf 

WORKDIR /tmp/workdir

CMD           ["--help"]
ENTRYPOINT    ["ffmpeg"]
