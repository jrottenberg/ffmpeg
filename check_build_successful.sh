#!/usr/bin/env bash

set -e

if [[ -z ${1} ]];then
    STR_COUNT=1
else
    STR_COUNT=${1}
fi

PROJECT_DIR=$(dirname $0)
LOG_FILES=$(find ${PROJECT_DIR} -name stdout | sort)

for FILE in ${LOG_FILES} ; do
    LAST_STRING=$(tail -n 1 ${FILE})
    if [[ $(echo -n ${LAST_STRING} | grep Successfully) ]]; then
        echo -e '\e[0;32m'"${FILE}"'\e[0m'
        tail -n 1 ${FILE}
    else
        echo -e '\e[0;31m'"${FILE}"'\e[0m'
        tail -n ${STR_COUNT} ${FILE}
    fi
done
