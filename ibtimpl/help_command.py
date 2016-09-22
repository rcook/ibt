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
        super(HelpCommand, self).__init__("help")

    def add_subparser(self, subparsers):
        p = subparsers.add_parser(self.name, help="Display summary of standard commands")
        p.set_defaults(handler=self.run)

    def run(self, ctx, args):
        print("IBT: Isolated Build Tool")
        print("https://github.com/rcook/ibt\n")

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
            print("  {}  (help not implemented)".format(name.ljust(max_name_len)))

        if has_aliases:
            print("\nProject aliases:")
            for key in sorted(aliases):
                alias = aliases[key]
                if isinstance(alias, list):
                    print("  {}:".format(key))
                    for line in alias:
                        print("  - {}".format(line))
                else:
                    print("  {}  {}".format(key.ljust(max_name_len), alias))

        print("")
