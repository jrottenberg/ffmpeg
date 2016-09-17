#!/bin/bash
set -eu

array_2_8='2';
array_3_0='';
array_3_1='3 latest';

cd $(cd ${0%/*} && pwd -P);

declare -A variants='centos'

hash git 2>/dev/null || { echo >&2 "git not found, exiting."; }

versions=( */ )
versions=( "${versions[@]%/}" )
url='git://github.com/jrottenberg/ffmpeg'

echo '# maintainer: Julien Rottenberg <julien@rottenberg.info>'

for version in "${versions[@]}"; do
	if [[ "$version" == "docs" ]]; then
		continue
	fi
	eval stub=$(echo "$version" | awk -F. '{ print "$array_" $1 "_" $2 }');
	commit="$(git log -1 --format='format:%H' -- "$version")"
	fullVersion="$(grep -m1 'FFMPEG_VERSION=' "$version/Dockerfile"  | cut -d'=' -f2 | cut -d ' ' -f1)"

	versionAliases=( $fullVersion $version ${stub} )
	echo
	for va in "${versionAliases[@]}"; do
		echo "$va: ${url}@${commit} $version"
	done

	for variant in $variants; do
		commit="$(git log -1 --format='format:%H' -- "$version/$variant")"
		for va in "${versionAliases[@]}"; do
			if [ "$va" = 'latest' ]; then
				va="$variant"
			else
				va="$va-$variant"
			fi
			echo "$va: ${url}@${commit} $version/$variant"
		done
	done
done
