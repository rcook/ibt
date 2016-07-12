import subprocess

SCRIPT_FILE_NAME = "temp.sh"

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
