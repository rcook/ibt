###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import os

from ibtimpl.command import *
from ibtimpl.docker_util import *
from ibtimpl.util import *

class StatusCommand(Command):
    def __init__(self):
        super(StatusCommand, self).__init__("status", "Show project status")

    def run(self, ctx, args):
        (uid, group_name, gid, user_name) = user_info(ctx.project_dir)

        print("IBT: Isolated Build Tool\n")
        print("Project information:")
        print("  Project directory:   {}".format(ctx.project_dir))
        print("  Working directory:   {}".format(ctx.dir))
        print("  Project ID:          {}".format(ctx.project_id))
        print("  Configuration file:  {}".format(ctx.config_path))
        print("  Temporary directory: {}".format(ctx.dot_dir))
        print("User information:")
        print("  User:                {} ({})".format(user_name, uid))
        print("  Group:               {} ({})".format(group_name, gid))
        print("Docker container information:")
        print("  Docker image ID:     {}".format(ctx.image_id))
        print("  Project directory:   {}".format(ctx.container_project_dir))
        print("  Temporary directory: {}".format(ctx.container_dot_dir))
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
                print("  {} = {}".format(key, aliases[key]))

        print("")
