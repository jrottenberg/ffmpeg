# FFmpeg Docker image

 [![Docker Stars](https://img.shields.io/docker/stars/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/stars/count/) [![Docker pulls](https://img.shields.io/docker/pulls/jrottenberg/ffmpeg.svg?style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/)
[![gitlab pipeline status](https://gitlab.com/jrottenberg/ffmpeg/badges/master/pipeline.svg)](https://gitlab.com/jrottenberg/ffmpeg/commits/master)
[![Azure Build Status](https://dev.azure.com/video-tools/ffmpeg/_apis/build/status/jrottenberg.ffmpeg)](https://dev.azure.com/video-tools/ffmpeg/_build/latest?definitionId=1)
[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000?style=plastic)](https://github.com/jrottenberg/ffmpeg/)

This project prepares a minimalist Docker image with FFmpeg. It compiles FFmpeg from sources following instructions from the [Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can be used as a base for an encoding farm.

## Builds

You can use jrottenberg/ffmpeg or jrottenberg/ffmpeg:3.3
to get the latest build based on ubuntu.

Note : I've made ubuntu the default after 3.1

You'll find centos based image using `ffmpeg:X.Y-centos` or `ffmpeg:centos` to get the latest.
alpine images  `ffmpeg:X.Y-alpine` to get the latest.
scratch images `ffmpeg:X.Y-scratch` to get the latest. (Scratch is an experimental image containing only FFmpeg and libraries)

Format is `ffmpeg:MAJOR.MINOR-VARIANT` with MAJOR.MINOR in :

- 2.8
- 3.0
- 3.1
- 3.2
- 3.3
- 3.4
- 4.0
- 4.1
- snapshot

and VARIANT in :

- alpine
- centos
- nvidia
- scratch
- ubuntu
- vaapi

Recent images:

```text
snapshot-vaapi      74mb
snapshot-ubuntu     86mb
snapshot-scratch    20mb
snapshot-nvidia     640mb
snapshot-centos     97mb
snapshot-alpine     35mb
4.1-vaapi           73mb
4.1-ubuntu          85mb
4.1-scratch         20mb
4.1-nvidia          640mb
4.1-centos          97mb
4.1-alpine          34mb
4.0-vaapi           73mb
4.0-ubuntu          83mb
4.0-scratch         20mb
4.0-nvidia          639mb
4.0-centos          97mb
4.0-alpine          34mb
3.4-vaapi           71mb
3.4-ubuntu          83mb
3.4-scratch         18mb
3.4-nvidia          637mb
3.4-centos          97mb
3.4-alpine          32mb
3.4                 83mb
3.3-vaapi           71mb
3.3-ubuntu          83mb
3.3-scratch         18mb
3.3-nvidia          637mb
3.3-centos          96mb
3.3-alpine          31mb
3.3                 82mb
3.2-vaapi           83mb
3.2-ubuntu          83mb
3.2-scratch         18mb
3.2-nvidia          623mb
3.2-centos          96mb
3.2-alpine          32mb
3.1-vaapi           83mb
3.1-ubuntu          82mb
3.1-scratch         17mb
3.1-nvidia          623mb
3.1-centos          96mb
3.1-alpine          32mb
3.1                 81mb
3.0-ubuntu          82mb
3.0-scratch         17mb
3.0-nvidia          623mb
3.0-centos          96mb
3.0-alpine          31mb
2.8-vaapi           82mb
2.8-ubuntu          81mb
2.8-scratch         17mb
2.8-nvidia          622mb
2.8-centos          95mb
2.8-alpine          30mb
```

### How the 'recent images' was generated

```bash
$ curl --silent https://hub.docker.com/v2/repositories/jrottenberg/ffmpeg/tags/?page_size=500 | jq -cr ".results|sort_by(.name)|reverse[]|.sz=(.full_size/1048576|floor|tostring+\"mb\")|[.name,( (20-(.name|length))*\" \" ),.sz,( (8-(.sz|length))*\" \"),.last_updated[:10]]|@text|gsub(\"[,\\\"\\\]\\\[]\";null)"

# If you want to compare the one you have locally
$ docker images | grep ffmpeg | sort | awk '{print $1 ":" $2 "\t" $7 $8}'
```

Please use [Github issues](https://github.com/jrottenberg/ffmpeg/issues/new) to report any bug or missing feature.

## Test

```bash
ffmpeg version N-98740-ga72d529 Copyright (c) 2000-2020 the FFmpeg developers
  built with gcc 7 (Ubuntu 7.5.0-3ubuntu1~18.04)
  configuration: --disable-debug --disable-doc --disable-ffplay --enable-shared --enable-avresample --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-gpl --enable-libass --enable-fontconfig --enable-libfreetype --enable-libvidstab --enable-libmp3lame --enable-libopus --enable-libtheora --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libxcb --enable-libx265 --enable-libxvid --enable-libx264 --enable-nonfree --enable-openssl --enable-libfdk_aac --enable-postproc --enable-small --enable-version3 --enable-libbluray --enable-libzmq --extra-libs=-ldl --prefix=/opt/ffmpeg --enable-libopenjpeg --enable-libkvazaar --enable-libaom --extra-libs=-lpthread --enable-libsrt --enable-libaribb24 --enable-vaapi --extra-cflags=-I/opt/ffmpeg/include --extra-ldflags=-L/opt/ffmpeg/lib
  libavutil      56. 58.100 / 56. 58.100
  libavcodec     58.100.100 / 58.100.100
  libavformat    58. 51.100 / 58. 51.100
  libavdevice    58. 11.101 / 58. 11.101
  libavfilter     7. 87.100 /  7. 87.100
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  8.100 /  5.  8.100
  libswresample   3.  8.100 /  3.  8.100
  libpostproc    55.  8.100 / 55.  8.100

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
    --enable-fontconfig
    --enable-libfreetype
    --enable-libvidstab
    --enable-libmp3lame
    --enable-libopus
    --enable-libtheora
    --enable-libvorbis
    --enable-libvpx
    --enable-libwebp
    --enable-libxcb
    --enable-libx265
    --enable-libxvid
    --enable-libx264
    --enable-nonfree
    --enable-openssl
    --enable-libfdk_aac
    --enable-postproc
    --enable-small
    --enable-version3
    --enable-libbluray
    --enable-libzmq
    --extra-libs=-ldl
    --prefix=/opt/ffmpeg
    --enable-libopenjpeg
    --enable-libkvazaar
    --enable-libaom
    --extra-libs=-lpthread
    --enable-libsrt
    --enable-libaribb24
    --enable-vaapi
    --extra-cflags=-I/opt/ffmpeg/include
    --extra-ldflags=-L/opt/ffmpeg/lib
```

Capture output from the container to the host running the command

```bash
 docker run jrottenberg/ffmpeg \
            -i http://url/to/media.mp4 \
            -stats \
            $ffmpeg_options  - > out.mp4
```

### Examples

#### Extract 5s @00:49:42 into a GIF

```bash
 docker run jrottenberg/ffmpeg -stats  \
        -i http://archive.org/download/thethreeagesbusterkeaton/Buster.Keaton.The.Three.Ages.ogv \
        -loop 0  \
        -final_delay 500 -c:v gif -f gif -ss 00:49:42 -t 5 - > trow_ball.gif
```

#### Convert 10bits MKV into a 10Bits MP4

```bash
 docker run -v $(pwd):$(pwd) -w $(pwd) jrottenberg/ffmpeg:3.4-scratch \
        -stats \
        -i http://www.jell.yfish.us/media/jellyfish-20-mbps-hd-hevc-10bit.mkv \
        -c:v libx265 -pix_fmt yuv420p10 \
        -t 5 -f mp4 test.mp4
```

The image has been compiled with [X265 Multilib](https://x265.readthedocs.io/en/default/api.html#multi-library-interface).
Use the pixel format switch to change the number of bits per pixel by suffixing it with 10 for 10bits or 12 for 12bits.

#### Convert a local GIF into a mp4

Let's assume ```original.gif``` is located in the current directory :

```bash
 docker run -v $(pwd):$(pwd) -w $(pwd)\
        jrottenberg/ffmpeg:3.2-scratch -stats \
        -i original.gif \
        original-converted.mp4
```

#### Use ZeroMQ to toggle filter value on-fly

Let's start some process continuously writing some radio music, and listen it:

```bash
 docker run --rm -d -v $(pwd):$(pwd) -w $(pwd) -p 11235:11235 \
        --name radio-writer jrottenberg/ffmpeg \
        -i http://radio.casse-tete.solutions/salut-radio-64.mp3 \
        -filter_complex '[0:a]volume@vol=1,azmq=bind_address=tcp\\\://0.0.0.0\\\:11235[out]' \
        -map '[out]' ./salut-radio.mp3

 ffplay ./salut-radio.mp3
```

Now, just toggle its volume on-fly, and hear how it changes:

```bash
 docker run --rm --network=host --entrypoint sh jrottenberg/ffmpeg -c \
        'echo "volume@vol volume 2" | zmqsend -b tcp://127.0.0.1:11235'
```

#### Send a stream over SRT

Let's send `video.mp4` to srt-listener on port 9000 over SRT protocol.

```bash
docker run -v $(pwd):$(pwd) jrottenberg/ffmpeg \
       -re -i $(pwd)/video.mp4 -acodec copy -vcodec copy -f mpegts srt://srt-listener:9000?pkt_size=1316
```

#### Use hardware acceleration enabled build

Thanks to [qmfrederik](https://github.com/qmfrederik) for the [vaapi ubuntu based variant](https://github.com/jrottenberg/ffmpeg/pull/106)

 jrottenberg/ffmpeg:vaapi or jrottenberg/ffmpeg:${VERSION}-vaapi

- Run the container with the device attached /dev/dri from your host into the container :

`docker run --device /dev/dri:/dev/dri -v $(pwd):$(pwd) -w $(pwd) jrottenberg/ffmpeg:vaapi [...]`

- Have the Intel drivers up and running on your host. You can run `vainfo` (part of vainfo package on Ubuntu) to determine whether your graphics card has been recognized correctly.
- Run ffmpeg with the correct parameters, this is the same as when running [ffmpeg natively](https://trac.ffmpeg.org/wiki/Hardware/VAAPI).

#### Use nvidia hardware acceleration enabled build

Thanks to [ShaulMyplay](https://github.com/ShaulMyplay) for the [nvidia based variant](https://github.com/jrottenberg/ffmpeg/pull/168)

Supports nvenc only on all ffmpeg versions, and hardware decoding and scaling on ffmpeg >= 4.0

- Install nvidia latest drivers on host machine.
- Install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) on host machine.
- Run container using "--runtime=nvidia" flag and use supported [ffmpeg hwaccel options](https://trac.ffmpeg.org/wiki/HWAccelIntro)

Hardware encoding only example:

`docker run --runtime=nvidia jrottenberg/ffmpeg:2.8-nvidia -i INPUT -c:v nvenc_h264 -preset hq OUTPUT`
Full hardware acceleration example:
`docker run --runtime=nvidia jrottenberg/ffmpeg:4.1-nvidia -hwaccel cuvid -c:v h264_cuvid -i INPUT -vf scale_npp=-1:720 -c:v h264_nvenc -preset slow OUTPUT`

##### See what's inside the beast

```bash
docker run -it --entrypoint='bash' jrottenberg/ffmpeg

for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /usr/local/ -name *$i*;done
```

## Keep up to date

See Dockerfile-env to update a version

- [FFMPEG_VERSION](http://ffmpeg.org/releases/): [GNU Lesser General Public License (LGPL) version 2.1](https://ffmpeg.org/legal.html)
- [OGG_VERSION](https://xiph.org/downloads/): [BSD-style license](https://git.xiph.org/?p=mirrors/ogg.git;a=blob_plain;f=COPYING;hb=HEAD)
- [OPENCOREAMR_VERSION](https://sourceforge.net/projects/opencore-amr/files/opencore-amr/): [Apache License](https://sourceforge.net/p/opencore-amr/code/ci/master/tree/LICENSE)
- [VORBIS_VERSION](https://xiph.org/downloads/): [BSD-style license](https://git.xiph.org/?p=mirrors/vorbis.git;a=blob_plain;f=COPYING;hb=HEAD)
- [THEORA_VERSION](https://xiph.org/downloads/): [BSD-style license](https://git.xiph.org/?p=mirrors/theora.git;a=blob_plain;f=COPYING;hb=HEAD)
- [LAME_VERSION](http://lame.sourceforge.net/download.php): [GNU Lesser General Public License (LGPL) version 2.1](http://lame.cvs.sourceforge.net/viewvc/lame/lame/LICENSE?revision=1.9)
- [OPUS_VERSION](https://www.opus-codec.org/downloads/): [BSD-style license](https://www.opus-codec.org/license/)
- [VPX_VERSION](https://github.com/webmproject/libvpx/releases): [BSD-style license](https://github.com/webmproject/libvpx/blob/master/LICENSE)
- [WEBP_VERSION](https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html): [BSD-style license](https://github.com/webmproject/libvpx/blob/master/LICENSE)
- [XVID_VERSION](https://labs.xvid.com/source/): [GNU General Public Licence (GPL) version 2](http://websvn.xvid.org/cvs/viewvc.cgi/trunk/xvidcore/LICENSE?revision=851)
- [FDKAAC_VERSION](https://github.com/mstorsjo/fdk-aac/releases): [Liberal but not a license of patented technologies](https://github.com/mstorsjo/fdk-aac/blob/master/NOTICE)
- [FREETYPE_VERSION](http://download.savannah.gnu.org/releases/freetype/): [GNU General Public License (GPL) version 2](https://www.freetype.org/license.html)
- [LIBVIDSTAB_VERSION](https://github.com/georgmartius/vid.stab/releases): [GNU General Public License (GPL) version 2](https://github.com/georgmartius/vid.stab/blob/master/LICENSE)
- [LIBFRIDIBI_VERSION](https://www.fribidi.org/): [GNU General Public License (GPL) version 2](https://cgit.freedesktop.org/fribidi/fribidi/plain/COPYING)
- [X264_VERSION](http://www.videolan.org/developers/x264.html): [GNU General Public License (GPL) version 2](https://git.videolan.org/?p=x264.git;a=blob_plain;f=COPYING;hb=HEAD)
- [X265_VERSION](https://bitbucket.org/multicoreware/x265/downloads/): [GNU General Public License (GPL) version 2](https://bitbucket.org/multicoreware/x265/raw/f8ae7afc1f61ed0db3b2f23f5d581706fe6ed677/COPYING)
- [LIBZMQ_VERSION](https://github.com/zeromq/libzmq/releases/): [GNU Lesser General Public License (LGPL) version 3.0](https://github.com/zeromq/libzmq/blob/v4.3.2/COPYING.LESSER)
- [LIBSRT_VERSION](https://github.com/Haivision/srt/releases/): [MPL-2.0](https://github.com/Haivision/srt/blob/master/LICENSE)
- [LIBPNG_VERSION](https://sourceforge.net/projects/libpng/files/): [zlib/libpng License](https://sourceforge.net/p/libpng/code/ci/master/tree/LICENSE)
- [LIBARIBB24_VERSION](https://github.com/nkoriyama/aribb24/tree/bc45f1406899603033218c2cc6d611ddcc5b3720): [GNU Lesser General Public License (LGPL) version 2.1 or newer](https://github.com/nkoriyama/aribb24/issues/9)

## Contribute

```text
# Add / fix stuff
${EDITOR} templates/

# Generates the Dockerfile for all variants
./update.py

# Test a specific variant
docker build -t my-build docker-images/VERSION/

# Make sure all variants pass before CI
find ffmpeg/ -name Dockerfile | xargs dirname | parallel --no-notice -j 4 --results logs docker build -t {} {}
```

Commit the templates files THEN all the generated Dockerfile for a merge request. So it's easier to review the template change.
