FFMPEG for Docker on Centos6
=============================

This repo has a Dockerfile to create a Docker image wth FFMPEG. It compiles
FFMPEG from sources following instructions from the
[Centos Compilation Guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos).

You can install the latest build of this image by running
`docker pull jrottenberg/docker-ffmpeg-centos`.

This image can likely be used as a base for a networked encoding farm, based on centos.
