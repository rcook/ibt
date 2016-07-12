###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import argparse
import shutil
import os

from ibtimpl.command import *
from ibtimpl.docker_util import *

class ScriptCommand(Command):
    def __init__(self):
        super(ScriptCommand, self).__init__("script", "Run script inside container")

    def run(self, ctx, args):
        if len(args) != 1:
            raise RuntimeError("script takes one argument")

        if not docker_image_exists(ctx.image_id):
            raise RuntimeError("Project has not been upped")

        rel_dir = os.path.relpath(ctx.dir, ctx.project_dir)
        container_working_dir = os.path.join(ctx.container_project_dir, rel_dir)

        local_run_path = os.path.join(ctx.dot_dir, SCRIPT_FILE_NAME)
        container_run_path = os.path.join(ctx.container_dot_dir, SCRIPT_FILE_NAME)

        shutil.copyfile(args[0], os.path.join(ctx.dot_dir, "script"))
        container_script_path = os.path.join(ctx.container_dot_dir, "script")

        with open(local_run_path, "wt") as f:
            f.write("#!/bin/sh\n")
            f.write("chmod +x {}\n".format(container_script_path))
            f.write(container_script_path + "\n")

        docker_run(ctx, container_working_dir, container_run_path)
