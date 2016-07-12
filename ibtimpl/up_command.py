import argparse
import os

from ibtimpl.command import *
from ibtimpl.docker_util import *
from ibtimpl.util import *

class UpCommand(Command):
    def __init__(self):
        super(UpCommand, self).__init__("up", "Create project image")
        self.parser.add_argument("--force", "-f", action="store_true", help="destroy and recreate project image")

    def run(self, ctx, args):
        with open(os.path.join(ctx.dot_dir, ".dockerignore"), "wt") as f:
            f.write("*\n")

        (uid, group_name, gid, user_name) = user_info(ctx.project_dir)

        with open(os.path.join(ctx.dot_dir, "Dockerfile"), "wt") as f:
            f.write("FROM {}\n".format(ctx.settings["docker-image"]))
            f.write("RUN groupadd -g {} {}\n".format(gid, group_name))
            f.write("RUN useradd -u {} -g {} {}\n".format(uid, gid, user_name))

        if args.force:
            docker_image_remove(ctx.image_id)
        docker_image_build(ctx.image_id, ctx.dot_dir)