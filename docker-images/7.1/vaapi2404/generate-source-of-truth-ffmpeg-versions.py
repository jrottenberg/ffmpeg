#!/usr/bin/env python3

import argparse
import json
import sys
from collections import OrderedDict

"""
------- Purpose -------
...This is the source of truth...
1. This script generates a table of the libraries used by FFMPEG that
   will be included in the main README.md file of the repository.
2. This script generates a 'build_manifest.json' file that contains the
   the download links, build directories, and build tarball names for
    each library. ( Required to generate a robust re-try download of the package tarballs)

------- Setup -------
This script is run in the container to generate 'build_manifest.json'
However, it is also used to generate a generated_versions_table.md file.
The steps for doing that are below.
To run this script you need the ?? library. You can install it with pip:
in a venv as follows:

$ python3 -mvenv .venv
$ source .venv/bin/activate
$ pip install ??
$ python3 ./generate-source-of-truth-ffmpeg-versions.py
$ deactivate
$ rm -rf .venv

The output of this script will be a table in markdown format, which you can
paste into the README.md file of the repository.
"""

# Library versions Source of truth
FFMPEG_71 = {"version": "7.1", "release_date": "2024-09-30"}
FFMPEG_70 = {"version": "7.0", "release_date": "2024-04-05"}
FFMPEG_61 = {"version": "6.1", "release_date": "2023-11-11"}
# FFMPEG_51 = {"version": "5.1", "release_date": "2022-06-22"}
OGG = {"version": "1.3.5", "release_date": "2021-06-04"}
OPENCOREAMR = {"version": "0.1.6", "release_date": "2022-08-01"}
VORBIS = {"version": "1.3.7", "release_date": "2020-07-04"}
THEORA = {"version": "1.1.1", "release_date": "2010"}
LAME = {"version": "3.100", "release_date": "2017-10-13"}
OPUS = {"version": "1.5.2", "release_date": "2024-04-12"}
VPX = {"version": "1.14.1", "release_date": "2024-05-30"}
WEBP = {"version": "1.4.0", "release_date": "2024-04-13"}
XVID = {"version": "1.3.7", "release_date": "2019"}
FDKAAC = {"version": "2.0.3", "release_date": "2023-12-21"}
FREETYPE = {"version": "2.13.3", "release_date": "2024-08-12"}
LIBVIDSTAB = {"version": "1.1.1", "release_date": "2022-05-30"}
LIBFRIDIBI = {"version": "1.0.16", "release_date": "2024-10-1"}
FONTCONFIG = {"version": "2.15.0", "release_date": "2023-12-22"}
LIBASS = {"version": "0.17.3", "release_date": "2024-07-02"}
KVAAZAAR = {"version": "2.3.1", "release_date": "2024-04-10"}
AOM = {"version": "3.10.0", "release_date": "2024-08-01"}
NV_CODEC = {"version": "12.2.72.0", "release_date": "2024-03-31"}
SVTAV1 = {"version": "2.2.1", "release_date": "2024-08-01"}
XORG_MACROS = {"version": "1.20.1", "release_date": "2024-04-16"}
XPROTO = {"version": "7.0.31", "release_date": "2016-09-23"}
XAU = {"version": "1.0.11", "release_date": "2022-12-08"}
PTHREAD_STUBS = {"version": "0.5", "release_date": "2023-07-18"}
LIBXML2 = {"version": "2.13.4", "release_date": "2024-09-01"}
LIBBLURAY = {"version": "1.3.4", "release_date": "2022-11-26"}
X264 = {"version": "20191217-2245-stable", "release_date": "2019-12-17"}
X265 = {"version": "4.0", "release_date": "2024-09-13"}
LIBZMQ = {"version": "4.3.5", "release_date": "2023-10-9"}
LIBSRT = {"version": "1.5.3", "release_date": "2023-09-07"}
LIBPNG = {"version": "1.6.44", "release_date": "2024-09-12"}
ZIMG = {"version": "3.0.5", "release_date": "2023-6-30"}
LIBARIBB24 = {"version": "1.0.3", "release_date": "2014-08-18"}
OPENJPEG = {"version": "2.5.2", "release_date": "2024-02-28"}
THEORA = {"version": "1.1.1", "release_date": "2010-01-25"}
LIBVMAF = {"version": "3.0.0", "release_date": "2023-12-07"}

