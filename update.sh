#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

versions=( "$@" )
if [ ${#versions[@]} -eq 0 ]; then
  versions=( */ )
fi
versions=( "${versions[@]%/}" )

travisEnv=''
#
for version in "${versions[@]}"; do
  ENV="$(sed s*%%FFMPEG_VERSION%%*${version}*g Dockerfile-env)"
  for variant in centos ubuntu; do
    sed -e "s*%%ENV%%*${ENV}*g" ${variant}-dockerfile.template  \
		    -e '/%%RUN%%/{
    s/%%RUN%%//g
    r Dockerfile-run
	}' > ${version}/${variant}/Dockerfile
    travisEnv+="\n - VERSION=${version} VARIANT=${variant}"
  done
done
travis="$(awk -v 'RS=\n\n' '$1 == "env:" { $0 = "env:'"$travisEnv"'" } { printf "%s%s", $0, RS }' .travis.yml)"
echo "$travis" > .travis.yml
