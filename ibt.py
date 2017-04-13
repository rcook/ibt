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
from ibtimpl.project_info import ProjectInfo
from ibtimpl.run_command import RunCommand
from ibtimpl.util import get_commands

HELP_COMMAND = HelpCommand()
RUN_COMMAND = RunCommand()

def show_usage(ctx):
    HELP_COMMAND.run(ctx, [])

def run_command(ctx, argv):
    name = argv[0]
    command = get_commands().get(name, None)
    if command is None:
        print("Unrecognized command \"{}\"!\n".format(name))
        show_usage(ctx)
        return

    args = command.parser.parse_args(argv[1 : ])
    command.run(ctx, args)

def format_alias_description(alias):
    if isinstance(alias, list):
        return "  Command:\n{}".format("\n".join(map(lambda x: "  $ {}".format(x), alias)))
    else:
        return "  Command:\n  $ {}".format(alias)

def handle_alias(parser, alias, ctx, args):
    if isinstance(alias, list):
        RUN_COMMAND.run_lines(ctx, args, alias)
    else:
        args = parser.parse_args(shlex.split(alias))
        args.handler(ctx, args)

def main(dir, argv):
    if not docker_installed():
        print("Please install Docker")
        return

    project_info = ProjectInfo.read(dir)
    if project_info is None:
        print("No Ibtfile project configuration file could be found")
        return

    ctx = Context(project_info, dir)

    # Special-case the "status" command to report status even
    # if .ibt directory has not been created yet
    if not os.path.isdir(ctx.dot_dir) and argv[1 : ] == ["status"]:
        StatusCommand().run(ctx, [])
        return

    parser = argparse.ArgumentParser(description="IBT: Isolated Build Tool (https://github.com/rcook/ibt)")
    parser.add_argument("--trace", "-t", action="store_true", help="trace Docker commands executed by tool")

    subparsers = parser.add_subparsers(
        title="Subcommands and aliases",
        description="Valid subcommands and aliases",
        help="Additional help")

    commands = get_commands()
    for key in sorted(commands):
        command = commands[key]
        command.add_subparser(subparsers)

    aliases = ctx.settings.get("aliases", None)
    if aliases is not None:
        for key in sorted(aliases):
            alias = aliases[key]
            p = subparsers.add_parser(
                key,
                help="<alias>",
                description=format_alias_description(alias),
                formatter_class=argparse.RawDescriptionHelpFormatter)
            p.set_defaults(handler=
                lambda ctx, args, alias=alias:
                   handle_alias(parser, alias, ctx, args))

    args = parser.parse_args(argv[1 : ])
    args.handler(ctx, args)

if __name__ == "__main__":
    colorama.init()
    main(os.getcwd(), sys.argv)
