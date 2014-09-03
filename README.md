FFMPEG for Docker on Centos6
============================

This repo has a Dockerfile to create a Docker image wth FFMPEG. It compiles FFMPEG from sources following instructions from the [Centos Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can likely be used as a base for a networked encoding farm, based on centos.

Test
----

```
$ docker run jrottenberg/ffmpeg
 ffmpeg version 2.3.3 Copyright (c) 2000-2014 the FFmpeg developers
  built on Aug 29 2014 23:44:42 with gcc 4.4.7 (GCC) 20120313 (Red Hat 4.4.7-4)
  configuration: --prefix=/opt/src --extra-cflags=-I/opt/src/include --extra-ldflags=-L/opt/src/lib --bindir=/usr/local/bin --extra-libs=-ldl --enable-version3 --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-libxvid --enable-gpl --enable-postproc --enable-nonfree --enable-avresample
  libavutil      52. 92.100 / 52. 92.100
  libavcodec     55. 69.100 / 55. 69.100
  libavformat    55. 48.100 / 55. 48.100
  libavdevice    55. 13.102 / 55. 13.102
  libavfilter     4. 11.100 /  4. 11.100
  libavresample   1.  3.  0 /  1.  3.  0
  libswscale      2.  6.100 /  2.  6.100
  libswresample   0. 19.100 /  0. 19.100
  libpostproc    52.  3.100 / 52.  3.100
Hyper fast Audio and Video encoder
```

Capture output from the container to the host running the command

```
 docker run jrottenberg/ffmpeg ffmpeg \
            -i http://url/to/media.mp4 \
            -stats \
            $ffmpeg_options    -   > out.mp4
```

### Example

```
 docker run jrottenberg/ffmpeg ffmpeg -stats  \
        -i http://archive.org/download/thethreeagesbusterkeaton/Buster.Keaton.The.Three.Ages.ogv \
        -loop 0  \
        -final_delay 500 -c:v gif -f gif -ss 00:49:42 -t 5 - > trow_ball.gif
```
