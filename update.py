#!/usr/bin/env python


# Get latest release from ffmpeg.org
import os, sys
import re
import operator
import urllib2
from distutils.version import StrictVersion

MIN_VERSION='2.8'

# response = urllib2.urlopen('https://ffmpeg.org/releases/')
# ffmpeg_releases = response.read()
#
# parse_re = re.compile('ffmpeg-([.0-9]*).tar.bz2.asc<\/a>\s+')
# all_versions = parse_re.findall(ffmpeg_releases)
# all_versions.sort(key=StrictVersion, reverse=True)
#
# version, all_versions = all_versions[0], all_versions[1:]

version = '3.2.1'
all_versions = ['3.2', '3.1.5', '3.0.9', '3.0.5','2.9']
last = version.split('.')
print last
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

for v in keep_version:
    
