#!/bin/bash

###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2017, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

set -euo pipefail
IFS=$'\n\t'

script_dir=$(dirname $(readlink -f $0))
python_path=$script_dir/bin/python

$script_dir/bootstrap.sh $script_dir/ibt.py $*
