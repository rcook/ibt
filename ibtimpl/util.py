import contextlib
import os
import shutil
import subprocess
import tempfile

def get_commands():
    if get_commands.commands is None:
        from ibtimpl.destroy_command import DestroyCommand
        from ibtimpl.help_command import HelpCommand
        from ibtimpl.run_command import RunCommand
        from ibtimpl.script_command import ScriptCommand
        from ibtimpl.shell_command import ShellCommand
        from ibtimpl.status_command import StatusCommand
        from ibtimpl.up_command import UpCommand

        commands = [
            DestroyCommand(),
            HelpCommand(),
            RunCommand(),
            ScriptCommand(),
            ShellCommand(),
            StatusCommand(),
            UpCommand()
        ]
        get_commands.commands = {}
        for command in commands:
            get_commands.commands[command.name] = command

    return get_commands.commands
get_commands.commands = None

def call_process(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    proc.communicate()
    return proc.returncode == 0

def check_process(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    (out, error) = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("Popen command failed: {}".format(error))
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
def temp_dir(dir=None):
    should_create_dir = dir is not None and not os.path.isdir(dir)
    if should_create_dir:
        os.makedirs(dir)

    temp_path = tempfile.mkdtemp(dir=dir)
    try:
        yield temp_path
    finally:
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)

            if should_create_dir:
                try:
                    os.removedirs(dir)
                except OSError:
                    pass
