###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import argparse
import os

from ibtimpl.command import *
from ibtimpl.docker_util import *

class RunCommand(Command):
    def __init__(self):
        super(RunCommand, self).__init__("run", "Run command inside container")
        self.parser.add_argument("command", metavar="COMMAND", help="command")
        self.parser.add_argument("args", metavar="ARGS", nargs=argparse.REMAINDER, help="arguments")

    def run(self, ctx, args):
        if not docker_image_exists(ctx.image_id):
            raise RuntimeError("Project has not been upped")

        rel_dir = os.path.relpath(ctx.dir, ctx.project_dir)
        container_working_dir = os.path.join(ctx.container_project_dir, rel_dir)

        local_run_path = os.path.join(ctx.dot_dir, SCRIPT_FILE_NAME)
        container_run_path = os.path.join(ctx.container_dot_dir, SCRIPT_FILE_NAME)

        with open(local_run_path, "wt") as f:
            f.write("#!/bin/sh\n")
            f.write(" ".join([args.command] + args.args) + "\n")

        docker_run(ctx, container_working_dir, container_run_path)