FFmpeg Docker image
==================

 [![Docker Stars](https://img.shields.io/docker/stars/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/stars/count/) [![Docker pulls](https://img.shields.io/docker/pulls/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/)
[![Travis](https://img.shields.io/travis/jrottenberg/ffmpeg/master.svg?maxAge=300?style=plastic)](https://travis-ci.org/jrottenberg/ffmpeg)
[![Build Status](https://dev.azure.com/video-tools/ffmpeg/_apis/build/status/jrottenberg.ffmpeg)](https://dev.azure.com/video-tools/ffmpeg/_build/latest?definitionId=1)
[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000?style=plastic)](https://github.com/jrottenberg/ffmpeg/)

This project prepares a minimalist Docker image with FFmpeg. It compiles FFmpeg from sources following instructions from the [Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can be used as a base for an encoding farm.

Ubuntu builds
--------------

You can use jrottenberg/ffmpeg or jrottenberg/ffmpeg:3.3
to get the latest build based on ubuntu.

Note : I've made ubuntu the default after 3.1

You'll find centos based image using `ffmpeg:X.Y-centos` or `ffmpeg:centos` to get the latest.
alpine images  `ffmpeg:X.Y-alpine` to get the latest.
scratch images `ffmpeg:X.Y-scratch` to get the latest. (Scratch is an experimental image containing only FFmpeg and libraries)

Recent images:

```
vaapi               86mb    2018-08-16
snapshot-centos     95mb    2018-08-16
snapshot-alpine     27mb    2018-08-16
4.0-vaapi           86mb    2018-08-15
4.0-ubuntu          94mb    2018-08-16
4.0-scratch         20mb    2018-08-16
4.0-centos          95mb    2018-08-16
3.4-vaapi           84mb    2018-08-15
3.4-scratch         18mb    2018-08-16
3.4-alpine          24mb    2018-08-16
3.4                 92mb    2018-08-16
3.3-scratch         17mb    2018-08-04
3.2-scratch         17mb    2018-08-16
3.2-alpine          24mb    2018-08-16
3.0-scratch         17mb    2018-08-16
3.0-centos          94mb    2018-08-16
2.8-scratch         16mb    2018-08-16
2.8                 90mb    2018-08-16
```

<details><summary>(How the 'recent images' was generated)</summary>
```
    $ curl --silent https://hub.docker.com/v2/repositories/jrottenberg/ffmpeg/tags/?page_size=500 | jq -cr ".results|sort_by(.name)|reverse[]|.sz=(.full_size/1048576|floor|tostring+\"mb\")|[.name,( (20-(.name|length))*\" \" ),.sz,( (8-(.sz|length))*\" \"),.last_updated[:10]]|@text|gsub(\"[,\\\"\\\]\\\[]\";null)" | grep 2018-08
```
</details>

Please use [Github issues](https://github.com/jrottenberg/ffmpeg/issues/new) to report any bug or missing feature.

Test
----

```
ffmpeg version 3.3.4 Copyright (c) 2000-2017 the FFmpeg developers
  built with gcc 5.4.0 (Ubuntu 5.4.0-6ubuntu1~16.04.4) 20160609
  configuration: --disable-debug --disable-doc --disable-ffplay --enable-shared --enable-avresample --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-gpl --enable-libass --enable-libfreetype --enable-libvidstab --enable-libmp3lame --enable-libopenjpeg --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-libx265 --enable-libxvid --enable-libx264 --enable-nonfree --enable-openssl --enable-libfdk_aac --enable-postproc --enable-small --enable-version3 --extra-cflags=-I/opt/ffmpeg/include --extra-ldflags=-L/opt/ffmpeg/lib --extra-libs=-ldl --prefix=/opt/ffmpeg
  libavutil      55. 58.100 / 55. 58.100
  libavcodec     57. 89.100 / 57. 89.100
  libavformat    57. 71.100 / 57. 71.100
  libavdevice    57.  6.100 / 57.  6.100
  libavfilter     6. 82.100 /  6. 82.100
  libavresample   3.  5.  0 /  3.  5.  0
  libswscale      4.  6.100 /  4.  6.100
  libswresample   2.  7.100 /  2.  7.100
  libpostproc    54.  5.100 / 54.  5.100

  configuration:
    --disable-debug
    --disable-doc
    --disable-ffplay
    --enable-shared
    --enable-avresample
    --enable-libopencore-amrnb
    --enable-libopencore-amrwb
    --enable-gpl
    --enable-libass
    --enable-libfreetype
    --enable-libvidstab
    --enable-libmp3lame
    --enable-libopenjpeg
    --enable-libopus
    --enable-libtheora
    --enable-libvorbis
    --enable-libvpx
    --enable-libx265
    --enable-libxvid
    --enable-libx264
    --enable-nonfree
    --enable-openssl
    --enable-libfdk_aac
    --enable-postproc
    --enable-small
    --enable-version3
    --extra-cflags=-I/opt/ffmpeg/include
    --extra-ldflags=-L/opt/ffmpeg/lib
    --extra-libs=-ldl
    --prefix=/opt/ffmpeg
```

Capture output from the container to the host running the command

```
 docker run jrottenberg/ffmpeg \
            -i http://url/to/media.mp4 \
            -stats \
            $ffmpeg_options  - > out.mp4
```

### Examples
#### Extract 5s @00:49:42 into a GIF

```
 docker run jrottenberg/ffmpeg -stats  \
        -i http://archive.org/download/thethreeagesbusterkeaton/Buster.Keaton.The.Three.Ages.ogv \
        -loop 0  \
        -final_delay 500 -c:v gif -f gif -ss 00:49:42 -t 5 - > trow_ball.gif
```

#### Convert 10bits MKV into a 10Bits MP4
```
 docker run -v $PWD:/tmp jrottenberg/ffmpeg:3.4-scratch \
        -stats \
        -i http://www.jell.yfish.us/media/jellyfish-20-mbps-hd-hevc-10bit.mkv \
        -c:v libx265 -pix_fmt yuv420p10 \
        -t 5 -f mp4 /tmp/test.mp4
```
The image has been compiled with [X265 Multilib](https://x265.readthedocs.io/en/default/api.html#multi-library-interface).
Use the pixel format switch to change the number of bits per pixel by suffixing it with 10 for 10bits or 12 for 12bits.

#### Use hardware acceleration enabled build

Thanks to [qmfrederik](https://github.com/qmfrederik) for the vaapi ubuntu based variant

 jrottenberg/ffmpeg:vaapi or jrottenberg/ffmpeg:vaapi-${VERSION}

- Run the container with the device attached /dev/dri from your host into the container :

`docker run --device /dev/dri:/dev/dri -v $(pwd):/mnt jrottenberg/ffmpeg:vaapi [...]`
- Have the Intel drivers up and running on your host. You can run `vainfo` (part of vainfo package on Ubuntu) to determine whether your graphics card has been recognized correctly.
- Run ffmpeg with the correct parameters, this is the same as when running [ffmpeg natively](https://trac.ffmpeg.org/wiki/Hardware/VAAPI).


See what's inside the beast
---------------------------

```
docker run -it --entrypoint='bash' jrottenberg/ffmpeg

for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /usr/local/ -name *$i*;done
```

Keep up to date
---------------

See Dockerfile-env to update a version

- [FFMPEG_VERSION](http://ffmpeg.org/releases/): [GNU Lesser General Public License (LGPL) version 2.1](https://ffmpeg.org/legal.html)
- [OGG_VERSION](https://xiph.org/downloads/): [BSD-style license](https://git.xiph.org/?p=mirrors/ogg.git;a=blob_plain;f=COPYING;hb=HEAD)
- [OPENCOREAMR_VERSION](https://sourceforge.net/projects/opencore-amr/files/opencore-amr/): [Apache License](https://sourceforge.net/p/opencore-amr/code/ci/master/tree/LICENSE)
- [VORBIS_VERSION](https://xiph.org/downloads/): [BSD-style license](https://git.xiph.org/?p=mirrors/vorbis.git;a=blob_plain;f=COPYING;hb=HEAD)
- [THEORA_VERSION](https://xiph.org/downloads/): [BSD-style license](https://git.xiph.org/?p=mirrors/theora.git;a=blob_plain;f=COPYING;hb=HEAD)
- [LAME_VERSION](http://lame.sourceforge.net/download.php): [GNU Lesser General Public License (LGPL) version 2.1](http://lame.cvs.sourceforge.net/viewvc/lame/lame/LICENSE?revision=1.9)
- [OPUS_VERSION](https://www.opus-codec.org/downloads/): [BSD-style license](https://www.opus-codec.org/license/)
- [VPX_VERSION](https://github.com/webmproject/libvpx/releases): [BSD-style license](https://github.com/webmproject/libvpx/blob/master/LICENSE)
- [XVID_VERSION](https://labs.xvid.com/source/): [GNU General Public Licence (GPL) version 2](http://websvn.xvid.org/cvs/viewvc.cgi/trunk/xvidcore/LICENSE?revision=851)
- [FDKAAC_VERSION](https://github.com/mstorsjo/fdk-aac/releases): [Liberal but not a license of patented technologies](https://github.com/mstorsjo/fdk-aac/blob/master/NOTICE)
- [FREETYPE_VERSION](http://download.savannah.gnu.org/releases/freetype/): [GNU General Public License (GPL) version 2](https://www.freetype.org/license.html)
- [LIBVIDSTAB_VERSION](https://github.com/georgmartius/vid.stab/releases): [GNU General Public License (GPL) version 2](https://github.com/georgmartius/vid.stab/blob/master/LICENSE)
- [LIBFRIDIBI_VERSION](https://www.fribidi.org/): [GNU General Public License (GPL) version 2](https://cgit.freedesktop.org/fribidi/fribidi/plain/COPYING)
- [X264_VERSION](http://www.videolan.org/developers/x264.html): [GNU General Public License (GPL) version 2](https://git.videolan.org/?p=x264.git;a=blob_plain;f=COPYING;hb=HEAD)
- [X265_VERSION](https://bitbucket.org/multicoreware/x265/downloads/):[GNU General Public License (GPL) version 2](https://bitbucket.org/multicoreware/x265/raw/f8ae7afc1f61ed0db3b2f23f5d581706fe6ed677/COPYING)


Contribute
-----------


```
# Add / fix stuff
${EDITOR} templates/

# Generates the Dockerfile for all variants
./update.py

# Test a specific variant
docker build -t my-build docker-images/VERSION/

# Make sure all variants pass before Travis does
find ffmpeg/ -name Dockerfile | xargs dirname | parallel --no-notice -j 4 --results logs docker build -t {} {}
```


Commit the templates files THEN all the generated Dockerfile for a merge request. So it's easier to review the template change.
