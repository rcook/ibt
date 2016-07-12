import subprocess

SCRIPT_FILE_NAME = "temp.sh"

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

def user_info(dir):
    return check_process(["stat", "-c", "%u:%G:%g:%U", dir]).strip().split(":")
