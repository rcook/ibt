###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from __future__ import print_function

from ibtimpl.command import Command

class DestroyCommand(Command):
    def __init__(self):
        super(DestroyCommand, self).__init__("destroy", requires_project=True)

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Destroy project image")
        p.set_defaults(command=self, handler=self.run)

    def run(self, ctx, project, args):
        docker_image_remove(ctx.image_id)
