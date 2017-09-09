FFMPEG for Docker on Centos7
============================

 [![Docker Stars](https://img.shields.io/docker/stars/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/stars/count/) [![Docker pulls](https://img.shields.io/docker/pulls/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/)
[![Travis](https://img.shields.io/travis/jrottenberg/ffmpeg/master.svg?maxAge=300?style=plastic)](https://travis-ci.org/jrottenberg/ffmpeg)
[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000?style=plastic)](https://github.com/jrottenberg/ffmpeg/)

This project prepares a minimalist Docker image with FFMPEG. It compiles FFMPEG from sources following instructions from the [Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can be used as a base for an encoding farm, based on centos7.

Ubuntu builds
--------------

You can use jrottenberg/ffmpeg:ubuntu or jrottenberg/ffmpeg:3.1 or jrottenberg/ffmpeg:3
to get the latest build based on ubuntu.

Note : I've made ubuntu the default after 3.1

You'll find centos based image using `ffmpeg:X.Y-centos` or `ffmpeg:centos` to get the latest.
alpine images  `ffmpeg:X.Y-alpine` or `ffmpeg:alpine` to get the latest.

For information :
```
u-3.2               ubuntu              1e998987f2da        2 minutes ago        205.5 MB
c-3.2               centos              b73e2e768092        9 minutes ago        274.4 MB
a-3.2               alpine              5da8a4eaeb41        45 minutes ago       73.64 MB
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
    --enable-libfreetype
    --enable-libvidstab
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
docker run -it --entrypoint='bash' jrottenberg/ffmpeg

for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /usr/local/ -name *$i*;done
```

Keep up to date
---------------

See Dockerfile-env to update a version

- [FFMPEG_VERSION](http://ffmpeg.org/releases/)

- [OGG_VERSION](https://xiph.org/downloads/)
- [OPENCOREAMR_VERSION](https://sourceforge.net/projects/opencore-amr/files/opencore-amr/)
- [VORBIS_VERSION](https://xiph.org/downloads/)
- [THEORA_VERSION](https://xiph.org/downloads/)
- [LAME_VERSION](http://lame.sourceforge.net/download.php)
- [OPUS_VERSION](https://www.opus-codec.org/downloads/)
- [FAAC_VERSION](http://www.audiocoding.com/downloads.html)
- [VPX_VERSION](https://github.com/webmproject/libvpx/releases)
- [XVID_VERSION](https://labs.xvid.com/source/)
- [FDKAAC_VERSION](https://github.com/mstorsjo/fdk-aac/releases)
- [FREETYPE_VERSION](http://download.savannah.gnu.org/releases/freetype/)
- [LIBVIDSTAB_VERSION](https://github.com/georgmartius/vid.stab/releases)
- [X264_VERSION](http://www.videolan.org/developers/x264.html)
- [X265_VERSION](https://bitbucket.org/multicoreware/x265/downloads/)


Contribute
-----------


```

${EDITOR} Dockerfile-env

./update.py # generates the Dockerfile

docker build -t my-build VERSION/path/

# make sure all variants pass before Travis does
find ffmpeg/ -name Dockerfile | xargs dirname | parallel --no-notice -j 4 --results logs docker build -t {} {}
```


Commit the env file THEN all the generated Dockerfile for a merge request. So it's easier to find the template change.
