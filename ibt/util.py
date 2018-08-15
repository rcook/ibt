###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2017, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from __future__ import print_function
import contextlib
import grp
import os
import pwd
import re
import shutil
import subprocess32 as subprocess
import tempfile

def _flatten(*args):
    output = []
    for arg in args:
        if hasattr(arg, "__iter__"):
            output.extend(_flatten(*arg))
        else:
            output.append(arg)
    return output

def get_commands():
    if get_commands.commands is None:
        from ibt.destroy_command import DestroyCommand
        from ibt.help_command import HelpCommand
        from ibt.info_command import InfoCommand
        from ibt.run_command import RunCommand
        from ibt.script_command import ScriptCommand
        from ibt.shell_command import ShellCommand
        from ibt.up_command import UpCommand

        commands = [
            DestroyCommand(),
            HelpCommand(),
            InfoCommand(),
            RunCommand(),
            ScriptCommand(),
            ShellCommand(),
            UpCommand()
        ]
        get_commands.commands = {}
        for command in commands:
            get_commands.commands[command.name] = command

    return get_commands.commands
get_commands.commands = None

def call_process(command, timeout=None):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    proc.communicate(timeout=timeout)
    return proc.returncode == 0

def check_process(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    (out, error) = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("Popen command failed: {} (command: {})".format(error, command))
    return out

def make_shell_script(path, lines):
    with open(path, "wt") as f:
        f.write("#!/bin/sh\n")
        for line in lines:
            f.write(line + "\n")

@contextlib.contextmanager
def temp_file(dir=None):
    f, temp_path = tempfile.mkstemp(dir=dir)
    os.close(f)
    try:
        yield temp_path
    finally:
        if os.path.isfile(temp_path):
            os.unlink(temp_path)

@contextlib.contextmanager
def ensure_mount_sources(*paths):
    try:
        cleanup_dirs = []
        for p in _flatten(paths):
            if p is not None and not os.path.isdir(p) and not os.path.isfile(p):
                cleanup_dirs.append(p)
                os.makedirs(p)
        yield
    finally:
        for dir in cleanup_dirs:
            try:
                os.removedirs(dir)
            except OSError:
                pass

@contextlib.contextmanager
def temp_dir(dir=None):
    with ensure_mount_sources(dir):
        temp_path = tempfile.mkdtemp(dir=dir)
        try:
            yield temp_path
        finally:
            if os.path.isdir(temp_path):
                shutil.rmtree(temp_path)

def shell_join(command):
    return " ".join(pipes.quote(s) for s in command)

def show_banner():
    print("IBT: Isolated Build Tool")
    print("https://github.com/rcook/ibt")
    print()

def get_user_info(working_dir):
    # Generate a (hopefully) valid user/group name
    def _sanitize(s):
        return re.sub("[^A-Za-z0-9_-]", "_", s)

    fs = os.stat(working_dir)
    uid = fs.st_uid
    uname = pwd.getpwuid(uid)[0]
    gid = fs.st_gid
    gname = grp.getgrgid(gid)[0]

    # Note the weird order we return the information in...
    return [str(uid), _sanitize(gname), str(gid), _sanitize(uname)]
