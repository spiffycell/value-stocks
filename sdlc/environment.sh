#!/bin/bash

set -eEu
set -o pipefail

export VCS_REF="${VCS_REF:-unset}"
export BUILD_DATE="${BUILD_DATE:-unset}"
export VERSION="${VERSION:-unset}"

# assign and set readonly var
python_path="$(python3 -c "import site; print(site.USER_BASE)")"
readonly python_path

# show PATH, check for user_base
# if not in PATH, add it
if ! printenv PATH | grep ":${python_path}/bin[:$]" >/dev/null 2>&1; then
  export PATH="${PATH}:${python_path}/bin"
fi
