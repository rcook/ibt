###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2017, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from __future__ import print_function

from ibtimpl.command import Command
from ibtimpl.docker_util import docker_installed
from ibtimpl.util import show_banner

class InfoCommand(Command):
    def __init__(self):
        super(InfoCommand, self).__init__("info", requires_project=False)

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Show configuration information")
        p.set_defaults(command=self, handler=self.run)

    def run(self, ctx, _):
        show_banner()
        show_info(ctx)

def show_info(ctx):
    uid, group_name, gid, user_name = ctx.user_info()

    print("System information:")
    print("  Docker:              {}".format("installed" if docker_installed() else "not installed"))
    print()

    print("Context information:")
    print("  Working directory:   {}".format(ctx.working_dir))
    print("  User:                {} ({})".format(user_name, uid))
    print("  Group:               {} ({})".format(group_name, gid))
    print()
