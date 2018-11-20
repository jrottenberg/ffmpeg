#!/usr/bin/env python


# Get latest release from ffmpeg.org
import os
import sys
import re
import urllib2
from distutils.version import StrictVersion

MIN_VERSION = '2.8'
VARIANTS = ['ubuntu', 'alpine', 'centos', 'scratch', 'vaapi']
FFMPEG_RELEASES = 'https://ffmpeg.org/releases/'

travis = []
azure = []
response = urllib2.urlopen(FFMPEG_RELEASES)
ffmpeg_releases = response.read()

parse_re = re.compile('ffmpeg-([.0-9]+).tar.bz2.asc<\/a>\s+')
all_versions = parse_re.findall(ffmpeg_releases)
all_versions.sort(key=StrictVersion, reverse=True)

version, all_versions = all_versions[0], all_versions[1:]

last = version.split('.')
keep_version = ['snapshot']

keep_version.append(version)

for cur in all_versions:
    if cur < MIN_VERSION:
        break

    tmp = cur.split('.')
    # Check Minor
    if len(tmp) >= 2 and tmp[1].isdigit() and tmp[1] < last[1]:
        keep_version.append(cur)
        last = tmp
    # Check Major
    elif len(tmp) > 1 and tmp[0].isdigit() and tmp[0] < last[0]:
        keep_version.append(cur)
        last = tmp

for version in keep_version:
    for variant in VARIANTS:
        if version == 'snapshot':
            dockerfile = 'docker-images/%s/%s/Dockerfile' % (
                version, variant)
            travis.append(' - VERSION=%s VARIANT=%s' % (version, variant))
            azure.append('      %s_%s:\n        VERSION: %s\n        VARIANT: %s' % (version.replace('.', '_'), variant, version, variant))
        else:
            dockerfile = 'docker-images/%s/%s/Dockerfile' % (
                version[0:3], variant)
            travis.append(' - VERSION=%s VARIANT=%s' % (version[0:3], variant))
            azure.append('      %s_%s:\n        VERSION: %s\n        VARIANT: %s' % (version[0:3].replace('.', '_'), variant, version[0:3], variant))

        with open('templates/Dockerfile-env', 'r') as tmpfile:
            env_content = tmpfile.read()
        with open('templates/Dockerfile-template.' + variant, 'r') as tmpfile:
            template = tmpfile.read()
        with open('templates/Dockerfile-run', 'r') as tmpfile:
            run_content = tmpfile.read()
        env_content = env_content.replace('%%FFMPEG_VERSION%%', version)
        docker_content = template.replace('%%ENV%%', env_content)
        docker_content = docker_content.replace('%%RUN%%', run_content)
        # OpenJpeg 2.1 is not supported in 2.8
        if version[0:3] == '2.8':
            docker_content = docker_content.replace('--enable-libopenjpeg', '')
            docker_content = docker_content.replace('--enable-libkvazaar', '')
        if (version != 'snapshot' and version[0:3] != '4.0') or variant == 'centos':
            docker_content = re.sub(r"--enable-libaom [^\\]*", "", docker_content)
        if (version == 'snapshot' or version[0] >= '3') and variant == 'vaapi':
            docker_content = docker_content.replace('--disable-ffplay', '--disable-ffplay \\\n        --enable-vaapi')

        # FFmpeg 3.2 and earlier don't compile correctly on Ubuntu 18.04 due to openssl issues
        if variant == 'vaapi' and (version[0] < '3' or (version[0] == '3' and version[2] < '3')):
            docker_content = docker_content.replace('ubuntu:18.04', 'ubuntu:16.04')
            docker_content = docker_content.replace('libva-drm2', 'libva-drm1')
            docker_content = docker_content.replace('libva2', 'libva1')

        patch = ''
        if version[0:3] == '4.0':
            with open('templates/Dockerfile-patch-4.0', 'r') as tmpfile:
                patch = tmpfile.read()

        docker_content = docker_content.replace('%%FFMPEG_PATCH%%', patch)

        d = os.path.dirname(dockerfile)
        if not os.path.exists(d):
            os.makedirs(d)

        with open(dockerfile, 'w') as dfile:
            dfile.write(docker_content)


with open('templates/travis.template', 'r') as tmpfile:
    template = tmpfile.read()
travis = template.replace('%%VERSIONS%%', '\n'.join(travis))


with open('.travis.yml', 'w') as travisfile:
    travisfile.write(travis)

with open('templates/azure.template', 'r') as tmpfile:
    template = tmpfile.read()
azure = template.replace('%%VERSIONS%%', '\n'.join(azure))


with open('azure-pipelines.yml', 'w') as azurefile:
    azurefile.write(azure)
