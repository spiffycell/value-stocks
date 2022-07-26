#!/bin/bash

set -eEu
set -o pipefail

##############################################
##### DECLARE FUNCTIONS FOR LATER USE  #######
##############################################
. sdlc/environment.sh

finish() {
    declare -ri RC=$?

    if [[ ${RC} -eq 0 ]]; then
        printf "$0 OK\n"
    else
        printf "$0 failed with exit code ${RC}\n"
    fi
}


check_top_dir() {
    declare git_dir
    git_dir="$(git rev-parse --show-toplevel)"
    readonly git_dir

    if ! [[ "$PWD" == "${git_dir}" ]]; then
        err Please run these scripts from the root of the repo
        exit 1
    fi
}

# in POSIX, besides signals, only EXIT is valid as an event
# you must use bash to use ERR
trap finish EXIT
