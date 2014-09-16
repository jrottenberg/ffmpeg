FFMPEG for Docker on Centos6
============================

This repo has a Dockerfile to create a Docker image wth FFMPEG. It compiles FFMPEG from sources following instructions from the [Centos Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos).

You can install the latest build of this image by running `docker pull jrottenberg/ffmpeg`.

This image can likely be used as a base for a networked encoding farm, based on centos.

Test
----

```
$ docker run jrottenberg/ffmpeg
 ffmpeg version 2.4 Copyright (c) 2000-2014 the FFmpeg developers
  built on Sep 16 2014 18:39:18 with gcc 4.4.7 (GCC) 20120313 (Red Hat 4.4.7-4)
  configuration: --prefix=/usr/local --extra-cflags=-I/usr/local/include --extra-ldflags=-L/usr/local/lib --bindir=/usr/local/bin --extra-libs=-ldl --enable-version3 --enable-libfaac --enable-libmp3lame --enable-libx264 --enable-libxvid --enable-gpl --enable-postproc --enable-nonfree --enable-avresample --enable-libfdk_aac --disable-debug --enable-small
  libavutil      54.  7.100 / 54.  7.100
  libavcodec     56.  1.100 / 56.  1.100
  libavformat    56.  4.101 / 56.  4.101
  libavdevice    56.  0.100 / 56.  0.100
  libavfilter     5.  1.100 /  5.  1.100
  libavresample   2.  1.  0 /  2.  1.  0
  libswscale      3.  0.100 /  3.  0.100
  libswresample   1.  1.100 /  1.  1.100
  libpostproc    53.  0.100 / 53.  0.100
Hyper fast Audio and Video encoder
[...]
```

Capture output from the container to the host running the command

```
 docker run jrottenberg/ffmpeg \
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

See what's inside the beast
---------------------------

```
$ docker run -ti --entrypoint='bash'  jrottenberg/ffmpeg
bash-4.1# ls -lsa /usr/local/bin/
total 46804
    4 drwxr-xr-x  2 root root     4096 Sep 16 18:39 .
    4 drwxr-xr-x 16 root root     4096 Sep 16 18:31 ..
 3040 -rwxr-xr-x  1 root root  3111725 Sep 16 18:33 faac
12204 -rwxr-xr-x  1 root root 12496224 Sep 16 18:39 ffmpeg
12144 -rwxr-xr-x  1 root root 12433632 Sep 16 18:39 ffprobe
11332 -rwxr-xr-x  1 root root 11603392 Sep 16 18:39 ffserver
  440 -rwxr-xr-x  1 root root   447593 Sep 16 18:32 lame
 2068 -rwxr-xr-x  1 root root  2116610 Sep 16 18:31 vsyasm
 1444 -rwxr-xr-x  1 root root  1474928 Sep 16 18:32 x264
 2068 -rwxr-xr-x  1 root root  2115439 Sep 16 18:31 yasm
 2056 -rwxr-xr-x  1 root root  2102781 Sep 16 18:31 ytasm
```
