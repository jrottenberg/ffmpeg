# ffmpeg - http://ffmpeg.org/download.html
#
# VERSION               2.8
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Centos
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#
FROM          centos:7
MAINTAINER    Julien Rottenberg <julien@rottenberg.info>


CMD           ["--help"]
ENTRYPOINT    ["ffmpeg"]
WORKDIR       /tmp/workdir


ENV           FFMPEG_VERSION=3.0 \
              YASM_VERSION=1.3.0   \
              OGG_VERSION=1.3.2    \
              VORBIS_VERSION=1.3.5 \
              THEORA_VERSION=1.1.1 \
              LAME_VERSION=3.99.5  \
              OPUS_VERSION=1.1.1   \
              FAAC_VERSION=1.28    \
              VPX_VERSION=1.5.0    \
              XVID_VERSION=1.3.4   \
              FDKAAC_VERSION=0.1.4 \
              X265_VERSION=1.9


# See https://github.com/jrottenberg/ffmpeg/blob/master/run.sh
COPY          run.sh /tmp/run.sh

RUN           /tmp/run.sh && ffmpeg -buildconf
# Let's make sure the app built correctly
# Convenient to verify on https://hub.docker.com/r/jrottenberg/ffmpeg/builds/ console output
