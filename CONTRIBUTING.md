# Welcome to ffmpeg docker image contributing guide <!-- omit in toc -->

Thank you for investing your time in contributing to our project! Any contribution you make will be reflected on [jrottenberg/ffmpeg](https://github.com/jrottenberg/ffmpeg) :tada:.

Read our [Code of Conduct](./CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

In this guide you will get an overview of the contribution workflow from opening an issue, creating a PR, reviewing, and merging the PR.


## Opening an issue

Make sure you search exisiting issues, that there is no duplicate, before opening a new one. If you are raising a bug, give enough information so we can reproduce it locally:

- Command you ran
- Observed output
- Expected output


## Creating a PR

### Local change

Before you open a PR make the change locally and verify it passes pre-commit :


```sh
pip install pre-commit
pre-commit install # inside the local checkout
pre-commit run -a # to force a run, but it will execute on commits
```

Manual changes are expected in the `templates/` folder or `./update.py`

__Don't__ make changes directly into the _generated_ `docker-images/` folder. Updates are variant specific (`templates/Dockerfile-template.*`) or ffmpeg specific (`templates/Dockerfile-env` and `templates/Dockerfile-run`). Either way after a change, run `./update.py` to regenerate all the Dockerfile files.

If you forget and don't have pre-commit configured, the pre-commit step will fail anyway.


```sh
# Generates the Dockerfile for all variants
./update.py

pre-commit run -a # recommended

# Test a specific variant
docker build -t my-build docker-images/VERSION/

# Make sure all variants pass before CI
find ffmpeg/ -name Dockerfile | xargs dirname | parallel --no-notice -j 4 --results logs docker build -t {} {}
```

<details><summary>Some detailed examples, of building and running</summary>

If you are not running the amd64 platform, you may need to pass in the --platform flag to build with docker desktop
- 7.1-ubuntu2404

```sh
$ ./update.py; time docker build --platform linux/amd64 -t ffmpeg-7.1-ubuntu2404-desktop-build docker-images/7.1/ubuntu2404
$ docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest
```

- 7.1-ubuntu2404-edge

```sh
$ ./update.py; time docker build --platform linux/amd64 -t ffmpeg-7.1-ubuntu2404-edge-desktop-build docker-images/7.1/ubuntu2404-edge
$ docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-edge-desktop-build:latest
```

- 7.1-nvidia2404

```sh
$ ./update.py; time docker build --platform linux/amd64 -t ffmpeg-7.1-nvidia2404-desktop-build docker-images/7.1/nvidia2404
$ docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-nvidia2404-desktop-build:latest
```

- vaapi2404
```sh
$ ./update.py; time docker build --platform linux/amd64 -t ffmpeg-7.1-vaapi2404-desktop-build docker-images/7.1/vaapi2404
$ docker run -it --rm --entrypoint='bash' --platform="linux/amd64" ffmpeg-7.1-vaapi2404-desktop-build:latest
```

- alpine320
```sh
$ ./update.py; time docker build --platform linux/amd64 -t ffmpeg-7.1-alpine320-desktop-build docker-images/7.1/alpine320
$ docker run -it --rm --entrypoint='sh' --platform="linux/amd64" ffmpeg-7.1-alpine320-desktop-build:latest
```

```sh
$ ./update.py; time docker build --platform linux/amd64 -t ffmpeg-7.1-scratch320-desktop-build docker-images/7.1/scratch320
$ docker run -it --rm --entrypoint='sh' --platform="linux/amd64" ffmpeg-7.1-scratch320-desktop-build:latest
```

</details>

<details><summary>More testing notes</summary>


```
1: simply run the image: which should output the ffmpeg help
`docker run -it --rm --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest`

2: now run the image in bash
`docker run -it --rm --entrypoint=bash --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest`

In the bash shell, run the following commands
   $ ffmpeg
   $ ffmpeg -h
   $ ldd `which ffmpeg`
   Note: this next command on alipne will need to be modified to look in '/lib/' instead of '/usr/local/'
         but they are all there
   $ for i in ogg amr vorbis theora mp3lame opus vpx xvid fdk x264 x265;do echo $i; find /usr/local/ -name *$i*;done
   $ ffmpeg -buildconf

3: Convert an avi file to an mp4 file.
   `docker run --rm -v $(pwd):$(pwd) -w $(pwd) --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest -i drop_video_1.avi outfile/dv_converted.mp4`

4: Convert a asf file to an mp4
   `docker run --rm -v $(pwd):$(pwd) -w $(pwd) --platform="linux/amd64" ffmpeg-7.1-ubuntu2404-desktop-build:latest -i MU_2_Discharge_Bottle___Inlet_to_Discharge.asf outfile/mpu2_discharge_bottle_converted.mp4`

```

</details>

# Reviewing


To make reviews simpler, try to limit changes to one functionnality or bug fix (no `and`)


# Merging the PR


Working on that project is not my day job, although I do enjoy maintaining it, I can't guarantee a review the same day.

Don't hesitate to ping me if an issue has been opened for too long.
