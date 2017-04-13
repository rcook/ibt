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
from ibtimpl.info_command import show_info
from ibtimpl.util import show_banner

class StatusCommand(Command):
    def __init__(self):
        super(StatusCommand, self).__init__("status", requires_project=True)

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Show project status")
        p.set_defaults(command=self, handler=self.run)

    def run(self, ctx, project, args):
        show_banner()
        show_info(ctx)
        uid, group_name, gid, user_name = project.user_info()

        print("Project information:")
        print("  Project directory:   {}".format(project.root_dir))
        print("  Project ID:          {}".format(project.project_id))
        print("  Configuration file:  {}".format(project.config_path))
        print("  Temporary directory: {}".format(project.dot_dir))
        print()

        print("Project user information:")
        print("  User:                {} ({})".format(user_name, uid))
        print("  Group:               {} ({})".format(group_name, gid))
        print()

        print("Docker container information:")
        print("  Docker image ID:     {}".format(project.image_id))
        container_project_dir = project.settings.get("container-project-dir", project.default_container_project_dir)
        print("  Project directory:   {}".format(container_project_dir))
        print("  Temporary directory: {}".format(project.container_dot_dir))
        docker = project.settings.get("docker", None)
        docker_image = None if docker is None else docker.get("image", None)
        if docker is None:
            print("  Docker base image:   not configured")
        else:
            print("  Docker base image:   {}".format(docker["image"]))
        print()

        print("IBT status:")
        print("  Temporary directory: {}".format("exists" if os.path.isdir(project.dot_dir) else "does not exist"))
        print("  Docker image:        {}".format("built" if docker_image_exists(project.image_id) else "not built"))

        volumes = project.settings.get("volumes", None)
        if volumes is not None and len(volumes) > 0:
            print("\nProject volumes:")
            for key in sorted(volumes):
                local_dir = project.resolve_local_path(key)
                print("  {} = {}".format(local_dir, volumes[key]))

        aliases = project.settings.get("aliases", None)
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

        print()
