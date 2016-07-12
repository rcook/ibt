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
from ibtimpl.util import *

class UpCommand(Command):
    def __init__(self):
        super(UpCommand, self).__init__("up", "Create project image")
        self.parser.add_argument("--destroy", "-d", action="store_true", help="destroy before recreating project image")
        self.parser.add_argument("--docker-build", "-b", action="store_true", help="rebuild base image before creating project image")

    def run(self, ctx, args):
        with open(os.path.join(ctx.dot_dir, ".dockerignore"), "wt") as f:
            f.write("*\n")

        (uid, group_name, gid, user_name) = user_info(ctx.project_dir)

        with open(os.path.join(ctx.dot_dir, "Dockerfile"), "wt") as f:
            f.write("FROM {}\n".format(ctx.settings["docker-image"]))
            f.write("RUN groupadd -g {} {}\n".format(gid, group_name))
            f.write("RUN useradd -u {} -g {} {}\n".format(uid, gid, user_name))

        if args.docker_build:
            lines = ctx.settings.get("docker-build", None)
            if lines is not None:
                with temp_file() as temp_path:
                    make_shell_script(temp_path, ["cd {}".format(ctx.project_dir)] + lines)
                    subprocess.check_call(["/bin/sh", temp_path])

        if args.destroy:
            docker_image_remove(ctx.image_id)

        docker_image_build(ctx.image_id, ctx.dot_dir)
