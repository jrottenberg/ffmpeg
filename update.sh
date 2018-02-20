#!/bin/bash

set -eu -o pipefail
cwd="$(dirname "$0")"

template_dir="$cwd/templates"
dockerfile_dir="$cwd/docker-images"

#If there is no ruby available install it
if ! which ruby 2>&1 > /dev/null; then
  alias ruby="docker run --rm -u $(id -u) -v "${PWD}":/usr/src/myapp -w /usr/src/myapp ruby:2.5-alpine ruby"
fi

semver_re='[^0-9]*\([0-9]*\)[.]\([0-9]*\)[.]\([0-9]*\)\([0-9A-Za-z-]*\)'
iwantplate="ruby $template_dir/iwantplate.rb"

for version in `$iwantplate --list-versions | tr -d '\r' | head -n 1`; do
    for variant in `$iwantplate --list-variants | tr -d '\r'`; do
        release=`echo $version | sed -e "s/$semver_re/\1.\2/"`
        mkdir -p ${dockerfile_dir}/${release}/${variant}
        ${iwantplate} -V ${variant} -v ${version} > ${dockerfile_dir}/${release}/${variant}/Dockerfile
        docker build -t ffmpeg:local --build-arg 'MAKEFLAGS=-j8' -f ${dockerfile_dir}/${release}/${variant}/Dockerfile .
        docker run --rm ffmpeg:local -buildconf
    done
done