# Library details, Source of truth
# TODO: store this in a yaml confiuration file ( would probably be better )
# flake8: noqa E501
LIBRARIES = OrderedDict(
    [
        (
            "libopencore-amr",
            {
                "link": "https://sourceforge.net/projects/opencore-amr/",
                "version": OPENCOREAMR["version"],
                "version_link": "https://sourceforge.net/projects/opencore-amr/files/opencore-amr/",
                "release_date": OPENCOREAMR["release_date"],
                "license_name": "Apache License",
                "license_link": "https://sourceforge.net/p/opencore-amr/code/ci/master/tree/LICENSE",
                "build_info": {
                    # this one of the finikie download link's ( and the reason we wrote the download_tarball.sh script)
                    "download_link": f"https://sourceforge.net/projects/opencore-amr/files/opencore-amr/opencore-amr-{OPENCOREAMR['version']}.tar.gz",
                    "build_dir": "/tmp/libopencore-amr",
                    "tarball_name": f"opencore-amr-{OPENCOREAMR['version']}.tar.gz",
                },
            },
        ),
        (
            "libx264",
            {
                "link": "https://www.videolan.org/developers/x264.html",
                "version": X264["version"],
                "version_link": "https://download.videolan.org/pub/videolan/x264/snapshots/",
                "release_date": X264["release_date"],
                "license_name": "GNU General Public License (GPL) version 2",
                "license_link": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
                "build_info": {
                    "download_link": f"https://download.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-{X264['version']}.tar.bz2",
                    "build_dir": "/tmp/x264",
                    "tarball_name": f"x264-snapshot-{X264['version']}.tar.bz2",
                },
            },
        ),
        (
            "libx265",
            {
                "link": "http://x265.org/",
                "version": X265["version"],
                "version_link": "http://ftp.videolan.org/pub/videolan/x265/",  # "https://www.x265.org/downloads/",
                "release_date": X265["release_date"],
                "license_name": "GNU General Public License (GPL) version 2",
                "license_link": "https://bitbucket.org/multicoreware/x265/raw/f8ae7afc1f61ed0db3b2f23f5d581706fe6ed677/COPYING",
                "build_info": {
                    "download_link": f"http://ftp.videolan.org/pub/videolan/x265/x265_{X265['version']}.tar.gz",
                    "build_dir": "/tmp/x265",
                    "tarball_name": f"x265_{X265['version']}.tar.gz",
                },
            },
        ),
        (
            "libogg",
            {
                "link": "https://www.xiph.org/ogg/",
                "version": OGG["version"],
                "version_link": "https://xiph.org/downloads/",
                "release_date": OGG["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://git.xiph.org/?p=mirrors/ogg.git;a=blob_plain;f=COPYING;hb=HEAD",  # TODO: check this link
                "build_info": {
                    "download_link": f"https://downloads.xiph.org/releases/ogg/libogg-{OGG['version']}.tar.gz",
                    "build_dir": "/tmp/libogg",
                    "tarball_name": f"libogg-{OGG['version']}.tar.gz",
                },
            },
        ),
        (
            "libopus",
            {
                "link": "https://www.opus-codec.org/",
                # https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libopus
                "version": OPUS["version"],
                "version_link": "https://www.opus-codec.org/downloads/",
                # https://ftp.osuosl.org/pub/xiph/releases/opus/
                "release_date": OPUS["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://www.xiph.org/licenses/bsd/",  # https://opus-codec.org/license/
                "build_info": {
                    "download_link": f"https://github.com/xiph/opus/releases/download/v{OPUS['version']}/opus-{OPUS['version']}.tar.gz",
                    "build_dir": "/tmp/opus",
                    "tarball_name": f"opus-{OPUS['version']}.tar.gz",
                    "sha256sum": "65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1 opus-1.5.2.tar.gz",
                },
            },
        ),
        (
            "libvorbis",
            {
                "link": "https://xiph.org/vorbis/",
                "version": VORBIS["version"],
                "version_link": "https://xiph.org/downloads/",
                "release_date": VORBIS["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://www.xiph.org/licenses/bsd/",
                "build_info": {
                    "download_link": f"http://downloads.xiph.org/releases/vorbis/libvorbis-{VORBIS['version']}.tar.gz",
                    "build_dir": "/tmp/vorbis",
                    "tarball_name": f"libvorbis-{VORBIS['version']}.tar.gz",
                    "sha256sum": "0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab libvorbis-1.3.7.tar.gz",
                },
            },
        ),
        (
            "libvpx",
            {
                "link": "https://www.webmproject.org/code/",
                # https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libvpx
                "version": VPX["version"],
                "version_link": "https://chromium.googlesource.com/webm/libvpx.git/",
                "release_date": VPX["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://github.com/webmproject/libvpx/blob/master/LICENSE",
                "build_info": {
                    # "download_link": f"https://chromium.googlesource.com/webm/libvpx/+archive/v{VPX['version']}.tar.gz",
                    "build_dir": "/tmp/libvpx",
                    # "tarball_name": f"libvpx-v{VPX['version']}.tar.gz",
                },
            },
        ),
        (
            "libwebp",
            {
                "link": "https://developers.google.com/speed/webp/",
                # https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libwebp
                "version": WEBP["version"],
                "version_link": "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html",
                "release_date": WEBP["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://github.com/webmproject/libvpx/blob/master/LICENSE",
                "build_info": {
                    "download_link": f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{WEBP['version']}.tar.gz",
                    "build_dir": "/tmp/webp",
                    "tarball_name": f"libwebp-{WEBP['version']}.tar.gz",
                },
            },
        ),
        (
            "libmp3lame",
            {
                "link": "http://lame.sourceforge.net/",
                "version": LAME["version"],
                "version_link": "http://lame.sourceforge.net/download.php",
                "release_date": LAME["release_date"],
                "license_name": "GNU Lesser General Public License (LGPL) version 2.1",
                "license_link": "http://lame.cvs.sourceforge.net/viewvc/lame/lame/LICENSE?revision=1.9",
                "build_info": {
                    # this one is also testie
                    "download_link": f"https://sourceforge.net/projects/lame/files/lame/{LAME['version']}/lame-{LAME['version']}.tar.gz",
                    "build_dir": "/tmp/lame",
                    "tarball_name": f"lame-{LAME['version']}.tar.gz",
                },
            },
        ),
        (
            "libxvid",
            {
                "link": "https://www.xvid.com/",
                "version": XVID["version"],
                "version_link": "https://labs.xvid.com/source/",
                "release_date": XVID["release_date"],
                "license_name": "GNU General Public Licence (GPL) version 2",
                "license_link": "http://websvn.xvid.org/cvs/viewvc.cgi/trunk/xvidcore/LICENSE?revision=851",
                "build_info": {
                    "download_link": f"https://downloads.xvid.com/downloads/xvidcore-{XVID['version']}.tar.gz",
                    "build_dir": "/tmp/xvid",
                    "tarball_name": f"xvidcore-{XVID['version']}.tar.gz",
                },
            },
        ),
        (
            "libfdk-aac",
            {
                "link": "https://github.com/mstorsjo/fdk-aac",
                # https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libfdk-aac
                "version": FDKAAC["version"],
                "version_link": "https://github.com/mstorsjo/fdk-aac/tags",
                "release_date": FDKAAC["release_date"],
                "license_name": "Liberal but not a license of patented technologies",
                "license_link": "https://github.com/mstorsjo/fdk-aac/blob/master/NOTICE",
                "build_info": {
                    "download_link": f"https://github.com/mstorsjo/fdk-aac/archive/refs/tags/v{FDKAAC['version']}.tar.gz",
                    "build_dir": "/tmp/fdk-aac",
                    "tarball_name": f"fdk-aac-{FDKAAC['version']}.tar.gz",
                },
            },
        ),
        (
            "openjpeg",
            {
                "link": "https://github.com/uclouvain/openjpeg",
                "version": OPENJPEG["version"],
                "version_link": "https://github.com/uclouvain/openjpeg/releases",
                "release_date": OPENJPEG["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://github.com/uclouvain/openjpeg/blob/master/LICENSE",
                "build_info": {
                    "download_link": f"https://github.com/uclouvain/openjpeg/archive/refs/tags/v{OPENJPEG['version']}.tar.gz",
                    "build_dir": "/tmp/openjpeg",
                    "tarball_name": f"openjpeg-{OPENJPEG['version']}.tar.gz",
                },
            },
        ),
        (
            "freetype",
            {
                "link": "https://www.freetype.org/",
                "version": FREETYPE["version"],
                "version_link": "http://download.savannah.gnu.org/releases/freetype/",
                "release_date": FREETYPE["release_date"],
                "license_name": "GNU General Public License (GPL) version 2",
                "license_link": "https://www.freetype.org/license.html",
                "build_info": {
                    "download_link": f"http://download.savannah.gnu.org/releases/freetype/freetype-{FREETYPE['version']}.tar.gz",
                    "build_dir": "/tmp/freetype",
                    "tarball_name": f"freetype-{FREETYPE['version']}.tar.gz",
                },
            },
        ),
        (
            "libvidstab",
            {
                "link": "https://github.com/georgmartius/vid.stab",
                "version": LIBVIDSTAB["version"],
                "version_link": "https://github.com/georgmartius/vid.stab/tags",
                "release_date": LIBVIDSTAB["release_date"],
                "license_name": "GNU General Public License (GPL) version 2",
                "license_link": "https://github.com/georgmartius/vid.stab/blob/master/LICENSE",
                "build_info": {
                    "download_link": f"https://github.com/georgmartius/vid.stab/archive/v{LIBVIDSTAB['version']}.tar.gz",
                    "build_dir": "/tmp/vid.stab",
                    "tarball_name": f"vid.stab-{LIBVIDSTAB['version']}.tar.gz",
                },
            },
        ),
        (
            "fribidi",
            {
                "link": "https://www.fribidi.org/",
                "version": LIBFRIDIBI["version"],
                "version_link": "https://github.com/fribidi/fribidi/releases",
                "release_date": LIBFRIDIBI["release_date"],
                "license_name": "GNU General Public License (GPL) version 2",
                "license_link": "https://cgit.freedesktop.org/fribidi/fribidi/plain/COPYING",
                "build_info": {
                    "download_link": f"https://github.com/fribidi/fribidi/archive/refs/tags/v{LIBFRIDIBI['version']}.tar.gz",
                    "build_dir": "/tmp/fribidi",
                    "tarball_name": f"fribidi-{LIBFRIDIBI['version']}.tar.gz",
                    "using_source_build": False,
                    # "sha256sum": "3fc96fa9473bd31dcb5500bdf1aa78b337ba13eb8c301e7c28923fea982453a8 fribidi-{LIBFRIDIBI['version']}.tar.gz"
                },
            },
        ),
        (
            "fontconfig",
            {
                "link": "https://www.freedesktop.org/wiki/Software/fontconfig/",
                "version": FONTCONFIG["version"],
                "version_link": "https://www.freedesktop.org/software/fontconfig/release/",
                "release_date": FONTCONFIG["release_date"],
                "license_name": "",
                "license_link": "",
                "build_info": {
                    "download_link": f"https://www.freedesktop.org/software/fontconfig/release/fontconfig-{FONTCONFIG['version']}.tar.gz",
                    "build_dir": "/tmp/fontconfig",
                    "tarball_name": f"fontconfig-{FONTCONFIG['version']}.tar.gz",
                },
            },
        ),
        (
            "libass",
            {
                "link": "https://github.com/libass/libass",
                "version": LIBASS["version"],
                "version_link": "https://github.com/libass/libass/releases",
                "release_date": LIBASS["release_date"],
                "license_name": "ISC License",
                "license_link": "https://github.com/libass/libass/blob/master/COPYING",
                "build_info": {
                    "download_link": f"https://github.com/libass/libass/releases/download/{LIBASS['version']}/libass-{LIBASS['version']}.tar.gz",
                    "build_dir": "/tmp/libass",
                    "tarball_name": f"libass-{LIBASS['version']}.tar.gz",
                    "using_source_build": False,
                },
            },
        ),
        (
            "kvazaar",
            {
                "link": "https://github.com/ultravideo/kvazaar",
                "version": KVAAZAAR["version"],
                "version_link": "https://github.com/ultravideo/kvazaar/releases",
                "release_date": KVAAZAAR["release_date"],
                "license_name": "BSD 3-Clause",
                "license_link": "https://github.com/ultravideo/kvazaar/blob/master/LICENSE`",
                "build_info": {
                    "download_link": f"https://github.com/ultravideo/kvazaar/releases/download/v{KVAAZAAR['version']}/kvazaar-{KVAAZAAR['version']}.tar.gz",
                    "build_dir": "/tmp/kvazaar",
                    "tarball_name": f"kvazaar-{KVAAZAAR['version']}.tar.gz",
                },
            },
        ),
        (
            "aom",
            {
                "link": "https://aomedia.googlesource.com/aom",
                "version": AOM["version"],
                "version_link": "https://aomedia.googlesource.com/aom/+refs",
                "release_date": AOM["release_date"],
                "license_name": "Alliance for Open Media",
                "license_link": "https://aomedia.org/license/software-license/",
                "build_info": {
                    "build_dir": "/tmp/aom",
                },
            },
        ),
        (
            "nvidia-codec-headers",
            {
                "link": "https://github.com/FFmpeg/nv-codec-headers",
                "version": NV_CODEC["version"],
                "version_link": "",
                "release_date": NV_CODEC["release_date"],
                "license_name": "",
                "license_link": "",
                "build_info": {
                    "download_link": f"https://github.com/FFmpeg/nv-codec-headers/releases/download/n{NV_CODEC['version']}/nv-codec-headers-{NV_CODEC['version']}.tar.gz",
                    # "download_link": f"https://github.com/FFmpeg/nv-codec-headers/archive/refs/tags/n{NV_CODEC['version']}.tar.gz",
                    "build_dir": "/tmp/nv-codec-headers",
                    "tarball_name": f"nv-codec-headers-{NV_CODEC['version']}.tar.gz",
                },
            },
        ),
        (
            "libsvtav1",
            {
                "link": "https://gitlab.com/AOMediaCodec/SVT-AV1",
                "version": SVTAV1["version"],
                "version_link": "https://gitlab.com/AOMediaCodec/SVT-AV1/-/tags",
                "release_date": SVTAV1["release_date"],
                "license_name": "BSD 3-Clause Clear License",
                "license_link": "https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/LICENSE.md?ref_type=heads",
                "build_info": {
                    "download_link": f"https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v{SVTAV1['version']}/SVT-AV1-v{SVTAV1['version']}.tar.gz",
                    "build_dir": "/tmp/libsvtav1",
                    "tarball_name": f"SVT-AV1-v{SVTAV1['version']}.tar.gz",
                },
            },
        ),
        (
            "xorg-macros",
            {
                "link": "https://xcb.freedesktop.org/",
                "version": XORG_MACROS["version"],
                "version_link": "https://www.x.org/releases/individual/util/",
                "release_date": XORG_MACROS["release_date"],
                "license_name": "The MIT License",
                "license_link": "https://opensource.org/licenses/MIT",
                "build_info": {
                    "download_link": f"https://www.x.org/releases/individual/util/util-macros-{XORG_MACROS['version']}.tar.xz",
                    "build_dir": "/tmp/xorg-macros",
                    "tarball_name": f"util-macros-{XORG_MACROS['version']}.tar.xz",
                    "using_source_build": False,
                },
            },
        ),
        (
            "xproto",
            {
                "link": "https://www.x.org/releases/individual/proto/",
                "version": XPROTO["version"],
                "version_link": "https://www.x.org/releases/individual/proto/",
                "release_date": XPROTO["release_date"],
                "license_name": "The MIT License",
                "license_link": "https://opensource.org/licenses/MIT",
                "build_info": {
                    "download_link": f"https://www.x.org/releases/individual/proto/xproto-{XPROTO['version']}.tar.gz",
                    "build_dir": "/tmp/xproto",
                    "tarball_name": f"xproto-{XPROTO['version']}.tar.gz",
                },
            },
        ),
        (
            "libxau",
            {
                "link": "https://www.x.org/releases/individual/lib/",
                "version": XAU["version"],
                "version_link": "https://www.x.org/releases/individual/lib/",
                "release_date": XAU["release_date"],
                "license_name": "The MIT License",
                "license_link": "https://opensource.org/licenses/MIT",
                "build_info": {
                    "download_link": f"https://www.x.org/releases/individual/lib/libXau-{XAU['version']}.tar.xz",
                    "build_dir": "/tmp/libXau",
                    "tarball_name": f"libXau-{XAU['version']}.tar.xz",
                    "using_source_build": False,
                },
            },
        ),
        (
            "libpthread-stubs",
            {
                "link": "https://www.x.org/releases/individual/lib/",
                "version": PTHREAD_STUBS["version"],
                "version_link": "https://www.x.org/releases/individual/lib/",
                "release_date": PTHREAD_STUBS["release_date"],
                "license_name": "The MIT License",
                "license_link": "https://opensource.org/licenses/MIT",
                "build_info": {
                    "download_link": f"https://www.x.org/releases/individual/lib/libpthread-stubs-{PTHREAD_STUBS['version']}.tar.xz",
                    "build_dir": "/tmp/libpthread-stubs",
                    "tarball_name": f"libpthread-stubs-{PTHREAD_STUBS['version']}.tar.xz",
                    # "using_source_build": False,
                },
            },
        ),
        (
            "libxml2",
            {
                "link": "http://www.xmlsoft.org/",
                "version": LIBXML2["version"],
                "version_link": "http://www.xmlsoft.org/downloads.html",
                "release_date": LIBXML2["release_date"],
                "license_name": "MIT License",
                "license_link": "http://www.xmlsoft.org/license.html",
                "build_info": {
                    "download_link": f"https://gitlab.gnome.org/GNOME/libxml2/-/archive/v{LIBXML2['version']}/libxml2-v{LIBXML2['version']}.tar.gz",
                    "build_dir": "/tmp/libxml2",
                    "tarball_name": f"libxml2-{LIBXML2['version']}.tar.gz",
                    "using_source_build": False,
                },
            },
        ),
        (
            "libbluray",
            {
                "link": "https://www.videolan.org/developers/libbluray.html",
                "version": LIBBLURAY["version"],
                "version_link": "https://download.videolan.org/pub/videolan/libbluray/",
                "release_date": LIBBLURAY["release_date"],
                "license_name": "GNU General Public License (GPL) version 2",
                "license_link": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
                "build_info": {
                    "download_link": f"https://download.videolan.org/pub/videolan/libbluray/{LIBBLURAY['version']}/libbluray-{LIBBLURAY['version']}.tar.bz2",
                    "build_dir": "/tmp/libbluray",
                    "tarball_name": f"libbluray-{LIBBLURAY['version']}.tar.bz2",
                },
            },
        ),
        (
            "libzmq",
            {
                "link": "https://github.com/zeromq/libzmq/",
                "version": LIBZMQ["version"],
                "version_link": "https://github.com/zeromq/libzmq/releases/",
                "release_date": LIBZMQ["release_date"],
                "license_name": "Mozilla Public License (MPL) version 2.0",
                "license_link": f"https://github.com/zeromq/libzmq/blob/v{LIBZMQ['version']}/LICENSE",
                "build_info": {
                    "download_link": f"https://github.com/zeromq/libzmq/releases/download/v{LIBZMQ['version']}/zeromq-{LIBZMQ['version']}.tar.gz",
                    "build_dir": "/tmp/libzmq",
                    "tarball_name": f"zeromq-{LIBZMQ['version']}.tar.gz",
                },
            },
        ),
        (
            "libpng",
            {
                "link": "http://www.libpng.org/pub/png/libpng.html",
                "version": LIBPNG["version"],
                "version_link": "https://sourceforge.net/projects/libpng/files/libpng16/",
                "release_date": LIBPNG["release_date"],
                "license_name": "PNG Reference Library License version 2",
                "license_link": "http://www.libpng.org/pub/png/src/libpng-LICENSE.txt",
                "build_info": {
                    # sourceforge is a bit finikie
                    # https://sourceforge.net/projects/libpng/files/libpng16/1.6.44/libpng-1.6.44.tar.gz/download
                    # https://download.sourceforge.net/libpng/libpng-1.6.44.tar.xz
                    "download_link": f"https://download.sourceforge.net/libpng/libpng-{LIBPNG['version']}.tar.xz",
                    "build_dir": "/tmp/libpng",
                    "tarball_name": f"libpng-{LIBPNG['version']}.tar.xz",
                    "using_source_build": False,
                },
            },
        ),
        (
            "libaribb24",
            {
                "link": "https://github.com/nkoriyama/aribb24/",
                "version": LIBARIBB24["version"],
                "version_link": "https://github.com/nkoriyama/aribb24/releases",
                "release_date": LIBARIBB24["release_date"],
                "license_name": "GNU Lesser General Public License (LGPL) version 2.1 or newer",
                "license_link": "https://github.com/nkoriyama/aribb24/issues/9",
                "build_info": {
                    "download_link": f"https://github.com/nkoriyama/aribb24/archive/refs/tags/v{LIBARIBB24['version']}.tar.gz",
                    "build_dir": "/tmp/b24",
                    "tarball_name": f"aribb24-v{LIBARIBB24['version']}.tar.gz",
                },
            },
        ),
        (
            "zimg",
            {
                "link": "https://github.com/sekrit-twc/zimg",
                "version": ZIMG["version"],
                "version_link": "https://github.com/sekrit-twc/zimg/releases",
                "release_date": ZIMG["release_date"],
                "license_name": "WTFPL",
                "license_link": "https://github.com/sekrit-twc/zimg?tab=WTFPL-1-ov-file",
                "build_info": {
                    "download_link": f"https://github.com/sekrit-twc/zimg/archive/refs/tags/release-{ZIMG['version']}.tar.gz",
                    "build_dir": "/tmp/zimg",
                    "tarball_name": f"zimg-{ZIMG['version']}.tar.gz",
                },
            },
        ),
        (
            "libtheora",
            {
                "link": "https://xiph.org/downloads/",
                "version": THEORA["version"],
                "version_link": "https://xiph.org/downloads/",
                "release_date": THEORA["release_date"],
                "license_name": "BSD-style license",
                "license_link": "https://git.xiph.org/?p=mirrors/theora.git;a=blob_plain;f=COPYING;hb=HEAD",
                "build_info": {
                    "download_link": f"https://downloads.xiph.org/releases/theora/libtheora-{THEORA['version']}.tar.gz",
                    "build_dir": "/tmp/theora",
                    "tarball_name": f"libtheora-{THEORA['version']}.tar.gz",
                },
            },
        ),
        (
            "libsrt",
            {
                "link": "https://github.com/Haivision/srt",
                "version": LIBSRT["version"],
                "version_link": "https://github.com/Haivision/srt/releases/",
                "release_date": LIBSRT["release_date"],
                "license_name": "Mozilla Public License (MPL) version 2.0",
                "license_link": "https://github.com/Haivision/srt/blob/master/LICENSE",
                "build_info": {
                    "download_link": f"https://github.com/Haivision/srt/archive/refs/tags/v{LIBSRT['version']}.tar.gz",
                    "build_dir": "/tmp/srt",
                    "tarball_name": f"srt-v{LIBSRT['version']}.tar.gz",
                },
            },
        ),
        (
            "libvmaf",
            {
                "link": "https://github.com/Netflix/vmaf",
                # https://github.com/Netflix/vmaf/issues/788
                "version": LIBVMAF["version"],
                "version_link": "https://github.com/Netflix/vmaf/releases",
                "release_date": LIBVMAF["release_date"],
                "license_name": "BSD-2-Clause",
                "license_link": "https://github.com/Netflix/vmaf/blob/master/LICENSE",
                "build_info": {
                    "download_link": f"https://github.com/Netflix/vmaf/archive/refs/tags/v{LIBVMAF['version']}.tar.gz",
                    "build_dir": "/tmp/vmaf",
                    "tarball_name": f"vmaf-v{LIBVMAF['version']}.tar.gz",
                },
            },
        ),
        (
            "ffmpeg-7.1",
            {
                "link": "http://ffmpeg.org/",
                "version": FFMPEG_71["version"],
                "version_link": "http://ffmpeg.org/releases/",
                "release_date": FFMPEG_71["release_date"],
                "license_name": "GNU Lesser General Public License (LGPL) version 2.1",
                "license_link": "https://ffmpeg.org/legal.html",
                "build_info": {
                    "download_link": f"https://ffmpeg.org/releases/ffmpeg-{FFMPEG_71['version']}.tar.bz2",
                    "build_dir": "/tmp/ffmpeg",
                    "tarball_name": f"ffmpeg-{FFMPEG_71['version']}.tar.bz2",
                },
            },
        ),
        (
            "ffmpeg-7.0",
            {
                "link": "http://ffmpeg.org/",
                "version": FFMPEG_70["version"],
                "version_link": "http://ffmpeg.org/releases/",
                "release_date": FFMPEG_70["release_date"],
                "license_name": "GNU Lesser General Public License (LGPL) version 2.1",
                "license_link": "https://ffmpeg.org/legal.html",
                "build_info": {
                    "download_link": f"https://ffmpeg.org/releases/ffmpeg-{FFMPEG_70['version']}.tar.bz2",
                    "build_dir": "/tmp/ffmpeg",
                    "tarball_name": f"ffmpeg-{FFMPEG_70['version']}.tar.bz2",
                },
            },
        ),
        (
            "ffmpeg-6.1",
            {
                "link": "http://ffmpeg.org/",
                "version": FFMPEG_61["version"],
                "version_link": "http://ffmpeg.org/releases/",
                "release_date": FFMPEG_61["release_date"],
                "license_name": "GNU Lesser General Public License (LGPL) version 2.1",
                "license_link": "https://ffmpeg.org/legal.html",
                "build_info": {
                    "download_link": f"https://ffmpeg.org/releases/ffmpeg-{FFMPEG_61['version']}.tar.bz2",
                    "build_dir": "/tmp/ffmpeg",
                    "tarball_name": f"ffmpeg-{FFMPEG_61['version']}.tar.bz2",
                },
            },
        ),
        # (
        #     "ffmpeg-5.1",
        #     {
        #         "link": "http://ffmpeg.org/",
        #         "version": FFMPEG_51["version"],
        #         "version_link": "http://ffmpeg.org/releases/",
        #         "release_date": FFMPEG_51["release_date"],
        #         "license_name": "GNU Lesser General Public License (LGPL) version 2.1",
        #         "license_link": "https://ffmpeg.org/legal.html",
        #         "build_info": {
        #             "download_link": f"https://ffmpeg.org/releases/ffmpeg-{FFMPEG_51['version']}.tar.bz2",
        #             "build_dir": "/tmp/ffmpeg",
        #             "tarball_name": f"ffmpeg-{FFMPEG_51['version']}.tar.bz2",
        #         },
        #     },
        # ),
    ]
)
# come back to this problem, I think yaml configuration might be better.
# with open('libraries.json', 'r') as f:
#     data = json.load(f) # todo this should be yaml config
#     order_list = data['build_order']
#     LIBRARIES = OrderedDict((key, data['libraries'][key]) for key in order_list)


def generate_library_table(filename):
    """
    Generates a formatted table of FFmpeg libraries.
    cut-n-paste this into the main projects README.md file.
    """
    # open the filename for writing, overwrite if it exists
    with open(filename, "w") as f:
        f.write("## FFMPEG Supported Libraries\n")
        f.write(
            "The following libraries are used by FFMPEG. The version number and release date are provided along with the license information.\n"
        )
        f.write(
            "These version numbers are for the lib source builds, which are 'ubuntu2404-edge' and 'foo'.\n"
        )
        f.write(
            "These libs are included in the package images as well, but the version numbers might vary slightly.\n\n"
        )

        f.write(
            "| Libraries | Version | Release Date | Download Source | Checksum | License |\n"
        )
        f.write(
            "|-----------|---------|--------------|------------ | --- | ---------|\n"
        )
        for k, v in LIBRARIES.items():
            libname = f"[{k}]({v['link']})"  # link to the library
            libversion = f"[{v['version']}]({v['version_link']})"  # link to the version
            license = (
                f"[{v['license_name']}]({v['license_link']})"  # link to the license
            )
            # if build_info and build_info.tarball_name and build_info.download_link is avaliabl then set the download_source
            download_source = ""
            if (
                v.get("build_info")
                and v["build_info"].get("tarball_name")
                and v["build_info"].get("download_link")
            ):
                download_source = f"[{v['build_info']['tarball_name']}]({v['build_info']['download_link']})"
            checksum = v["build_info"].get("sha256sum", "")
            has_checksum = "Yes" if checksum else "No"

            using_source_build = v["build_info"].get("using_source_build", True)
            # if we are not using the source build then do not display it in the table.
            if using_source_build:
                f.write(
                    f"| {libname} | {libversion} | {v.get('release_date', '')} | {download_source} | {has_checksum} | {license} |\n"
                )
        print(f"Library table generated: {filename}")
        sys.stdout.flush()


def generate_versions_manifest(output_file, ffmpeg_libraries=[]):
    """
    Generates a 'generated_build_versions_manifest.json' file containing library version information.

    Args:
        ffmpeg_libraries (dict): A dictionary containing FFmpeg library information.
        output_file (str, optional): The filename for the build manifest. Defaults to "generated_build_versions_manifest.json".
    """

    manifest_data = {}
    if not ffmpeg_libraries:
        ffmpeg_libraries = LIBRARIES.keys()
    for library_name in ffmpeg_libraries:
        library_info = LIBRARIES.get(library_name, {})
        manifest_data[library_name] = library_info.get("version", "")

    with open(output_file, "w") as f:
        json.dump(manifest_data, f, indent=4)
        print(f"Versions manifest generated: {output_file}")
        sys.stdout.flush()


def generate_build_manifest(output_file, ffmpeg_libraries=[]):
    """
    Generates a 'generated_build_manifest.json' file containing library download information.

    Args:
        ffmpeg_libraries (dict): A dictionary containing FFmpeg library information.
        output_file (str, optional): The filename for the build manifest. Defaults to "generated_build_manifest.json".
    """

    manifest_data = []
    if not ffmpeg_libraries:
        ffmpeg_libraries = LIBRARIES.keys()
    for library_name in ffmpeg_libraries:
        library_info = LIBRARIES.get(library_name, {})
        build_info = library_info.get("build_info", {})
        download_url = build_info.get("download_link", "")
        build_dir = build_info.get("build_dir", "")
        tarball_name = build_info.get("tarball_name", "")
        sha256sum = build_info.get("sha256sum", "")

        if not all([build_dir]):
            print(
                f"Warning: Missing 'build_dir' information for {library_name} in build manifest generation."
            )
            continue

        data = {
            "library_name": library_name,
            "build_dir": build_dir,
        }
        if download_url and tarball_name:
            data["download_url"] = download_url
            data["tarball_name"] = tarball_name

        if sha256sum:
            data["sha256sum"] = sha256sum
        manifest_data.append(data)

    with open(output_file, "w") as f:
        json.dump(manifest_data, f, indent=4)
        print(f"Build manifest generated: {output_file}")
        sys.stdout.flush()


def list_of_strings(arg):
    return arg.split(",")


def main():
    """
    Handles three modes:
     1. Generate both generated files (default)
     2. Generate library table
     3. Generate build manifest
    """

    parser = argparse.ArgumentParser(description="FFmpeg Library Information Script")
    parser.add_argument("--library-list", type=list_of_strings, default=[])
    args = parser.parse_args()

    default_versions_table = "generated_versions_table.md"
    default_generated_json_file = "generated_build_manifest.json"
    default_generated_versions_json = "generated_build_versions_manifest.json"

    generate_library_table(default_versions_table)
    generate_build_manifest(default_generated_json_file, args.library_list)
    generate_versions_manifest(default_generated_versions_json, args.library_list)


if __name__ == "__main__":
    main()
