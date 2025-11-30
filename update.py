#!/usr/bin/env python3

import datetime
import json
import os
import shutil
from urllib import request

FFMPEG_RELEASES = "https://endoflife.date/api/ffmpeg.json"

DIR_FORMAT_STR = "docker-images/{0}/{1}"
IMAGE_FORMAT_STR = "{0}/Dockerfile".format(DIR_FORMAT_STR)
TEMPLATE_STR = "templates/Dockerfile-template.{0}"

# https://ffmpeg.org/olddownload.html
# https://endoflife.date/ffmpeg
# We use the endoflife.date API to find the most recent ffmpeg versions. However,
# to simplify image maintenance, we only consider versions released within the
# last YEARS years (currently set to 3). Including very older versions compatibility
# issues with different libraries and operating system versions. By focusing on
# recent versions, we keep things manageable.
# Note: the older builds will be preserved in the the docker hub registry.
RELEASED_YEARS_AGO = 3
KEEP_VERSION = "8."


def is_too_old(date_str, years):
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    diff = datetime.datetime.now() - date_obj
    # Check if the difference is more than x years
    return diff.days > (years * 365)


def get_eol_versions():
    keep_version = []
    with request.urlopen(FFMPEG_RELEASES) as conn:
        ffmpeg_releases = conn.read().decode("utf-8")

    for v in json.loads(ffmpeg_releases):
        if not v["eol"]:
            if "0.0" in v["latest"]:
                v["latest"] = v["latest"].replace("0.0", "0")
            release_date = v["latestReleaseDate"]
            if not is_too_old(release_date, years=RELEASED_YEARS_AGO) and v[
                "latest"
            ].startswith(KEEP_VERSION):
                keep_version.append(v["latest"])
    return keep_version


keep_version = get_eol_versions()
print("The following versions of ffmpeg is still supported:")
for version in keep_version:
    print(version)

# Determine the latest version for "latest" tag
latest_version = keep_version[-1] if keep_version else None
print(f"Latest version for 'latest' tag: {latest_version}")

VARIANTS = [
    {"name": "ubuntu2404", "parent": "ubuntu"},
    {"name": "ubuntu2404-edge", "parent": "ubuntu-edge"},
    {"name": "alpine320", "parent": "alpine"},
    {"name": "scratch320", "parent": "scratch"},
    # Video Acceleration API (VAAPI) https://trac.ffmpeg.org/wiki/HWAccelIntro#VAAPI
    {"name": "vaapi2404", "parent": "vaapi"},
    {"name": "nvidia2404", "parent": "nvidia"},
]
current_variant_names = [v["name"] for v in VARIANTS]

# Define which variant should be tagged as "latest" (Ubuntu LTS)
LATEST_VARIANT = "ubuntu2404"


all_parents = sorted(set([sub["parent"] for sub in VARIANTS]))
gitlabci = ["stages:\n  - lint\n"]
azure = []

for parent in all_parents:
    gitlabci.append(f"  - {parent}\n")

# Note: Skip variants and the is_too_old(), work together to allow us to skip things
#       Skip variants allow us to skip some variants for specific versions
#       is_too_old() check allow us to skip versions that are too old
SKIP_VARIANTS = {
    "2.8": ["nvidia2204", "vaapi2204"] + [v["name"] for v in VARIANTS],
    "3.4": ["alpine313", "nvidia2204", "scratch313", "vaapi2204"]
    + [v["name"] for v in VARIANTS],
    "4.2": ["alpine313", "ubuntu2404"] + [v["name"] for v in VARIANTS],
    "4.3": ["nvidia2204", "vaapi2204"] + [v["name"] for v in VARIANTS],
    "4.4": ["alpine313", "nvidia2204", "scratch313"] + [v["name"] for v in VARIANTS],
    "5.1": [v["name"] for v in VARIANTS],
    "6.1": [
        "nvidia2404",
        "scratch320",
    ],  # failing from long build times ( over an hour )
    "7.0": [],
    "7.1": [],
}


def get_shorten_version(version):
    if version == "snapshot":
        return version
    else:
        major, minor, *patch = version.split(".")
        return f"{major}.{minor}"


def get_major_version(version):
    if version == "snapshot":
        return version
    else:
        major, minor, *patch = version.split(".")
        return f"{major}"


def read_ffmpeg_template(variant_name, env_or_run="env"):
    """Read the ffmpeg template file and return the content"""
    if variant_name == "scratch":
        distro_name = "alpine-scratch"
    elif variant_name == "alpine":
        distro_name = "alpine"
    elif variant_name == "ubuntu-edge":
        distro_name = "ubuntu-edge"
    elif variant_name == "nvidia":
        distro_name = "nvidia"
    elif variant_name == "vaapi":
        distro_name = "vaapi"
    else:
        distro_name = "ubuntu"

    with open(f"templates/Dockerfile-{env_or_run}-{distro_name}", "r") as tmpfile:
        return tmpfile.read()


