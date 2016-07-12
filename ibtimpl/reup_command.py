###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import argparse

from ibtimpl.command import *
from ibtimpl.destroy_command import *
from ibtimpl.up_command import *

class ReupCommand(Command):
    def __init__(self):
        super(ReupCommand, self).__init__("reup", "Destroy and recreate project image")

    def run(self, ctx, args):
        if len(args) > 0:
            raise RuntimeError("reup takes no arguments")

        DestroyCommand().run(ctx, args)
        UpCommand().run(ctx, args)
