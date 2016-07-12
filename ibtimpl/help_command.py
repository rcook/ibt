###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from ibtimpl.command import *
from ibtimpl.util import *

class HelpCommand(Command):
    def __init__(self):
        super(HelpCommand, self).__init__("help", "Display summary of standard commands")

    def run(self, ctx, args):
        print("IBT: Isolated Build Tool\n")

        commands = get_commands()
        aliases = ctx.settings.get("aliases", None)
        has_aliases = aliases is not None and len(aliases) > 0

        max_name_len = 0
        for name in commands:
            if len(name) > max_name_len:
                max_name_len = len(name)

        if has_aliases:
            for key in aliases:
                if len(key) > max_name_len:
                    max_name_len = len(key)

        print("Commands:")
        for name in sorted(commands):
            command = commands[name]
            print("  {}  {}".format(name.ljust(max_name_len), command.parser.description))

        if has_aliases:
            print("\nProject aliases:")
            for key in sorted(aliases):
                print("  {}  {}".format(key.ljust(max_name_len), aliases[key]))

        print("")
