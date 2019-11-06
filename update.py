#!/usr/bin/env python


# Get latest release from ffmpeg.org
import os
import sys
import re
import urllib2
from distutils.version import StrictVersion

MIN_VERSION = '2.8'
VARIANTS = ['ubuntu', 'alpine', 'centos', 'scratch', 'vaapi', 'nvidia']
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

        with open('templates/Dockerfile-template.' + variant, 'r') as tmpfile:
            template = tmpfile.read()
        with open('templates/Dockerfile-run', 'r') as tmpfile:
            run_content = tmpfile.read()
        run_content = run_content.replace('%%FFMPEG_VERSION%%', version)
        docker_content = template.replace('%%RUN%%', run_content)
        docker_content = docker_content.replace('%%FFMPEG_VERSION%%', version)
        # OpenJpeg 2.3 is not supported in  < 3.3
        if (version[0] < '3' or (version[0] == '3' and version[2] < '4')):
            docker_content = docker_content.replace('--enable-libopenjpeg', '')
            docker_content = docker_content.replace('--enable-libkvazaar', '')
        if (version != 'snapshot' and version[0] < '4'):
            docker_content = re.sub(r"--enable-libaom [^\\]*", "", docker_content)
        if (version == 'snapshot' or version[0] >= '3') and variant == 'vaapi':
            docker_content = docker_content.replace('--disable-ffplay', '--disable-ffplay \\\n        --enable-vaapi')
        if variant == 'nvidia':
            docker_content = docker_content.replace('--extra-cflags="-I${PREFIX}/include"', '--extra-cflags="-I${PREFIX}/include -I${PREFIX}/include/ffnvcodec -I/usr/local/cuda/include/"')
            docker_content = docker_content.replace('--extra-ldflags="-L${PREFIX}/lib"', '--extra-ldflags="-L${PREFIX}/lib -L/usr/local/cuda/lib64/ -L/usr/local/cuda/lib32/"')
            if (version == 'snapshot' or version[0] >= '4') :
                docker_content = docker_content.replace('--disable-ffplay', '--disable-ffplay \\\n     	--enable-cuda \\\n        --enable-nvenc \\\n        --enable-cuvid \\\n        --enable-libnpp')
            # Don't support hw decoding and scaling on older ffmpeg versions
            if (version[0] < '4') :
                docker_content = docker_content.replace('--disable-ffplay', '--disable-ffplay \\\n      --enable-nvenc')

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
