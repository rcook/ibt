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
        self.parser.add_argument("command", metavar="COMMAND", nargs="?", help="command")
        self.parser.add_argument("args", metavar="ARGS", nargs=argparse.REMAINDER, help="arguments")

    def run(self, ctx, args):
        if not docker_image_exists(ctx.image_id):
            raise RuntimeError("Project has not been upped")

        rel_dir = os.path.relpath(ctx.dir, ctx.project_dir)
        container_working_dir = os.path.join(ctx.container_project_dir, rel_dir)

        user_command = args.args if args.command is None else [args.command] + args.args
        command = make_run_command(ctx, container_working_dir, ["-it"]) + user_command
        subprocess.check_call(command)
