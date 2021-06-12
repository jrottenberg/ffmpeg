#!/usr/bin/env python3


import os
import re
import shutil
from urllib import request
from distutils.version import StrictVersion

MIN_VERSION = "2.7"
with open("templates/Dockerfile-env", "r") as tmpfile:
    ENV_CONTENT = tmpfile.read()
with open("templates/Dockerfile-run", "r") as tmpfile:
    RUN_CONTENT = tmpfile.read()
DIR_FORMAT_STR = "docker-images/{0}/{1}"
IMAGE_FORMAT_STR = "{0}/Dockerfile".format(DIR_FORMAT_STR)
TEMPLATE_STR = "templates/Dockerfile-template.{0}"

# https://ffmpeg.org/olddownload.html
SKIP_VERSIONS = "3.1.11 3.0.12 snapshot"
VARIANTS = [
    {"name": "ubuntu1804", "parent": "ubuntu"},
    {"name": "ubuntu2004", "parent": "ubuntu"},
    {"name": "alpine312", "parent": "alpine"},
    {"name": "alpine38", "parent": "alpine"},
    {"name": "centos7", "parent": "centos"},
    {"name": "centos8", "parent": "centos"},
    {"name": "scratch312", "parent": "scratch"},
    {"name": "scratch38", "parent": "scratch"},
    {"name": "vaapi1804", "parent": "vaapi"},
    {"name": "vaapi2004", "parent": "vaapi"},
    {"name": "nvidia2004", "parent": "nvidia"},
]
FFMPEG_RELEASES = "https://ffmpeg.org/releases/"
gitlabci = []
azure = []

# Get latest release from ffmpeg.org
with request.urlopen(FFMPEG_RELEASES) as conn:
    ffmpeg_releases = conn.read().decode("utf-8")

parse_re = re.compile(r"ffmpeg-([.0-9]+).tar.bz2.asc</a>\s+")
all_versions = parse_re.findall(ffmpeg_releases)
all_versions.sort(key=StrictVersion, reverse=True)

version, all_versions = all_versions[0], all_versions[1:]

SKIP_VARIANTS = {
    "3.2": [
        "alpine312",
        "centos8",
        "nvidia2004",
        "scratch312",
        "ubuntu1804",
        "vaapi1804",
    ],
    "3.3": ["alpine38", "nvidia1604", "scratch38", "vaapi1804"],
    "3.4": ["alpine38", "nvidia1604", "scratch38", "vaapi1804"],
    "4.0": ["alpine38", "nvidia1604", "scratch38", "vaapi1804"],
    "4.1": ["alpine38", "nvidia1604", "scratch38", "vaapi1804"],
    "4.2": ["alpine38", "nvidia1604", "scratch38", "vaapi1804"],
}

last = version.split(".")
keep_version = []

keep_version.append(version)


def get_shorten_version(version):
    if version == "snapshot":
        return version
    else:
        major, minor, *patch = version.split(".")
        return f"{major}.{minor}"


def get_major_version(version):
    print(version)
    if version == "snapshot":
        return version
    else:
        major, minor, *patch = version.split(".")
        return f"{major}"


for cur in all_versions:
    if cur < MIN_VERSION:
        break

    if cur in SKIP_VERSIONS:
        break
    tmp = cur.split(".")
    # Check Minor
    if len(tmp) >= 2 and tmp[1].isdigit() and tmp[1] < last[1]:
        keep_version.append(cur)
        last = tmp
    # Check Major
    elif len(tmp) > 1 and tmp[0].isdigit() and tmp[0] < last[0]:
        keep_version.append(cur)
        last = tmp

print(f"Preparing docker images for ffmpeg versions : {keep_version}")


