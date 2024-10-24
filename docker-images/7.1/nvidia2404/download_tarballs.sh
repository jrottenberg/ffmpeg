#!/usr/bin/env bash

# The point of this script is to read in the list of tarballs to download from generated_build_manifest.json
# using jq and then download them into their build directories.
#
# The point, we need robust re-tries, as sometimes the download fails, and we need to be able to re-try.
# and verify that the download was successful.

manifestJsonFile="/tmp/workdir/generated_build_manifest.json"

report_on_failed_downloads() {
    local librariesRaw="$(jq -r '.[] | .library_name' $manifestJsonFile)"
    local libs=( $librariesRaw )
    local count=0

    for i in "${!libs[@]}"; do
        lib_name=${libs[$i]}
        local data=$(jq -r '.[] | select(.library_name == "'${lib_name}'")' $manifestJsonFile)
        build_dir=$(echo "$data" | jq -r '.build_dir')
        tarball_name=$(echo "$data" | jq -r '.tarball_name')
        # if tarball_name does not exist, then it could be a source repo build
        # just check the directory
        if [ -z "$tarball_name" ]; then
            if [ ! -d "$build_dir" ]; then
                echo "Error: $build_dir does not exist"
                ((count++))
            fi
        fi
        if [ ! -f "$build_dir/$tarball_name" ]; then
            echo "Error: $build_dir/$tarball_name does not exist"
            ((count++))
        fi
    done
    echo "Failed to download $count tarballs"
}

actual_number_of_downloads_completed() {
    local librariesRaw="$(jq -r '.[] | .library_name' $manifestJsonFile)"
    local libs=( $librariesRaw )
    local count=0

    for i in "${!libs[@]}"; do
        lib_name=${libs[$i]}
        local data=$(jq -r '.[] | select(.library_name == "'${lib_name}'")' $manifestJsonFile)
        build_dir=$(echo "$data" | jq -r '.build_dir')
        tarball_name=$(echo "$data" | jq -r '.tarball_name')
        # if tarball_name does not exist, then it could be a source repo build
        # just check the directory
        if [[ -z "$tarball_name" || "$tarball_name" == "null" ]]; then
            if [ -d "$build_dir" ]; then
                ((count++))
            fi
        fi
        if [ -f "$build_dir/$tarball_name" ]; then
            ((count++))
        fi
    done
    echo $count  # Return the count as output
}
number_of_tarballs_to_download() {
    local librariesRaw="$(jq -r '.[] | .library_name' $manifestJsonFile)"
    local libs=( $librariesRaw )
    echo "${#libs[@]}" # return count as output
}

download_tarballs() {
    # the default argument of quiet is false
    quiet=${1:-false}
	local librariesRaw="$(jq -r '.[] | .library_name' $manifestJsonFile)"
	local libs=( $librariesRaw )
    echo "Downloading (${#libs[@]} libraries)..."
    for i in "${!libs[@]}"; do
        # echo "Downloading ${libs[$i]}..."
        lib_name=${libs[$i]}
        # use double quotes around '${lib_name}', so Bash will expand the value.
        build_dir=$(jq -r '.[] | select(.library_name == "'${lib_name}'") | .build_dir' $manifestJsonFile)
        download_url=$(jq -r '.[] | select(.library_name == "'${lib_name}'") | .download_url' $manifestJsonFile)
        tarball_name=$(jq -r '.[] | select(.library_name == "'${lib_name}'") | .tarball_name' $manifestJsonFile)
        if [ -z "$build_dir" ]; then
            echo "Error: build_dir, is empty"
            exit 1
        fi

        # does the directory exist? if not make it
        if [ ! -d "$build_dir" ]; then
            mkdir -p "$build_dir"
        fi
        # handle edge case for source repo builds (git clone )
        if [[ -z "$tarball_name" || -z "$download_url" || "$tarball_name" == "null" || "$download_url" == "null" ]]; then
            echo "Warning: tarball_name, or download_url is empty or unset (ok in a source repo build)"
            continue
        fi
        echo "Downloading: ${download_url} to: ${build_dir} ${tarball_name}"
        if [ -z "$build_dir" ] || [ -z "$download_url" ] || [ -z "$tarball_name" ]; then
            echo "Error: build_dir, download_url, or tarball_name is empty"
            exit 1
        fi
        # if the tarball_file does not exhist then download it
        if [ ! -f "$build_dir/$tarball_name" ]; then
            echo "$build_dir/$tarball_name does not exist, downloading now..."
            cd "$build_dir"
            # curl -fsSL -o "$library.tar.gz" "
            # curl command line reference
            #      -o write output to file
            #      -f Fail fast with no output on HTTP errors
            #      -s Silent mode
            #      -S, --show-error  Show error even when -s is used
            #      -L, --location    Follow redirects
            #      --retry <num>     Retry request if transient problems occur
            curl -fsSL --retry 2 -o "$tarball_name" "$download_url"
        else
            # if not quietly, then echo that we are skipping the download
            [ "$quiet" = false ] &&
            echo "$build_dir/$tarball_name already exists, skipping download"
        fi
    done
}

num_to_download=1 # at least 1
num_completed=0
number_of_times_to_retry=6
download_tarballs_called_number=0
num_completed=$(actual_number_of_downloads_completed)
num_to_download=$(number_of_tarballs_to_download)
echo "Starting to download ${num_to_download} tarball images"
while [ $num_completed -lt $num_to_download ] && [ $number_of_times_to_retry -gt $download_tarballs_called_number ]; do
    ((download_tarballs_called_number++))
    download_tarballs
    sleep 5
    num_completed=$(actual_number_of_downloads_completed)
    num_to_download=$(number_of_tarballs_to_download)
    echo "Downloaded ${num_completed} of ${num_to_download} tarball images on pass ${download_tarballs_called_number}"
done

if [ $num_completed -lt $num_to_download ]; then
    echo "Failed to download all tarballs after $download_tarballs_called_number attempts"
    report_on_failed_downloads
    exit 1
fi
echo "Successfully Downloaded the ${num_completed} tarball images after $download_tarballs_called_number attempts"
exit 0
