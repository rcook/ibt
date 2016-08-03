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
from ibtimpl.container_util import *
from ibtimpl.docker_util import *
from ibtimpl.util import *

class ShellCommand(Command):
    def __init__(self):
        super(ShellCommand, self).__init__("shell")

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Run interactive shell inside container")
        p.add_argument("command", metavar="COMMAND", nargs="?", help="command")
        p.add_argument("args", metavar="ARGS", nargs=argparse.REMAINDER, help="arguments")
        p.set_defaults(handler=self.run)

    def run(self, ctx, args):
        if not docker_image_exists(ctx.image_id):
            raise RuntimeError("Project has not been upped")

        rel_dir = os.path.relpath(ctx.dir, ctx.project_info.dir)
        container_working_dir = os.path.join(ctx.container_project_dir, rel_dir)

        user_command = args.args if args.command is None else [args.command] + args.args
        status = call_process_in_container(ctx, args, container_working_dir, ["-it"], user_command)
        if status != 0:
            print("Shell returned {}".format(status))
