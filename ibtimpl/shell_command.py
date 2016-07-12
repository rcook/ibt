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

class ShellCommand(Command):
    def __init__(self):
        super(ShellCommand, self).__init__("shell", "Run shell inside container")

    def run(self, ctx, args):
        if not docker_image_exists(ctx.image_id):
            raise RuntimeError("Project has not been upped")

        rel_dir = os.path.relpath(ctx.dir, ctx.project_dir)
        container_working_dir = os.path.join(ctx.container_project_dir, rel_dir)

        command = make_run_command(ctx, container_working_dir, ["-it"]) + args
        subprocess.check_call(command)
