###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from ibtimpl.container_util import *
from ibtimpl.util import *

def docker_installed():
    try:
        return call_process(["docker", "--version"])
    except OSError:
        return False

def docker_image_exists(image_id):
    return call_process(["docker", "inspect", image_id])

def docker_image_build(image_id, context_dir):
    if docker_image_exists(image_id):
        print("Docker image {} already built".format(image_id))
    else:
        print("Building Docker image {}".format(image_id))
        check_process(["docker", "build", "-t", image_id, context_dir])

def docker_image_remove(image_id):
    if docker_image_exists(image_id):
        print("Destroying Docker image {}".format(image_id))
        check_process(["docker", "rmi", image_id])
    else:
        print("No Docker image {} to destroy".format(image_id))

def docker_run(ctx, container_working_dir, container_run_path):
    run_in_container(ctx, container_working_dir, None, ["/bin/sh", container_run_path])
