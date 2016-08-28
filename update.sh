#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$BASH_SOURCE")")"

versions=( "$@" )
if [ ${#versions[@]} -eq 0 ]; then
  versions=( */ )
fi
versions=( "${versions[@]%/}" )

travisEnv=''
for version in "${versions[@]}"; do
  sed s*%%FFMPEG_VERSION%%*${version}*g Dockerfile-env > ENV
  for variant in centos ubuntu; do
    sed s*%%ENV%%*"$(cat ENV)"*g ${variant}-dockerfile-head > ${version}/${variant}/Dockerfile
    cat dockerfile-run >> ${version}/${variant}/Dockerfile
    cat ${variant}-dockerfile-tail >> ${version}/${variant}/Dockerfile
    travisEnv+="\n - VERSION=${version} VARIANT=${variant}"
  done
  rm ENV

done
echo -e "${travisEnv}"

travis="$(awk -v 'RS=\n\n' '$1 == "env:" { $0 = "env:'"$travisEnv"'" } { printf "%s%s", $0, RS }' .travis.yml)"
echo "$travis" > .travis.yml
