# ffmpeg
#
# VERSION               2.8.1-1
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
FROM          centos:7
MAINTAINER    Julien Rottenberg <julien@rottenberg.info>


ENV           FFMPEG_VERSION  2.8.1
ENV           MPLAYER_VERSION 1.2
ENV           YASM_VERSION    1.3.0
ENV           OGG_VERSION     1.3.2
ENV           VORBIS_VERSION  1.3.5
ENV           LAME_VERSION    3.99.5
ENV           OPUS_VERSION    1.1
ENV           FAAC_VERSION    1.28
ENV           VPX_VERSION     1.4.0
ENV           XVID_VERSION    1.3.4
ENV           FDKAAC_VERSION  0.1.4
ENV           X265_VERSION    1.8


WORKDIR       /tmp/workdir

# See https://github.com/jrottenberg/ffmpeg/blob/master/run.sh
COPY          run.sh /tmp/run.sh
RUN           /tmp/run.sh

# Let's make sure the app built correctly
RUN           ffmpeg -buildconf


CMD           ["--help"]
ENTRYPOINT    ["ffmpeg"]
