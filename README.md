FFMPEG for Docker on Centos7
============================

[![Image Size](https://img.shields.io/imagelayers/image-size/jrottenberg/ffmpeg/latest.svg?style=plastic)](https://imagelayers.io/?images=jrottenberg%2Fffmpeg:latest) [![Image Layers](https://img.shields.io/imagelayers/layers/jrottenberg/ffmpeg/latest.svg?style=plastic)](https://imagelayers.io/?images=jrottenberg%2Fffmpeg:latest) [![Docker Stars](https://img.shields.io/docker/stars/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/stars/count/) [![Docker pulls](https://img.shields.io/docker/pulls/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/)
[![Travis](https://img.shields.io/travis/jrottenberg/ffmpeg.svg?maxAge=300?style=plastic)](https://travis-ci.org/jrottenberg/ffmpeg)

This project prepares a minimalist Docker image with FFMPEG. It compiles FFMPEG from sources following instructions from the [Centos Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can be used as a base for an encoding farm, based on centos7.

Ubuntu builds
--------------

You can use jrottenberg/ffmpeg:ubuntu or  jrottenberg/ffmpeg:3.1-ubuntu
to get the latest build based on ubuntu.

Note : I'll make ubuntu the default after 3.1
ie you'll find centos based image using jrottenberg/ffmpeg:3.x-centos

```
ffmpeg                                                      ubuntu              571384c84090        12 hours ago        289.3 MB
ffmpeg                                                      centos              4478825e57ee        8 weeks ago         341 MB
```


Please use [Github issues](https://github.com/jrottenberg/ffmpeg/issues/new) to report any bug or missing feature.

Test
----

```
ffmpeg version 3.0 Copyright (c) 2000-2016 the FFmpeg developers
  built with gcc 4.8.5 (GCC) 20150623 (Red Hat 4.8.5-4)
  configuration: --prefix=/usr/local --extra-cflags=-I/usr/local/include --extra-ldflags=-L/usr/local/lib --bindir=/usr/local/bin --extra-libs=-ldl --enable-version3 --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-libxvid --enable-gpl --enable-postproc --enable-nonfree --enable-avresample --enable-libfdk_aac --disable-debug --enable-small --enable-openssl --enable-libtheora --enable-libx265 --enable-libopus --enable-libvorbis --enable-libvpx
  libavutil      55. 17.103 / 55. 17.103
  libavcodec     57. 24.102 / 57. 24.102
  libavformat    57. 25.100 / 57. 25.100
  libavdevice    57.  0.101 / 57.  0.101
  libavfilter     6. 31.100 /  6. 31.100
  libavresample   3.  0.  0 /  3.  0.  0
  libswscale      4.  0.100 /  4.  0.100
  libswresample   2.  0.101 /  2.  0.101
  libpostproc    54.  0.100 / 54.  0.100

  configuration:
    --prefix=/usr/local
    --extra-cflags=-I/usr/local/include
    --extra-ldflags=-L/usr/local/lib
    --bindir=/usr/local/bin
    --extra-libs=-ldl
    --enable-version3
    --enable-libfaac
    --enable-libmp3lame
    --enable-libx264
    --enable-libxvid
    --enable-gpl
    --enable-postproc
    --enable-nonfree
    --enable-avresample
    --enable-libfdk_aac
    --disable-debug
    --enable-small
    --enable-openssl
    --enable-libtheora
    --enable-libx265
    --enable-libopus
    --enable-libvorbis
    --enable-libvpx
```

Capture output from the container to the host running the command

```
 docker run jrottenberg/ffmpeg \
            -i http://url/to/media.mp4 \
            -stats \
            $ffmpeg_options  - > out.mp4
```

### Example

```
 docker run jrottenberg/ffmpeg -stats  \
        -i http://archive.org/download/thethreeagesbusterkeaton/Buster.Keaton.The.Three.Ages.ogv \
        -loop 0  \
        -final_delay 500 -c:v gif -f gif -ss 00:49:42 -t 5 - > trow_ball.gif
```

See what's inside the beast
---------------------------

```
$ docker run -it --entrypoint='bash' jrottenberg/ffmpeg
bash-4.1# for i in yasm x264 x265 ogg opus theora vorbis vpx mp3lame faac xvid fdk ;do echo $i; find /usr/local/ -name "*$i*";done
```

Keep uptodate
-------------

-	FFMPEG_VERSION 3.1.3 https://github.com/FFmpeg/FFmpeg/blob/master/Changelog
-	YASM_VERSION 1.3.0 https://github.com/yasm/yasm/releases
-	OGG_VERSION 1.3.2 https://xiph.org/downloads/
-	VORBIS_VERSION 1.3.5 https://xiph.org/downloads/
-	THEORA_VERSION 1.1.1 https://xiph.org/downloads/
-	LAME_VERSION 3.99.5 http://lame.sourceforge.net/download.php
-	OPUS_VERSION 1.1.1 https://www.opus-codec.org/downloads/
-	FAAC_VERSION 1.28 http://www.audiocoding.com/downloads.html
-	VPX_VERSION 1.6.0 https://github.com/webmproject/libvpx/releases
-	XVID_VERSION 1.3.5 https://labs.xvid.com/source/
-	FDKAAC_VERSION 0.1.4 https://github.com/mstorsjo/fdk-aac/releases
-	X265_VERSION 2.0 https://bitbucket.org/multicoreware/x265/downloads
- X264_VERSION latest_stable http://www.videolan.org/developers/x264.html
