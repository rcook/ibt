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
from ibtimpl.docker_util import docker_image_exists

class StatusCommand(Command):
    def __init__(self):
        super(StatusCommand, self).__init__("status")

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Show project status")
        p.set_defaults(handler=self.run)

    def run(self, ctx, args):
        uid, group_name, gid, user_name = ctx.user_info()

        print("IBT: Isolated Build Tool")
        print("https://github.com/rcook/ibt\n")
        print("Project information:")
        print("  Project directory:   {}".format(ctx.project_info.dir))
        print("  Working directory:   {}".format(ctx.dir))
        print("  Project ID:          {}".format(ctx.project_id))
        print("  Configuration file:  {}".format(ctx.project_info.config_path))
        print("  Temporary directory: {}".format(ctx.dot_dir))

        print("User information:")
        print("  User:                {} ({})".format(user_name, uid))
        print("  Group:               {} ({})".format(group_name, gid))

        print("Docker container information:")
        print("  Docker image ID:     {}".format(ctx.image_id))
        container_project_dir = ctx.settings.get("container-project-dir", ctx.default_container_project_dir)
        print("  Project directory:   {}".format(container_project_dir))
        print("  Temporary directory: {}".format(ctx.container_dot_dir))
        docker = ctx.settings.get("docker", None)
        docker_image = None if docker is None else docker.get("image", None)
        if docker is None:
            print("  Docker base image:   not configured")
        else:
            print("  Docker base image:   {}".format(docker["image"]))

        print("IBT status:")
        print("  Temporary directory: {}".format("exists" if os.path.isdir(ctx.dot_dir) else "does not exist"))
        print("  Docker image:        {}".format("built" if docker_image_exists(ctx.image_id) else "not built"))

        volumes = ctx.settings.get("volumes", None)
        if volumes is not None and len(volumes) > 0:
            print("\nProject volumes:")
            for key in sorted(volumes):
                local_dir = ctx.resolve_local_path(key)
                print("  {} = {}".format(local_dir, volumes[key]))

        aliases = ctx.settings.get("aliases", None)
        if aliases is not None and len(aliases) > 0:
            print("\nProject aliases:")
            for key in sorted(aliases):
                alias = aliases[key]
                if isinstance(alias, list):
                    print("  {}:".format(key))
                    for line in alias:
                        print("  - {}".format(line))
                else:
                    print("  {} = {}".format(key, alias))

        print("")
