#!/usr/bin/env bash

manifestJsonFile="/tmp/workdir/generated_build_manifest.json"

extract_tarball() {
    local tarball_name=$1
    # grab the extension of the tarball
    local extension="${tarball_name##*.}"
    # tar extraction args: -z, -j, -J, --lzma  Compress archive with gzip/bzip2/xz/lzma
    if [ "$extension" == "gz" ]; then
        tar -zx --strip-components=1 -f ${tarball_name}
    elif [ "$extension" == "bz2" ]; then
        tar -jx --strip-components=1 -f ${tarball_name}
    elif [ "$extension" == "zx" ]; then
        tar -Jx --strip-components=1 -f ${tarball_name}
    else
        echo "Error while extract_tarball, got an unknown extension: $extension"
    fi
}

read_data_from_manifest() {
    local lib_name=$1
    local data=$(jq -r '.[] | select(.library_name == "'$lib_name'")' $manifestJsonFile)
    local build_dir=$(echo "$data" | jq -r '.build_dir')
    local tarball_name=$(echo "$data" | jq -r '.tarball_name')
    echo "$build_dir $tarball_name"
}
# echo "Building prefix: ${PREFIX}"
# build_opencore_amr
# build_libogg "libogg"
build_libopencore-amr() {
    ./configure --prefix="${PREFIX}" --enable-shared && \
    make && \
    make install 
}

build_support_libraries() {
    local librariesRaw="$(jq -r '.[] | .library_name' $manifestJsonFile)"
    local libs=( $librariesRaw )
    for i in "${!libs[@]}"; do
        lib_name=${libs[$i]}
        local data=$(jq -r '.[] | select(.library_name == "'${lib_name}'")' $manifestJsonFile)
        build_dir=$(echo "$data" | jq -r '.build_dir')
        tarball_name=$(echo "$data" | jq -r '.tarball_name')
        echo "Building $lib_name: in [${build_dir}] from [$tarball_name] source"
        cd $build_dir
        extract_tarball $tarball_name
        # make a callback function to build the library
        # if anything fails, we will exit with a non-zero status
        build_${lib_name} ${lib_name}
    done
}

# First we need to build all of the support  libs that are in a standard'ish format
# that contains a tarball bundle of the source code.
build_support_libraries

# # lib aom 
# # https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu#libaom
# RUN \
#         echo "Building aom-${AOM_VERSION}" && \
#         DIR=/tmp/aom && \
#         git clone --branch ${AOM_VERSION} --depth 1 https://aomedia.googlesource.com/aom ${DIR} ; \
#         cd ${DIR} ; \
#         mkdir -p ./aom_build ; \
#         cd ./aom_build ; \
#         # cmake -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 ..; \
#         cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="${PREFIX}" -DBUILD_SHARED_LIBS=1 -DENABLE_NASM=on ..; \
#         make ; \
#         make install ; \
#         rm -rf ${DIR}

## libpng
# also pulls in a bunch of stuff
# RUN \
#         echo "Building libpng-${LIBPNG_VERSION}" && \
#         DIR=/tmp/png && \
#         mkdir -p ${DIR} && \
#         cd ${DIR} && \
#         git clone https://git.code.sf.net/p/libpng/code ${DIR} -b v${LIBPNG_VERSION} --depth 1 && \
#         ./autogen.sh && \
#         ./configure --prefix="${PREFIX}" && \
#         make check && \
#         make install && \
#         rm -rf ${DIR}
