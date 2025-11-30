# FFmpeg Docker image

[![Docker Stars](https://img.shields.io/docker/stars/jrottenberg/ffmpeg.svg?logo=docker&style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/stars/count/)
[![Docker pulls](https://img.shields.io/docker/pulls/jrottenberg/ffmpeg.svg?logo=docker&style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/)
[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?logo=docker)](https://hub.docker.com/r/jrottenberg/ffmpeg/tags)
[![Github Container Registry Images](https://img.shields.io/badge/images-automated-blue?logo=github&style=plastic)](https://github.com/jrottenberg/ffmpeg/pkgs/container/ffmpeg)
[![gitlab pipeline status](https://gitlab.com/jrottenberg/ffmpeg/badges/main/pipeline.svg)](https://gitlab.com/jrottenberg/ffmpeg/commits/main)
[![Azure Build Status](https://dev.azure.com/video-tools/ffmpeg/_apis/build/status/jrottenberg.ffmpeg)](https://dev.azure.com/video-tools/ffmpeg/_build/latest?definitionId=1)


This project prepares a minimalist Docker image with FFmpeg. It compiles FFmpeg from sources following instructions from the [Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg:${VERSION}-${VARIANT}` or `docker pull ghcr.io/jrottenberg/ffmpeg:${VERSION}-${VARIANT}`.

For the latest FFmpeg version on Ubuntu LTS, you can use: `docker pull jrottenberg/ffmpeg:latest` or `docker pull ghcr.io/jrottenberg/ffmpeg:latest`.

This image can be used as a base for an encoding farm.

## Builds / Avaliabvle Docker Containers

There are different builds available:
Below is a table that provides examples for the nomenclature:

`ffmpeg-<version>-<os variant and version>`

| image name | OS ver | ffmpeg ver | variant | description
| --- | --- | --- | --- | --- |
| ffmpeg-7.1-ubuntu2404 | 24.04 | 6.x - 7.x | [ubuntu](https://releases.ubuntu.com/) | external libraries are installed from os packages, and ffmpeg is built from source. See [Ubuntu Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu) for details on this. |
| ffmpeg-7.1-ubuntu2404-edge | 24.04 | 6.x - 7.x | [ubuntu](https://releases.ubuntu.com/) | libs and ffmpeg are built from source. See [Ubuntu Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu) for details on this. |
| ffmpeg-7.1-vaapi2404 | 24.04 | 6.x - 7.x | [ubuntu](https://releases.ubuntu.com/) | like: `ubuntu2404` but enables: [Video Acceleration API (VAAPI)](https://trac.ffmpeg.org/wiki/HWAccelIntro#VAAPI) in ffmpeg |
| ffmpeg-7.1-nvidia2204-edge | 22.04 | 6.x - 7.x | [ubuntu](https://releases.ubuntu.com/) | Built w/ [NVIDIA's hardware-accelerated encoding and decoding APIs](https://trac.ffmpeg.org/wiki/HWAccelIntro#CUDANVENCNVDEC) enabled |
| ffmpeg-7.1-alpine320 | 3.20 | 6.x - 7.x | [alpine](https://alpinelinux.org/releases/) | vendor libs, but ffmpeg is built from source |
| ffmpeg-7.1-scratch | 3.20 | 6.x - 7.x | [alpine](https://alpinelinux.org/releases/) | vendor libs, and ffmpeg are built from source. Also we make the distro as small as possible by not installing any packages in base and striping symbols of installed libs |

ffmpeg `<version>` can be one of the following: `6.1`, `7.0`, `7.1` with the above table.

Note: The current versions of ffmpeg supported are  anything newer than 3 years old and not exceeded the end-of-life


<details><summary>Here are some additional older builds</summary>

- alpine based images `ffmpeg:<version>-alpine` or `ffmpeg:<version>-alpine313`  (old versions with `ffmpeg:<version>-alpine312` , `ffmpeg:<version>-alpine311`)
  - alpine based scratch images `ffmpeg:<version>-scratch` or `ffmpeg:<version>-scratch313`   (old versions with `ffmpeg:<version>-scratch312` , `ffmpeg:<version>-scratch311`)
- ubuntu based images `ffmpeg:<version>-ubuntu` or `ffmpeg:<version>-ubuntu2004` (old versions with `ffmpeg:<version>-ubuntu1804` , `ffmpeg:<version>-ubuntu1604`)
  - ubuntu based nvidia images `ffmpeg:<version>-nvidia` or `ffmpeg:<version>-nvidia2004` (old versions with `ffmpeg:<version>-nvidia1804`, `ffmpeg:<version>-nvidia1604`)
  - ubuntu based vaapi images `ffmpeg:<version>-vaapi1804` or `ffmpeg:<version>-vaapi2004` (old versions with `ffmpeg:<version>-vaapi1804`, `ffmpeg:<version>-nvidia1604`)

</details>

### Philosophy behind the different builds

**ubuntu2404**
We chose Ubuntu 24.04 because it is the LTS ( Long Term Support ) build of Ubuntu.
We used the ffmpeg support libraries from the Ubuntu distrobution where possible. Example: we use 'libx264-dev' as the package to install. We do not tie it to a version. This way when its time to update from 24.04 to 26.04 we can simply update the base Docker template for ubuntu. This will make updating the OS easier as time goes on.

**ubuntu2404-edge**
This image is just like the above `ubuntu2404` container image, except we build all of the ffmpeg support libraries. This is in the spirit of the original intent of this project `jrottenberg/ffmpeg` alltogether. Building everything that ffmpeg needs, and ffmpeg itself from source. This gives us the most control over all of the details of release. The drawback of this is that its much harder to keep updated. The thought process of having both 'Ubuntu-2404' and 'Ubuntu-2404-edge' is that it makes updating the OS easier over time.

**vaapi2404**
 This release is like also `ubuntu2404` but enables: [Video Acceleration API (VAAPI)](https://trac.ffmpeg.org/wiki/HWAccelIntro#VAAPI) when building ffmpeg

**nvidia2204-edge**
 This release is like also `ubuntu2404` but enables: [NVIDIA's hardware-accelerated encoding and decoding APIs](https://trac.ffmpeg.org/wiki/HWAccelIntro#CUDANVENCNVDEC) enabled

**alpine320**
[alpine](https://alpinelinux.org/releases/) uses the os vendor libs, but ffmpeg is built from source.

**scratch**
Scratch is also an [alpine](https://alpinelinux.org/releases/) image. We build the vendor libs, and ffmpeg from source. Also we make the distro as small as possible by not installing any packages in base and striping symbols of installed libs.

### Generate list of recent Docker Container Images

You can use the following command to generate a list of current images:
```bash
$ python3 -mvenv .venv
$ source .venv/bin/activate
$ pip install requests
$ python3 ./generate-list-of-recent-images.py > list_of_recent_images.txt
$ deactivate
$ rm -rf .venv
$ less list_of_recent_images.txt
```

If you want to compare the one you have locally, use the following command:
```bash
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
 docker run jrottenberg/ffmpeg:4.4-alpine \
            -i http://url/to/media.mp4 \
            -stats \
            $ffmpeg_options  - > out.mp4
```

### Examples

#### Extract 5s @00:49:42 into a GIF

```bash
 docker run jrottenberg/ffmpeg:4.4-alpine -stats  \
        -i http://archive.org/download/thethreeagesbusterkeaton/Buster.Keaton.The.Three.Ages.ogv \
        -loop 0  \
        -final_delay 500 -c:v gif -f gif -ss 00:49:42 -t 5 - > trow_ball.gif
```

#### Convert 10bits MKV into a 10Bits MP4

```bash
 docker run -v $(pwd):$(pwd) -w $(pwd) jrottenberg/ffmpeg:4.4-scratch \
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
        jrottenberg/ffmpeg:4.4-scratch -stats \
        -i original.gif \
        original-converted.mp4
```

#### Use ZeroMQ to toggle filter value on-fly

Let's start some process continuously writing some radio music, and listen it:

```bash
docker run --rm -d -v $(pwd):$(pwd) -w $(pwd) -p 11235:11235 \
        --name radio-writer jrottenberg/ffmpeg:4.4-alpine \
        -i http://radio.casse-tete.solutions/salut-radio-64.mp3 \
        -filter_complex '[0:a]volume@vol=1,azmq=bind_address=tcp\\\://0.0.0.0\\\:11235[out]' \
        -map '[out]' ./salut-radio.mp3

docker run -it -v $(pwd):$(pwd) -w $(pwd) --entrypoint=ffprobe jrottenberg/ffmpeg:4.4-alpine -v quiet  -show_streams salut-radio.mp3
```

Now, just toggle its volume on-fly, and hear how it changes:

```bash
docker run --rm --network=host --entrypoint sh jrottenberg/ffmpeg:4.4-ubuntu -c \
        'echo "volume@vol volume 2" | zmqsend -b tcp://127.0.0.1:11235'
```

#### Send a stream over SRT

Let's send `video.mp4` to srt-listener on port 9000 over SRT protocol.

```bash
docker run -v $(pwd):$(pwd) jrottenberg/ffmpeg:4.4-centos \
       -re -i $(pwd)/video.mp4 -acodec copy -vcodec copy -f mpegts srt://srt-listener:9000?pkt_size=1316
```

#### Use hardware acceleration enabled build

Thanks to [qmfrederik](https://github.com/qmfrederik) for the [vaapi ubuntu based variant](https://github.com/jrottenberg/ffmpeg/pull/106)

 jrottenberg/ffmpeg:vaapi or jrottenberg/ffmpeg:${VERSION}-vaapi

- Run the container with the device attached /dev/dri from your host into the container :

`docker run --device /dev/dri:/dev/dri -v $(pwd):$(pwd) -w $(pwd) jrottenberg/ffmpeg:4.4-vaapi [...]`

- Have the Intel drivers up and running on your host. You can run `vainfo` (part of vainfo package on Ubuntu) to determine whether your graphics card has been recognized correctly.
- Run ffmpeg with the correct parameters, this is the same as when running [ffmpeg natively](https://trac.ffmpeg.org/wiki/Hardware/VAAPI).

#### Use nvidia hardware acceleration enabled build

Thanks to [ShaulMyplay](https://github.com/ShaulMyplay) for the [nvidia based variant](https://github.com/jrottenberg/ffmpeg/pull/168)

Supports nvenc only on all ffmpeg versions, and hardware decoding and scaling on ffmpeg >= 4.0

- Install nvidia latest drivers on host machine.
- Install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) on host machine.
- Run container using "--runtime=nvidia" flag and use supported [ffmpeg hwaccel options](https://trac.ffmpeg.org/wiki/HWAccelIntro)

Hardware encoding only example:

`docker run --runtime=nvidia jrottenberg/ffmpeg:4.4-nvidia -i INPUT -c:v nvenc_h264 -preset hq OUTPUT`
Full hardware acceleration example:
`docker run --runtime=nvidia jrottenberg/ffmpeg:4.4-nvidia -hwaccel cuvid -c:v h264_cuvid -i INPUT -vf scale_npp=-1:720 -c:v h264_nvenc -preset slow OUTPUT`

##### See what's inside the beast

```bash
docker run -it --entrypoint='bash' jrottenberg/ffmpeg:7.1-ubuntu2404
for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /usr/local/ -name *$i*;done
```
Libs are in `/lib` in alpine.
```bash
docker run -it --entrypoint='sh' jrottenberg/ffmpeg:7.1-alpine320
for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /lib/ -name *$i*;done
```


## FFMPEG Supported Libraries
The following libraries are used by FFMPEG. The version number and release date are provided along with the license information.
These version numbers are for the lib source builds, which are 'ubuntu2404-edge' and 'foo'.
These libs are included in the package images as well, but the version numbers might vary slightly.
| Libraries | Version | Release Date | License |
|-----------|---------|--------------|---------|
| [ffmpeg](http://ffmpeg.org/) | [7.1](http://ffmpeg.org/releases/) |  | [GNU Lesser General Public License (LGPL) version 2.1](https://ffmpeg.org/legal.html)|
| [libogg](https://www.xiph.org/ogg/) | [1.3.4](https://xiph.org/downloads/) | 08-2019 | [BSD-style license](https://git.xiph.org/?p=mirrors/ogg.git;a=blob_plain;f=COPYING;hb=HEAD)|
| [libopencore-amr](https://sourceforge.net/projects/opencore-amr/) | [0.1.6](https://sourceforge.net/projects/opencore-amr/files/opencore-amr/) | 08-2022 | [Apache License](https://sourceforge.net/p/opencore-amr/code/ci/master/tree/LICENSE)|


See `generate-source-of-truth-ffmpeg-versions.py` to update a version

## FFMPEG Supported Libraries
The following libraries are used by FFMPEG. The version number and release date are provided along with the license information.
These version numbers are for the lib source builds, which are 'ubuntu2404-edge' and 'foo'.
These libs are included in the package images as well, but the version numbers might vary slightly.

| Libraries | Version | Release Date | Download Source | Checksum | License |
|-----------|---------|--------------|------------ | --- | ---------|
| [libopencore-amr](https://sourceforge.net/projects/opencore-amr/) | [0.1.6](https://sourceforge.net/projects/opencore-amr/files/opencore-amr/) | 2022-08-01 | [opencore-amr-0.1.6.tar.gz](https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-0.1.6.tar.gz) | No | [Apache License](https://sourceforge.net/p/opencore-amr/code/ci/master/tree/LICENSE) |
| [libx264](https://www.videolan.org/developers/x264.html) | [20191217-2245-stable](https://download.videolan.org/pub/videolan/x264/snapshots/) | 2019-12-17 | [x264-snapshot-20191217-2245-stable.tar.bz2](https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-20191217-2245-stable.tar.bz2) | No | [GNU General Public License (GPL) version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| [libx265](http://x265.org/) | [4.0](http://ftp.videolan.org/pub/videolan/x265/) | 2024-09-13 | [x265_4.0.tar.gz](http://ftp.videolan.org/pub/videolan/x265/x265_4.0.tar.gz) | No | [GNU General Public License (GPL) version 2](https://bitbucket.org/multicoreware/x265/raw/f8ae7afc1f61ed0db3b2f23f5d581706fe6ed677/COPYING) |
| [libogg](https://www.xiph.org/ogg/) | [1.3.5](https://xiph.org/downloads/) | 2021-06-04 | [libogg-1.3.5.tar.gz](https://downloads.xiph.org/releases/ogg/libogg-1.3.5.tar.gz) | No | [BSD-style license](https://git.xiph.org/?p=mirrors/ogg.git;a=blob_plain;f=COPYING;hb=HEAD) |
| [libopus](https://www.opus-codec.org/) | [1.5.2](https://www.opus-codec.org/downloads/) | 2024-04-12 | [opus-1.5.2.tar.gz](https://github.com/xiph/opus/releases/download/v1.5.2/opus-1.5.2.tar.gz) | Yes | [BSD-style license](https://www.xiph.org/licenses/bsd/) |
| [libvorbis](https://xiph.org/vorbis/) | [1.3.7](https://xiph.org/downloads/) | 2020-07-04 | [libvorbis-1.3.7.tar.gz](http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.7.tar.gz) | Yes | [BSD-style license](https://www.xiph.org/licenses/bsd/) |
| [libvpx](https://www.webmproject.org/code/) | [1.14.1](https://chromium.googlesource.com/webm/libvpx.git/) | 2024-05-30 |  | No | [BSD-style license](https://github.com/webmproject/libvpx/blob/master/LICENSE) |
| [libwebp](https://developers.google.com/speed/webp/) | [1.4.0](https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html) | 2024-04-13 | [libwebp-1.4.0.tar.gz](https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.4.0.tar.gz) | No | [BSD-style license](https://github.com/webmproject/libvpx/blob/master/LICENSE) |
| [libmp3lame](http://lame.sourceforge.net/) | [3.100](http://lame.sourceforge.net/download.php) | 2017-10-13 | [lame-3.100.tar.gz](https://sourceforge.net/projects/lame/files/lame/3.100/lame-3.100.tar.gz) | No | [GNU Lesser General Public License (LGPL) version 2.1](http://lame.cvs.sourceforge.net/viewvc/lame/lame/LICENSE?revision=1.9) |
| [libxvid](https://www.xvid.com/) | [1.3.7](https://labs.xvid.com/source/) | 2019 | [xvidcore-1.3.7.tar.gz](https://downloads.xvid.com/downloads/xvidcore-1.3.7.tar.gz) | No | [GNU General Public Licence (GPL) version 2](http://websvn.xvid.org/cvs/viewvc.cgi/trunk/xvidcore/LICENSE?revision=851) |
| [libfdk-aac](https://github.com/mstorsjo/fdk-aac) | [2.0.3](https://github.com/mstorsjo/fdk-aac/tags) | 2023-12-21 | [fdk-aac-2.0.3.tar.gz](https://github.com/mstorsjo/fdk-aac/archive/refs/tags/v2.0.3.tar.gz) | No | [Liberal but not a license of patented technologies](https://github.com/mstorsjo/fdk-aac/blob/master/NOTICE) |
| [openjpeg](https://github.com/uclouvain/openjpeg) | [2.5.2](https://github.com/uclouvain/openjpeg/releases) | 2024-02-28 | [openjpeg-2.5.2.tar.gz](https://github.com/uclouvain/openjpeg/archive/refs/tags/v2.5.2.tar.gz) | No | [BSD-style license](https://github.com/uclouvain/openjpeg/blob/master/LICENSE) |
| [freetype](https://www.freetype.org/) | [2.13.3](http://download.savannah.gnu.org/releases/freetype/) | 2024-08-12 | [freetype-2.13.3.tar.gz](http://download.savannah.gnu.org/releases/freetype/freetype-2.13.3.tar.gz) | No | [GNU General Public License (GPL) version 2](https://www.freetype.org/license.html) |
| [libvidstab](https://github.com/georgmartius/vid.stab) | [1.1.1](https://github.com/georgmartius/vid.stab/tags) | 2022-05-30 | [vid.stab-1.1.1.tar.gz](https://github.com/georgmartius/vid.stab/archive/v1.1.1.tar.gz) | No | [GNU General Public License (GPL) version 2](https://github.com/georgmartius/vid.stab/blob/master/LICENSE) |
| [fontconfig](https://www.freedesktop.org/wiki/Software/fontconfig/) | [2.15.0](https://www.freedesktop.org/software/fontconfig/release/) | 2023-12-22 | [fontconfig-2.15.0.tar.gz](https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.15.0.tar.gz) | No | []() |
| [kvazaar](https://github.com/ultravideo/kvazaar) | [2.3.1](https://github.com/ultravideo/kvazaar/releases) | 2024-04-10 | [kvazaar-2.3.1.tar.gz](https://github.com/ultravideo/kvazaar/releases/download/v2.3.1/kvazaar-2.3.1.tar.gz) | No | [BSD 3-Clause](https://github.com/ultravideo/kvazaar/blob/master/LICENSE`) |
| [aom](https://aomedia.googlesource.com/aom) | [3.10.0](https://aomedia.googlesource.com/aom/+refs) | 2024-08-01 |  | No | [Alliance for Open Media](https://aomedia.org/license/software-license/) |
| [nvidia-codec-headers](https://github.com/FFmpeg/nv-codec-headers) | [12.2.72.0]() | 2024-03-31 | [nv-codec-headers-12.2.72.0.tar.gz](https://github.com/FFmpeg/nv-codec-headers/releases/download/n12.2.72.0/nv-codec-headers-12.2.72.0.tar.gz) | No | []() |
| [libsvtav1](https://gitlab.com/AOMediaCodec/SVT-AV1) | [2.2.1](https://gitlab.com/AOMediaCodec/SVT-AV1/-/tags) | 2024-08-01 | [SVT-AV1-v2.2.1.tar.gz](https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v2.2.1/SVT-AV1-v2.2.1.tar.gz) | No | [BSD 3-Clause Clear License](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/LICENSE.md?ref_type=heads) |
| [xproto](https://www.x.org/releases/individual/proto/) | [7.0.31](https://www.x.org/releases/individual/proto/) | 2016-09-23 | [xproto-7.0.31.tar.gz](https://www.x.org/releases/individual/proto/xproto-7.0.31.tar.gz) | No | [The MIT License](https://opensource.org/licenses/MIT) |
| [libpthread-stubs](https://www.x.org/releases/individual/lib/) | [0.5](https://www.x.org/releases/individual/lib/) | 2023-07-18 | [libpthread-stubs-0.5.tar.xz](https://www.x.org/releases/individual/lib/libpthread-stubs-0.5.tar.xz) | No | [The MIT License](https://opensource.org/licenses/MIT) |
| [libbluray](https://www.videolan.org/developers/libbluray.html) | [1.3.4](https://download.videolan.org/pub/videolan/libbluray/) | 2022-11-26 | [libbluray-1.3.4.tar.bz2](https://download.videolan.org/pub/videolan/libbluray/1.3.4/libbluray-1.3.4.tar.bz2) | No | [GNU General Public License (GPL) version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| [libzmq](https://github.com/zeromq/libzmq/) | [4.3.5](https://github.com/zeromq/libzmq/releases/) | 2023-10-9 | [zeromq-4.3.5.tar.gz](https://github.com/zeromq/libzmq/releases/download/v4.3.5/zeromq-4.3.5.tar.gz) | No | [Mozilla Public License (MPL) version 2.0](https://github.com/zeromq/libzmq/blob/v4.3.5/LICENSE) |
| [libaribb24](https://github.com/nkoriyama/aribb24/) | [1.0.3](https://github.com/nkoriyama/aribb24/releases) | 2014-08-18 | [aribb24-v1.0.3.tar.gz](https://github.com/nkoriyama/aribb24/archive/refs/tags/v1.0.3.tar.gz) | No | [GNU Lesser General Public License (LGPL) version 2.1 or newer](https://github.com/nkoriyama/aribb24/issues/9) |
| [zimg](https://github.com/sekrit-twc/zimg) | [3.0.5](https://github.com/sekrit-twc/zimg/releases) | 2023-6-30 | [zimg-3.0.5.tar.gz](https://github.com/sekrit-twc/zimg/archive/refs/tags/release-3.0.5.tar.gz) | No | [WTFPL](https://github.com/sekrit-twc/zimg?tab=WTFPL-1-ov-file) |
| [libtheora](https://xiph.org/downloads/) | [1.1.1](https://xiph.org/downloads/) | 2010-01-25 | [libtheora-1.1.1.tar.gz](https://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.gz) | No | [BSD-style license](https://git.xiph.org/?p=mirrors/theora.git;a=blob_plain;f=COPYING;hb=HEAD) |
| [libsrt](https://github.com/Haivision/srt) | [1.5.3](https://github.com/Haivision/srt/releases/) | 2023-09-07 | [srt-v1.5.3.tar.gz](https://github.com/Haivision/srt/archive/refs/tags/v1.5.3.tar.gz) | No | [Mozilla Public License (MPL) version 2.0](https://github.com/Haivision/srt/blob/master/LICENSE) |
| [libvmaf](https://github.com/Netflix/vmaf) | [3.0.0](https://github.com/Netflix/vmaf/releases) | 2023-12-07 | [vmaf-v3.0.0.tar.gz](https://github.com/Netflix/vmaf/archive/refs/tags/v3.0.0.tar.gz) | No | [BSD-2-Clause](https://github.com/Netflix/vmaf/blob/master/LICENSE) |
| [ffmpeg-7.1](http://ffmpeg.org/) | [7.1](http://ffmpeg.org/releases/) | 2024-09-30 | [ffmpeg-7.1.tar.bz2](https://ffmpeg.org/releases/ffmpeg-7.1.tar.bz2) | No | [GNU Lesser General Public License (LGPL) version 2.1](https://ffmpeg.org/legal.html) |
| [ffmpeg-7.0](http://ffmpeg.org/) | [7.0](http://ffmpeg.org/releases/) | 2024-04-05 | [ffmpeg-7.0.tar.bz2](https://ffmpeg.org/releases/ffmpeg-7.0.tar.bz2) | No | [GNU Lesser General Public License (LGPL) version 2.1](https://ffmpeg.org/legal.html) |
| [ffmpeg-6.1](http://ffmpeg.org/) | [6.1](http://ffmpeg.org/releases/) | 2023-11-11 | [ffmpeg-6.1.tar.bz2](https://ffmpeg.org/releases/ffmpeg-6.1.tar.bz2) | No | [GNU Lesser General Public License (LGPL) version 2.1](https://ffmpeg.org/legal.html) |



## Contribute

See [the contributing guide](CONTRIBUTING.md)



## Legal

Those docker images use code of <a href=http://ffmpeg.org>FFmpeg</a> licensed under the <a href=http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>LGPLv2.1</a> and their source can be downloaded on <a href=https://github.com/jrottenberg/ffmpeg>github.com/jrottenberg/ffmpeg</a>.
