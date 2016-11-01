#!/usr/bin/env bash

set -euox pipefail

cd $(cd ${0%/*} && pwd -P);


majors=( "$@" )
if [ ${#majors[@]} -eq 0 ]; then
  majors=( */ )
fi
majors=( "${majors[@]%/}" )

travisEnv=''


#
for major in "${majors[@]}"; do
  minor=$(curl -sSL --compressed http://ffmpeg.org/releases/ | grep '<a href="ffmpeg-'"${major}." | sed -E 's!.*<a href="ffmpeg-([^"/]+)/?".*!\1!' | cut -f 3 -d . | sort -n | tail -1)
  if [ "x${minor}" = 'xtar' ]; then
  	version=${major}
  else 
	version=${major}.${minor}
  fi
  ENV="$(sed s*%%FFMPEG_VERSION%%*${version}*g Dockerfile-env)"

  for variant in ubuntu alpine centos; do
    if [[ $variant == 'ubuntu' ]]; then
      DOCKERFILE=${major}/Dockerfile
      TRAVIS_VARIANT=""
    else
      DOCKERFILE=${major}/${variant}/Dockerfile
      TRAVIS_VARIANT="VARIANT=${variant}"
    fi

    if [ -e $DOCKERFILE ]; then
      sed -i -e "s/FFMPEG_VERSION=.*/FFMPEG_VERSION=$version \\\\/" $DOCKERFILE
    else
      mkdir -p $(dirname $DOCKERFILE)
      sed -e "s*%%ENV%%*${ENV}*g" ${variant}-dockerfile.template  \
	      -e '/%%RUN%%/{
		  s/%%RUN%%//g
	          r Dockerfile-run
	      }' > ${DOCKERFILE}
    fi
    travisEnv+="\n - major=${major} ${TRAVIS_VARIANT}"
  done
done
travis="$(awk -v 'RS=\n\n' '$1 == "env:" { $0 = "env:'"$travisEnv"'" } { printf "%s%s", $0, RS }' .travis.yml)"
echo "$travis" > .travis.yml
