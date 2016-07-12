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
from ibtimpl.docker_util import *

class DestroyCommand(Command):
    def __init__(self):
        super(DestroyCommand, self).__init__("destroy", "Destroy project image")

    def run(self, ctx, args):
        docker_image_remove(ctx.image_id)