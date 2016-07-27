###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import os

from ibtimpl.util import *

def run_in_container(ctx, container_working_dir, args=None, subcommand=None):
    additional_args = []

    ports = ctx.settings.get("port", None)
    if ports is not None:
        for entry in ports:
            additional_args.append("-p")
            additional_args.append(entry)

    volumes = {
        ctx.project_info.dir: ctx.container_project_dir,
        ctx.dot_dir: ctx.container_dot_dir
    }

    volumes_setting = ctx.settings.get("volumes", None)
    if volumes_setting is not None:
        for key in volumes_setting:
            local_dir = ctx.resolve_local_path(key)
            container_dir = volumes_setting[key]
            if local_dir in volumes:
                raise RuntimeError("Duplicate volume {}".format(local_dir))
            volumes[local_dir] = container_dir

    _, _, _, user_name = ctx.user_info()

    command = [
        "docker",
        "run",
        "-w",
        container_working_dir,
        "-u",
        user_name,
        "--rm",
        "-e",
        "IBTPROJECTDIR={}".format(ctx.container_project_dir)
    ] + \
        sum([["-v", "{}:{}".format(key, volumes[key])] for key in volumes], []) + \
        additional_args + \
        ([] if args is None else args) + \
        [ctx.image_id] + \
        ([] if subcommand is None else subcommand)

    with ensure_dirs(volumes.keys()):
        subprocess.check_call(command)
