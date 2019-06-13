#! /bin/sh

variants=("ubuntu" "centos" "alpine", "nvidia", "arm32v7")
versions=("2.8" "3.2" "3.3" "3.4" "4.0" "4.1" "snapshot")

for variant in ${variants[*]}; do
    for version in ${versions[*]}; do 
        echo "${variant}: ffmpeg-${version}"
        dir="docker-images/${version}/${variant}"
        mkdir -p ${dir}
        python3 update.py --slim --enable-all ${variant} ${version} > ${dir}/Dockerfile
    done
done

scratch_variant="alpine"
for version in ${versions[*]}; do 
    dir="docker-images/${version}/${variant}"
    mkdir -p ${dir}
    python3 update.py --scratch --enable-all ${scratch_variant} ${version} > ${dir}/Dockerfile
done

# FFMPEG 2.8 Patches
# FFMPEG requires libssl1.0
sed -ri\
     -e 's/alpine:[[:digit:]]+.[[:digit:]]+/alpine:3.8/' \
     -e 's/libssl1.[[:digit:]]/libssl1.0/' \
     -e 's/libcrypto1.[[:digit:]]/libcrypto1.0/' \
    docker-images/2.8/alpine/Dockerfile