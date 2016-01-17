FFMPEG for Docker on Centos7
============================

This project prepares a minimalist Docker image with FFMPEG. It compiles FFMPEG from sources following instructions from the [Centos Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can be used as a base for an encoding farm, based on centos7.

Please use [Github issues](https://github.com/jrottenberg/ffmpeg/issues/new) to report any bug or missing feature.

Test
----

```
$ docker run jrottenberg/ffmpeg -buildconf
ffmpeg version 2.8.1 Copyright (c) 2000-2015 the FFmpeg developers
  built with gcc 4.8.3 (GCC) 20140911 (Red Hat 4.8.3-9)
  configuration: --prefix=/usr/local --extra-cflags=-I/usr/local/include --extra-ldflags=-L/usr/local/lib --bindir=/usr/local/bin --extra-libs=-ldl --enable-version3 --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-libxvid --enable-gpl --enable-postproc --enable-nonfree --enable-avresample --enable-libfdk_aac --disable-debug --enable-small --enable-openssl --enable-libtheora --enable-libx265 --enable-libopus --enable-libvorbis --enable-libvpx
  libavutil      54. 31.100 / 54. 31.100
  libavcodec     56. 60.100 / 56. 60.100
  libavformat    56. 40.101 / 56. 40.101
  libavdevice    56.  4.100 / 56.  4.100
  libavfilter     5. 40.101 /  5. 40.101
  libavresample   2.  1.  0 /  2.  1.  0
  libswscale      3.  1.101 /  3.  1.101
  libswresample   1.  2.101 /  1.  2.101
  libpostproc    53.  3.100 / 53.  3.100

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

-	FFMPEG_VERSION 2.8.5 https://github.com/FFmpeg/FFmpeg/blob/master/Changelog
-	YASM_VERSION 1.3.0 https://github.com/yasm/yasm/releases
-	OGG_VERSION 1.3.2 https://xiph.org/downloads/
-	VORBIS_VERSION 1.3.5 https://xiph.org/downloads/
-	THEORA_VERSION 1.1.1 https://xiph.org/downloads/
-	LAME_VERSION 3.99.5 http://lame.sourceforge.net/download.php
-	OPUS_VERSION 1.1.1 https://www.opus-codec.org/downloads/
-	FAAC_VERSION 1.28 http://www.audiocoding.com/downloads.html
-	VPX_VERSION 1.5.0 https://github.com/webmproject/libvpx/releases
-	XVID_VERSION 1.3.4 https://labs.xvid.com/source/
-	FDKAAC_VERSION 0.1.4 https://github.com/mstorsjo/fdk-aac/releases
-	X265_VERSION 1.8 https://bitbucket.org/multicoreware/x265/downloads
