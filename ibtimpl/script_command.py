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
        super(ScriptCommand, self).__init__("script")

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Run script inside container")
        p.add_argument("script_path", metavar="SCRIPTPATH", help="script to run")
        p.set_defaults(handler=self.run)

    def run(self, ctx, args):
        if not docker_image_exists(ctx.image_id):
            raise RuntimeError("Project has not been upped")

        rel_dir = os.path.relpath(ctx.dir, ctx.project_info.dir)
        container_working_dir = os.path.join(ctx.container_project_dir, rel_dir)

        with temp_dir(ctx.dot_dir) as dir:
            local_path = os.path.join(dir, "script")
            container_path = os.path.join(ctx.container_dot_dir, os.path.relpath(local_path, ctx.dot_dir))

            local_input_path = os.path.join(dir, "input")
            container_input_path = os.path.join(ctx.container_dot_dir, os.path.relpath(local_input_path, ctx.dot_dir))

            shutil.copyfile(args.script_path, local_input_path)

            with open(local_path, "wt") as f:
                f.write("#!/bin/sh\n")
                f.write("chmod +x {}\n".format(container_input_path))
                f.write(container_input_path + "\n")

            docker_run(ctx, args, container_working_dir, container_path)
