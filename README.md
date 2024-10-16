# FFmpeg Docker image

[![Docker Stars](https://img.shields.io/docker/stars/jrottenberg/ffmpeg.svg?logo=docker&style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/stars/count/)
[![Docker pulls](https://img.shields.io/docker/pulls/jrottenberg/ffmpeg.svg?logo=docker&style=plastic)](https://registry.hub.docker.com/v2/repositories/jrottenberg/ffmpeg/)
[![Docker Automated build](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?logo=docker)](https://hub.docker.com/r/jrottenberg/ffmpeg/tags)
[![Github Container Registry Images](https://img.shields.io/badge/images-automated-blue?logo=github&style=plastic)](https://github.com/jrottenberg/ffmpeg/pkgs/container/ffmpeg)
[![gitlab pipeline status](https://gitlab.com/jrottenberg/ffmpeg/badges/main/pipeline.svg)](https://gitlab.com/jrottenberg/ffmpeg/commits/main)
[![Azure Build Status](https://dev.azure.com/video-tools/ffmpeg/_apis/build/status/jrottenberg.ffmpeg)](https://dev.azure.com/video-tools/ffmpeg/_build/latest?definitionId=1)


This project prepares a minimalist Docker image with FFmpeg. It compiles FFmpeg from sources following instructions from the [Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg:${VERSION}-${VARIANT}` or `docker pull ghcr.io/jrottenberg/ffmpeg:${VERSION}-${VARIANT}`.

This image can be used as a base for an encoding farm.

## Builds / Avaliabvle Docker Containers

There are different builds available:
Below is a table that provides examples for the nomenclature:

`ffmpeg-<version>-<os variant and version>`

| image name | OS ver | ffmpeg ver | variant | description 
| --- | --- | --- | --- | --- | 
| ffmpeg-7.1-ubuntu2404 | 24.04 | 7.1 | [ubuntu](https://releases.ubuntu.com/) | external libraries are installed from os packages, and ffmpeg is built from source. See [Ubunu Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu) for details on this. | 
| ffmpeg-7.0-ubuntu2404-edge | 24.04 | 7.0 | [ubuntu](https://releases.ubuntu.com/) | libs and ffmpeg are built from source. See [Ubunu Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu) for details on this. |
| ffmpeg-6.1-vaapi2404 | 24.04 | 6.1 | [ubuntu](https://releases.ubuntu.com/) | like: `ubuntu2404` but enables: [Video Acceleration API (VAAPI)](https://trac.ffmpeg.org/wiki/HWAccelIntro#VAAPI) in ffmpeg |
| ffmpeg-5.1-nvidia2204-edge | 22.04 | 5.1 | [ubuntu](https://releases.ubuntu.com/) | Built w/ [NVIDIA's hardware-accelerated encoding and decoding APIs](https://trac.ffmpeg.org/wiki/HWAccelIntro#CUDANVENCNVDEC) enabled |
| ffmpeg-7.1-alpine320 | 3.20 | 7.1 | [alpine](https://alpinelinux.org/releases/) | vendor libs, but ffmpeg is built from source |
| ffmpeg-7.0-scratch | 3.20 | 7.0 | [alpine](https://alpinelinux.org/releases/) | vendor libs, and ffmpeg are built from source. Also we make the distro as small as possible by not installing any packages in base and striping symbols of installed libs |

ffmpeg `<version>` can be one of the following: `5.1`, `6.1`, `7.0`, `7.1` with the above table.

Note: I changed the ffmpeg version number in the table above as an example of how this works. Probably best to stick with the latest ffmpeg.


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
$ python3 ./generate_list_of_recent_images.py > list_of_recent_images.txt
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

See [the contributing guide](CONTRIBUTING.md)



## Legal

Those docker images use code of <a href=http://ffmpeg.org>FFmpeg</a> licensed under the <a href=http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>LGPLv2.1</a> and their source can be downloaded on <a href=https://github.com/jrottenberg/ffmpeg>github.com/jrottenberg/ffmpeg</a>.