print("Preparing docker images for ffmpeg versions: ")


for version in keep_version:
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
    os.makedirs(ver_path, exist_ok=True)
    for existing_variant in os.listdir(ver_path):
        if existing_variant not in compatible_variants:
            shutil.rmtree(
                DIR_FORMAT_STR.format(short_version, existing_variant),
                ignore_errors=True,
            )

    print(f"Preparing Dockerfile for ffmpeg-{version}")
    for variant in compatible_variants:
        print(f"{' '*25}{version}-{variant['name']}")

        ENV_CONTENT = read_ffmpeg_template(variant["parent"], "env")
        RUN_CONTENT = read_ffmpeg_template(variant["parent"], "run")

        siblings = [
            v["name"] for v in compatible_variants if v["parent"] == variant["parent"]
        ]
        is_parent = sorted(siblings, reverse=True)[0] == variant["name"]
        # Determine if this should be tagged as "latest"
        is_latest = version == latest_version and variant["name"] == LATEST_VARIANT
        dockerfile = IMAGE_FORMAT_STR.format(short_version, variant["name"])
        gitlabci.append(
            f"""
{version}-{variant['name']}:
  extends: .docker
  stage: {variant['parent']}
  variables:
    MAJOR_VERSION: {major_version}
    VERSION: "{short_version}"
    LONG_VERSION: "{version}"
    VARIANT: {variant['name']}
    PARENT: "{variant['parent']}"
    ISPARENT: "{is_parent}"
    ISLATEST: "{is_latest}"
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
        ISLATEST:  {is_latest}
"""
        )
        # with open(
        #     TEMPLATE_STR.format(variant["name"].replace("-edge", "")), "r"
        # ) as tmpfile:
        #     template = tmpfile.read()
        with open(TEMPLATE_STR.format(variant["name"]), "r") as tmpfile:
            template = tmpfile.read()

        FFMPEG_CONFIG_FLAGS = [
            "--disable-debug",
            "--disable-doc",
            "--disable-ffplay",
            "--enable-shared",
            "--extra-libs=-ldl",
            "--enable-gpl",
            "--enable-fontconfig",
            "--enable-libass",
            "--enable-libbluray",
            # https://ffmpeg.org/ffmpeg-filters.html#drawtext-1
            "--enable-libfreetype",
            "--enable-libharfbuzz",
            "--enable-libfontconfig",
            "--enable-libfribidi",
            "--enable-libmp3lame",
            "--enable-libopencore-amrnb",
            "--enable-libopencore-amrwb",
            "--enable-libopus",
            "--enable-libtheora",
            "--enable-libvidstab",
            "--enable-libvorbis",
            "--enable-libvpx",
            "--enable-libwebp",
            "--enable-libx264",
            "--enable-libx265",
            "--enable-libxvid",
            "--enable-libzimg",
            "--enable-libzmq",
            "--enable-nonfree",
            "--enable-openssl",
            "--enable-small",
            "--enable-version3",
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

        if (template.find("meson") > 0) and (
            version == "snapshot" or float(version[0:3]) >= 4.3
        ):
            FFMPEG_CONFIG_FLAGS.append("--enable-libvmaf")

        if (version == "snapshot" or int(version[0]) >= 3) and variant[
            "parent"
        ] == "vaapi":
            FFMPEG_CONFIG_FLAGS.append("--enable-vaapi")

        # libavresample removed on v5, deprecated since v4.0
        # https://github.com/FFmpeg/FFmpeg/commit/c29038f3041a4080342b2e333c1967d136749c0f
        if float(version[0]) < 5:
            FFMPEG_CONFIG_FLAGS.append("--enable-avresample")

        if variant["parent"] == "nvidia":
            CFLAGS.append("-I${PREFIX}/include/ffnvcodec")
            CFLAGS.append("-I/usr/local/cuda/include/")
            LDFLAGS.append("-L/usr/local/cuda/lib64")
            LDFLAGS.append("-L/usr/local/cuda/lib32/")
            FFMPEG_CONFIG_FLAGS.append("--enable-nvenc")
            FFMPEG_CONFIG_FLAGS.append("--enable-cuda-nvcc")
            if version == "snapshot" or int(version[0]) >= 4:
                FFMPEG_CONFIG_FLAGS.append("--enable-cuda")
                FFMPEG_CONFIG_FLAGS.append("--enable-cuvid")
                FFMPEG_CONFIG_FLAGS.append("--enable-libnpp")

        if float(version[0:3]) >= 5.1:
            # from https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#FFmpeg
            FFMPEG_CONFIG_FLAGS.append("--extra-libs=-lm")  # add math library
            FFMPEG_CONFIG_FLAGS.append("--ld=g++")  # use g++ as linker

            # DELETE NEXT 5 LINES when everything works
            # --extra-cflags="-I/usr/local/include -I/usr/lib/include" \
            # --extra-cxxflags="-I/usr/local/include -I/usr/lib/include" \
            # --extra-ldflags="-L/usr/local/lib" \
            # --extra-ldflags="-L/usr/local/lib64 -L/usr/lib -L/usr/lib64" \
            # FFMPEG_CONFIG_FLAGS.append("--extra-ldflags=-L/usr/local/lib \
            # -L/usr/local/lib64 -L/usr/lib -L/usr/lib64")

            # Some shenagians to get libvmaf to build with static linking
            FFMPEG_CONFIG_FLAGS.append(
                "--extra-ldflags=-L/opt/ffmpeg/lib/x86_64-linux-gnu"
            )

            # --ld=g++ or --ld=clang++ when configuring ffmpeg
            # FFMPEG_CONFIG_FLAGS.append("--pkg-config-flags='--static'")
            # FFMPEG_CONFIG_FLAGS.append("--enable-static")
            # FFMPEG_CONFIG_FLAGS.append("--enable-gnutls")
            FFMPEG_CONFIG_FLAGS.append("--enable-libfdk-aac")
            FFMPEG_CONFIG_FLAGS.append("--enable-libsvtav1")
            FFMPEG_CONFIG_FLAGS.append("--enable-libdav1d")
        else:  # for older versions
            FFMPEG_CONFIG_FLAGS.append(
                "--enable-libfdk_aac"
            )  # this was likely misstyped before

        # if "ubuntu" in variant["parent"] and float(version[0:3]) >= 5.1:
        if float(version[0:3]) >= 5.1:
            CFLAGS.append("-I/usr/include/x86_64-linux-gnu")
            LDFLAGS.append("-L/usr/lib/x86_64-linux-gnu")
            LDFLAGS.append("-L/usr/lib")  # for alpine ( but probably fine for all)

        if float(version[0:1]) >= 8:
            FFMPEG_CONFIG_FLAGS.append("--enable-whisper")

        cflags = '--extra-cflags="{0}"'.format(" ".join(CFLAGS))
        ldflags = '--extra-ldflags="{0}"'.format(" ".join(LDFLAGS))
        FFMPEG_CONFIG_FLAGS.append(cflags)
        FFMPEG_CONFIG_FLAGS.append(ldflags)
        FFMPEG_CONFIG_FLAGS.sort()

        COMBINED_CONFIG_FLAGS = " \\\n        ".join(FFMPEG_CONFIG_FLAGS)
        # run content needs two replace statements
        run_content_flags = RUN_CONTENT.replace(
            "%%FFMPEG_CONFIG_FLAGS%%", COMBINED_CONFIG_FLAGS
        )
        run_content = run_content_flags.replace("%%FFMPEG_VERSION%%", version[0:3])

        env_content = ENV_CONTENT.replace("%%FFMPEG_VERSION%%", version)
        docker_content = template.replace("%%ENV%%", env_content)
        docker_content = docker_content.replace("%%RUN%%", run_content)

        ddir = os.path.dirname(dockerfile)
        if not os.path.exists(ddir):
            os.makedirs(ddir)

        with open(dockerfile, "w") as dfile:
            dfile.write(docker_content)

        # These 4 files are used this for everything as even the packaged
        # builds require building ffmpeg.
        shutil.copy("generate-source-of-truth-ffmpeg-versions.py", ddir)
        shutil.copy("download_tarballs.sh", ddir)
        shutil.copy("install_ffmpeg.sh", ddir)
        # for build_source.sh, we are not going to just copy the file, we are going
        # to replace the FFMPEG_CONFIG_FLAGS
        with open("build_source.sh", "r") as tmpfile:
            template = tmpfile.read()
            build_source_content = template.replace(
                "%%FFMPEG_CONFIG_FLAGS%%", COMBINED_CONFIG_FLAGS
            )
            os.chmod("build_source.sh", 0o755)

        with open(f"{ddir}/build_source.sh", "w") as buildfile:
            buildfile.write(build_source_content)
            os.chmod(f"{ddir}/build_source.sh", 0o755)


with open("docker-images/gitlab-ci.yml", "w") as gitlabcifile:
    gitlabcifile.write("".join(gitlabci))

with open("templates/azure.template", "r") as tmpfile:
    template = tmpfile.read()
azure = template.replace("%%VERSIONS%%", "\n".join(azure))


with open("docker-images/azure-jobs.yml", "w") as azurefile:
    azurefile.write(azure)
