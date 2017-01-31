#!/usr/bin/env python


# Get latest release from ffmpeg.org
import os, sys
import re
import urllib2
from distutils.version import StrictVersion

MIN_VERSION='2.8'
VARIANTS = ['ubuntu', 'alpine', 'centos']
FFMPEG_RELEASES='https://ffmpeg.org/releases/'

travis = []
response = urllib2.urlopen(FFMPEG_RELEASES)
ffmpeg_releases = response.read()

parse_re = re.compile('ffmpeg-([.0-9]+).tar.bz2.asc<\/a>\s+')
all_versions = parse_re.findall(ffmpeg_releases)
all_versions.sort(key=StrictVersion, reverse=True)

version, all_versions = all_versions[0], all_versions[1:]


# # offline mode
# version = '3.2.1'
# all_versions = ['3.2', '3.1.5', '3.0.9', '3.0.5','2.9']


last = version.split('.')
keep_version = [version]

for cur in all_versions:
    if cur < MIN_VERSION:
        break

    tmp = cur.split('.')
## Check Minor
    if len(tmp) >= 2 and tmp[1].isdigit() and tmp[1] < last[1]:
        keep_version.append(cur)
        last = tmp
## Check Major
    elif len(tmp) > 1 and tmp[0].isdigit() and tmp[0] < last[0]:
        keep_version.append(cur)
        last = tmp

for version in keep_version:
    for variant in VARIANTS:
        if variant == 'ubuntu':
            dockerfile = '%s/Dockerfile' % version[0:3]
            travis.append(' - VERSION=%s' % version[0:3])
        else:
            dockerfile = '%s/%s/Dockerfile' % (version[0:3], variant)
            travis.append(' - VERSION=%s VARIANT=%s' % (version[0:3], variant))

        with open('Dockerfile-env', 'r') as tmpfile:
           env_content = tmpfile.read()
        with open('Dockerfile-template.' + variant , 'r') as tmpfile:
           template = tmpfile.read()
        with open('Dockerfile-run', 'r') as tmpfile:
           run_content = tmpfile.read()
        env_content = env_content.replace('%%FFMPEG_VERSION%%', version)
        docker_content = template.replace('%%ENV%%', env_content)
        docker_content = docker_content.replace('%%RUN%%', run_content)

        d = os.path.dirname(dockerfile)
        if not os.path.exists(dockerfile):
            os.makedirs(d)

        with open(dockerfile, 'w') as dfile:
          dfile.write(docker_content)


with open('travis.template', 'r') as tmpfile:
   template = tmpfile.read()
travis = template.replace('%%VERSIONS%%', '\n'.join(travis))


with open('.travis.yml', 'w') as travisfile:
  travisfile.write(travis)
