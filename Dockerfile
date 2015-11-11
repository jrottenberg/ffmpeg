# ffmpeg
#
# VERSION               2.8.1-1
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
FROM          centos:7
MAINTAINER    Julien Rottenberg <julien@rottenberg.info>


ENV           FFMPEG_VERSION=2.8.1 \
              MPLAYER_VERSION=1.2  \
              YASM_VERSION=1.3.0   \
              OGG_VERSION=1.3.2    \
              VORBIS_VERSION=1.3.5 \
              THEORA_VERSION=1.1.1 \
              LAME_VERSION=3.99.5  \
              OPUS_VERSION=1.1     \
              FAAC_VERSION=1.28    \
              VPX_VERSION=1.4.0    \
              XVID_VERSION=1.3.4   \
              FDKAAC_VERSION=0.1.4 \
              X265_VERSION=1.8


WORKDIR       /tmp/workdir

# See https://github.com/jrottenberg/ffmpeg/blob/master/run.sh
COPY          run.sh /tmp/run.sh
RUN           /tmp/run.sh

# Let's make sure the app built correctly
RUN           ffmpeg -buildconf


CMD           ["--help"]
ENTRYPOINT    ["ffmpeg"]
