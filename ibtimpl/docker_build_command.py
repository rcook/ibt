###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import argparse
import subprocess

from ibtimpl.command import *
from ibtimpl.util import *

class DockerBuildCommand(Command):
    def __init__(self):
        super(DockerBuildCommand, self).__init__("dockerbuild", "Build Docker image")

    def run(self, ctx, args):
        lines = ctx.settings.get("docker-build", None)
        if lines is None:
            raise RuntimeError("Don't know how to build Docker image")

        with temp_file() as temp_path:
            make_shell_script(temp_path, lines)
            subprocess.check_call(["/bin/sh", temp_path])
