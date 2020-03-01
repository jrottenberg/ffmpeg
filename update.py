#!/usr/bin/env python3


import os
import sys
import re
import shutil
import urllib.request, urllib.error, urllib.parse
from distutils.version import StrictVersion

MIN_VERSION = "2.8"

# https://ffmpeg.org/olddownload.html
SKIP_VERSIONS = "3.1.11 3.0.12"

VARIANTS = [
    {
        "name": "ubuntu",
        "parent": "ubuntu",
    },
    {
        "name": "alpine",
        "parent": "alpine",
    },
    {
       "name": "centos7",
       "parent": "centos",
    },
    {
        "name": "centos8",
        "parent": "centos",
    },
    {
        "name": "scratch",
        "parent": "scratch",
    },
    {
        "name": "vaapi",
        "parent": "vaapi",
    },
    {
        "name": "nvidia",
        "parent": "nvidia",
    },
]
FFMPEG_RELEASES = "https://ffmpeg.org/releases/"

gitlabci = []
azure = []

# Get latest release from ffmpeg.org
with urllib.request.urlopen(FFMPEG_RELEASES) as conn:
    ffmpeg_releases = conn.read().decode("utf-8")

parse_re = re.compile("ffmpeg-([.0-9]+).tar.bz2.asc<\/a>\s+")
all_versions = parse_re.findall(ffmpeg_releases)
all_versions.sort(key=StrictVersion, reverse=True)

version, all_versions = all_versions[0], all_versions[1:]

SKIP_VARIANTS = {
    "3.2": ["centos8"]
}

last = version.split(".")
keep_version = ["snapshot"]

keep_version.append(version)

def shorten_version(version):
    if version == 'snapshot':
        return version
    else:
        return version[0:3]

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

for version in keep_version:
    skip_variants = None
    for k,v in SKIP_VARIANTS.items():
        if version.startswith(k):
            skip_variants = v
    compatible_variants = [v for v in VARIANTS if skip_variants is None or v['name'] not in skip_variants]
    short_version = shorten_version(version)
    for existing_variant in os.listdir(os.path.join('docker-images', short_version)):
        if existing_variant not in compatible_variants:
            shutil.rmtree(os.path.join('docker-images', short_version, existing_variant))

    for variant in compatible_variants:
        sibling_variants = [v['name'] for v in compatible_variants if v['parent'] == variant['parent']]
        
        is_parent =  sorted(sibling_variants, reverse=True)[0] == variant['name']
        dockerfile = "docker-images/%s/%s/Dockerfile" % (short_version, variant['name'])
        gitlabci.append(
            f"""
{version}-{variant['name']}:
  extends: .docker
  stage: {variant['name']}
  variables:
    VERSION: "{short_version}"
    VARIANT: {variant['name']}
    PARENT: "{variant['parent']}"
    ISPARENT: "{is_parent}"
"""
        )

        azure.append(
            "      %s_%s:\n        VERSION: %s\n        VARIANT: %s\n        PARENT: %s\n        ISPARENT: %s"
            % (short_version.replace(".", "_"), variant['name'], short_version, variant['name'], variant['parent'], is_parent)
        )

        with open("templates/Dockerfile-env", "r") as tmpfile:
            env_content = tmpfile.read()
        with open("templates/Dockerfile-template." + variant['name'], "r") as tmpfile:
            template = tmpfile.read()
        with open("templates/Dockerfile-run", "r") as tmpfile:
            run_content = tmpfile.read()
        env_content = env_content.replace("%%FFMPEG_VERSION%%", version)
        docker_content = template.replace("%%ENV%%", env_content)
        docker_content = docker_content.replace("%%RUN%%", run_content)
        # OpenJpeg 2.1 is not supported in 2.8
        if version[0:3] == "2.8":
            docker_content = docker_content.replace("--enable-libopenjpeg", "")
            docker_content = docker_content.replace("--enable-libkvazaar", "")
        if (version != "snapshot" and version[0] < "4"):
            docker_content = re.sub(r"--enable-libaom [^\\]*", "", docker_content)
        if (version == "snapshot" or version[0] >= "3") and variant['parent'] == "vaapi":
            docker_content = docker_content.replace(
                "--disable-ffplay", "--disable-ffplay \\\n        --enable-vaapi"
            )

        if variant['parent'] == "nvidia":
            docker_content = docker_content.replace(
                '--extra-cflags="-I${PREFIX}/include"',
                '--extra-cflags="-I${PREFIX}/include -I${PREFIX}/include/ffnvcodec -I/usr/local/cuda/include/"',
            )
            docker_content = docker_content.replace(
                '--extra-ldflags="-L${PREFIX}/lib"',
                '--extra-ldflags="-L${PREFIX}/lib -L/usr/local/cuda/lib64/ -L/usr/local/cuda/lib32/"',
            )
            if version == "snapshot" or version[0] >= "4":
                docker_content = docker_content.replace(
                    "--disable-ffplay",
                    "--disable-ffplay \\\n     	--enable-cuda \\\n        --enable-nvenc \\\n        --enable-cuvid \\\n        --enable-libnpp",
                )
            # Don't support hw decoding and scaling on older ffmpeg versions
            if version[0] < "4":
                docker_content = docker_content.replace(
                    "--disable-ffplay", "--disable-ffplay \\\n      --enable-nvenc"
                )
            # FFmpeg 3.2 and earlier don't compile correctly on Ubuntu 18.04 due to openssl issues
            if version[0] < "3" or (version[0] == "3" and version[2] < "3"):
                docker_content = docker_content.replace("-ubuntu18.04", "-ubuntu16.04")

        # FFmpeg 3.2 and earlier don't compile correctly on Ubuntu 18.04 due to openssl issues
        if variant['parent'] == "vaapi" and (
            version[0] < "3" or (version[0] == "3" and version[2] < "3")
        ):
            docker_content = docker_content.replace("ubuntu:18.04", "ubuntu:16.04")
            docker_content = docker_content.replace("libva-drm2", "libva-drm1")
            docker_content = docker_content.replace("libva2", "libva1")

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


with open("azure-pipelines.yml", "w") as azurefile:
    azurefile.write(azure)

