###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from __future__ import print_function
import os

from ibtimpl.command import Command
from ibtimpl.docker_util import docker_image_build, docker_image_remove
from ibtimpl.tracing import trace_data
from ibtimpl.util import temp_dir

class UpCommand(Command):
    def __init__(self):
        super(UpCommand, self).__init__("up")

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Create project image")
        p.add_argument("--destroy", "-d", action="store_true", help="destroy before recreating project image")
        p.add_argument("--docker-build", "-b", action="store_true", help="rebuild base image before creating project image")
        p.add_argument("--config", "-c", help="specify a Docker configuration")
        p.set_defaults(handler=self.run)

    def run(self, ctx, args):
        parent_settings = ctx.settings if args.config is None else ctx.settings["configurations"][args.config]

        docker = parent_settings.get("docker", None)
        if docker is None:
            docker_image = None
            docker_build = None
        else:
            docker_image = docker.get("image", None)
            docker_build = docker.get("build", None)

        trace_data(args, docker)

        if args.docker_build:
            if docker_build is None:
                raise RuntimeError("No build commands configured for Docker base image")
            else:
                with temp_file() as temp_path:
                    make_shell_script(temp_path, ["cd {}".format(ctx.project_info.dir)] + docker_build)
                    subprocess.check_call(["/bin/sh", temp_path])

        if args.destroy:
            docker_image_remove(ctx.image_id)

        with temp_dir() as dir:
            if docker_image is None:
                raise RuntimeError("No Docker base image is configured")
            else:
                uid, group_name, gid, user_name = ctx.user_info()
                with open(os.path.join(dir, "Dockerfile"), "wt") as f:
                    f.write("FROM {}\n".format(docker_image))
                    f.write("RUN groupadd -g {} {}\n".format(gid, group_name))
                    f.write("RUN useradd -l -u {} -g {} {}\n".format(uid, gid, user_name))

            with open(os.path.join(dir, ".dockerignore"), "wt") as f:
                f.write("*\n")

            docker_image_build(ctx.image_id, dir)
