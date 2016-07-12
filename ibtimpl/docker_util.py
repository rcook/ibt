###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from ibtimpl.util import *

def docker_installed():
    try:
        return call_process(["docker", "--version"])
    except OSError:
        return False

def docker_image_exists(image_id):
    return call_process(["docker", "inspect", image_id])

def docker_image_build(image_id, project_dir):
    if docker_image_exists(image_id):
        print("Docker image {} already built".format(image_id))
    else:
        print("Building Docker image {}".format(image_id))
        check_process(["docker", "build", "-t", image_id, project_dir])

def docker_image_remove(image_id):
    if docker_image_exists(image_id):
        print("Destroying Docker image {}".format(image_id))
        check_process(["docker", "rmi", image_id])
    else:
        print("No Docker image {} to destroy".format(image_id))

def make_run_command(ctx, container_working_dir, args=None):
    additional_args = []

    ports = ctx.settings.get("port", None)
    if ports is not None:
        for entry in ports:
            additional_args.append("-p")
            additional_args.append(entry)

    volumes = ctx.settings.get("volumes", None)
    if volumes is not None:
        for key in volumes:
            additional_args.append("-v")
            local_dir = resolve_local_path(ctx, key)
            container_dir = volumes[key]
            additional_args.append("{}:{}".format(local_dir, container_dir))

    (_, _, _, user_name) = user_info(ctx.project_dir)
    front = [
        "docker",
        "run",
        "-w",
        container_working_dir,
        "-u",
        user_name,
        "-v",
        "{}:{}".format(ctx.project_dir, ctx.container_project_dir),
        "--rm",
        "-e",
        "IBTPROJECTDIR={}".format(ctx.container_project_dir)
    ] + additional_args
    back = [ctx.image_id]

    return front + back if args is None else front + args + back

def docker_run(ctx, container_working_dir, container_run_path):
    command = make_run_command(ctx, container_working_dir) + ["/bin/sh", container_run_path]
    subprocess.check_call(command)