print(keep_version)
for version in keep_version:
    print(version)
    skip_variants = None
    for k, v in SKIP_VARIANTS.items():
        if version.startswith(k):
            skip_variants = v
    compatible_variants = [
        v for v in VARIANTS if skip_variants is None or v["name"] not in skip_variants
    ]
    short_version = get_shorten_version(version)
    major_version = get_major_version(version)
    ver_path = os.path.join("docker-images", short_version)
    for existing_variant in os.listdir(ver_path):
        if existing_variant not in compatible_variants:
            shutil.rmtree(DIR_FORMAT_STR.format(short_version, existing_variant))

    for variant in compatible_variants:
        siblings = [
            v["name"] for v in compatible_variants if v["parent"] == variant["parent"]
        ]
        is_parent = sorted(siblings, reverse=True)[0] == variant["name"]
        dockerfile = IMAGE_FORMAT_STR.format(short_version, variant["name"])
        gitlabci.append(
            f"""
{version}-{variant['name']}:
  extends: .docker
  stage: {variant['name']}
  variables:
    MAJOR_VERSION: {major_version}
    VERSION: "{short_version}"
    LONG_VERSION: "{version}"
    VARIANT: {variant['name']}
    PARENT: "{variant['parent']}"
    ISPARENT: "{is_parent}"
"""
        )

        azure.append(
            f"""
      {variant["name"]}_{version}:
        MAJOR_VERSION: {major_version}
        VERSION:  {short_version}
        LONG_VERSION: {version}
        VARIANT:  {variant["name"]}
        PARENT: {variant["parent"]}
        ISPARENT:  {is_parent}
"""
        )
        with open(TEMPLATE_STR.format(variant["name"]), "r") as tmpfile:
            template = tmpfile.read()

        FFMPEG_CONFIG_FLAGS = [
            "--disable-debug",
            "--disable-doc",
            "--disable-ffplay",
            "--enable-shared",
            "--enable-avresample",
            "--enable-libopencore-amrnb",
            "--enable-libopencore-amrwb",
            "--enable-gpl",
            "--enable-libass",
            "--enable-fontconfig",
            "--enable-libfreetype",
            "--enable-libvidstab",
            "--enable-libmp3lame",
            "--enable-libopus",
            "--enable-libtheora",
            "--enable-libvorbis",
            "--enable-libvpx",
            "--enable-libwebp",
            "--enable-libxcb",
            "--enable-libx265",
            "--enable-libxvid",
            "--enable-libx264",
            "--enable-nonfree",
            "--enable-openssl",
            "--enable-libfdk_aac",
            "--enable-postproc",
            "--enable-small",
            "--enable-version3",
            "--enable-libbluray",
            "--enable-libzmq",
            "--extra-libs=-ldl",
            '--prefix="${PREFIX}"',
        ]
        CFLAGS = [
            "-I${PREFIX}/include",
        ]
        LDFLAGS = [
            "-L${PREFIX}/lib",
        ]

        # OpenJpeg 2.1 is not supported in 2.8
        if version[0:3] != "2.8":
            FFMPEG_CONFIG_FLAGS.append("--enable-libopenjpeg")
            FFMPEG_CONFIG_FLAGS.append("--enable-libkvazaar")
        if version == "snapshot" or int(version[0]) > 3:
            FFMPEG_CONFIG_FLAGS.append("--enable-libaom")
            FFMPEG_CONFIG_FLAGS.append("--extra-libs=-lpthread")

        # LibSRT is supported from 4.0
        if version == "snapshot" or int(version[0]) >= 4:
            FFMPEG_CONFIG_FLAGS.append("--enable-libsrt")

        # LibARIBB24 is supported from 4.2
        if version == "snapshot" or float(version[0:3]) >= 4.2:
            FFMPEG_CONFIG_FLAGS.append("--enable-libaribb24")

        if ((template.find('meson') > 0) and (version == "snapshot" or float(version[0:3]) >= 4.3)):
            FFMPEG_CONFIG_FLAGS.append("--enable-libvmaf")

        if (version == "snapshot" or int(version[0]) >= 3) and variant[
            "parent"
        ] == "vaapi":
            FFMPEG_CONFIG_FLAGS.append("--enable-vaapi")

        if variant["parent"] == "nvidia":
            CFLAGS.append("-I${PREFIX}/include/ffnvcodec")
            CFLAGS.append("-I/usr/local/cuda/include/")
            LDFLAGS.append("-L/usr/local/cuda/lib64")
            LDFLAGS.append("-L/usr/local/cuda/lib32/")
            FFMPEG_CONFIG_FLAGS.append("--enable-nvenc")
            if version == "snapshot" or int(version[0]) >= 4:
                FFMPEG_CONFIG_FLAGS.append("--enable-cuda")
                FFMPEG_CONFIG_FLAGS.append("--enable-cuvid")
                FFMPEG_CONFIG_FLAGS.append("--enable-libnpp")
        cflags = '--extra-cflags="{0}"'.format(" ".join(CFLAGS))
        ldflags = '--extra-ldflags="{0}"'.format(" ".join(LDFLAGS))
        FFMPEG_CONFIG_FLAGS.append(cflags)
        FFMPEG_CONFIG_FLAGS.append(ldflags)
        FFMPEG_CONFIG_FLAGS[-1] += " && \\"
        COMBINED_CONFIG_FLAGS = " \\\n        ".join(FFMPEG_CONFIG_FLAGS)

        run_content = RUN_CONTENT.replace(
            "%%FFMPEG_CONFIG_FLAGS%%", COMBINED_CONFIG_FLAGS
        )
        env_content = ENV_CONTENT.replace("%%FFMPEG_VERSION%%", version)
        docker_content = template.replace("%%ENV%%", env_content)
        docker_content = docker_content.replace("%%RUN%%", run_content)

        d = os.path.dirname(dockerfile)
        if not os.path.exists(d):
            os.makedirs(d)

        with open(dockerfile, "w") as dfile:
            dfile.write(docker_content)


with open("docker-images/gitlab-ci.yml", "w") as gitlabcifile:
    gitlabcifile.write("".join(gitlabci))

with open("templates/azure.template", "r") as tmpfile:
    template = tmpfile.read()
azure = template.replace("%%VERSIONS%%", "\n".join(azure))


with open("docker-images/azure-jobs.yml", "w") as azurefile:
    azurefile.write(azure)
