#!/usr/bin/env python

###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from __future__ import print_function
import argparse
import colorama
import os
import sys

from ibtimpl.context import Context
from ibtimpl.docker_util import docker_installed
from ibtimpl.help_command import HelpCommand
from ibtimpl.project import Project
from ibtimpl.run_command import RunCommand
from ibtimpl.util import get_commands

_HELP_COMMAND = HelpCommand()
_RUN_COMMAND = RunCommand()

def _show_usage(ctx):
    _HELP_COMMAND.run(ctx, [])

def _format_alias_description(alias):
    if isinstance(alias, list):
        return "  Command:\n{}".format("\n".join(map(lambda x: "  $ {}".format(x), alias)))
    else:
        return "  Command:\n  $ {}".format(alias)

def _handle_alias(parser, alias, ctx, args):
    if isinstance(alias, list):
        _RUN_COMMAND.run_lines(ctx, args, alias)
    else:
        args = parser.parse_args(shlex.split(alias))
        args.handler(ctx, args)

class ThrowingArgumentParserError(Exception):
    def __init__(self, *args, **kwargs):
        super(ThrowingArgumentParserError, self).__init__(*args, **kwargs)

class ThrowingArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(ThrowingArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        raise ThrowingArgumentParserError(message)

    def show_usage_and_exit(self):
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(2, _('%(prog)s: error: %(message)s\n') % args)

    def parse_args_no_throw(self, argv):
        try:
            return self.parse_args(argv)
        except ThrowingArgumentParserError:
            return

def _main(working_dir, argv):
    ctx = Context(working_dir)

    parser = ThrowingArgumentParser(description="IBT: Isolated Build Tool (https://github.com/rcook/ibt)")
    parser.add_argument("--verbose", "-v", action="store_true", help="output diagnostic information including Docker commands executed by tool")

    subparsers = parser.add_subparsers(
        title="Subcommands and aliases",
        description="Valid subcommands and aliases",
        help="Additional help")

    commands = get_commands()
    for key in sorted(commands):
        command = commands[key]
        command.add_subparser(subparsers)

    command_argv = argv[1 : ]

    # First handle commands that do not need a project
    args = parser.parse_args_no_throw(command_argv)
    if args is not None and not args.command.requires_project:
        args.handler(ctx, args)
        return

    # Can't do much without Docker
    if not docker_installed():
        print("Please install Docker")
        return

    # All commands from this point onwards require a project.
    # Furthermore, to get the full set of available commands, we need a project.
    project = Project.read(working_dir)
    if project is None:
        print("No Ibtfile project configuration file could be found")
        return

    # Special-case the "status" command to report status even
    # if .ibt directory has not been created yet
    if not os.path.isdir(project.dot_dir) and argv[1 : ] == ["status"]:
        StatusCommand().run(ctx, [])
        return

    aliases = project.settings.get("aliases", None)
    if aliases is not None:
        for key in sorted(aliases):
            alias = aliases[key]
            p = subparsers.add_parser(
                key,
                help="<alias>",
                description=_format_alias_description(alias),
                formatter_class=argparse.RawDescriptionHelpFormatter)
            p.set_defaults(handler=
                lambda ctx, args, alias=alias:
                    _handle_alias(parser, alias, ctx, args))

    args = parser.parse_args(command_argv)
    args.handler(ctx, project, args)

if __name__ == "__main__":
    colorama.init()
    _main(os.getcwd(), sys.argv)
