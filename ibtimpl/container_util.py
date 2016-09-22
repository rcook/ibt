###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import colorama
import os
import pipes
import re

from ibtimpl.util import *

def expand(env_vars, value):
    def replace(m):
        key = m.group(1)
        replacement = env_vars.get(key)
        return m.group(0) if replacement is None else replacement

    return re.sub('\$([A-Za-z_][A-Za-z_0-9]*)', replace, value)

def build_command(ctx, container_working_dir, command_args, subcommand):
    additional_args = []

    ports = {}

    ports_setting = ctx.settings.get("ports", None)
    if ports_setting is not None:
        for key in ports_setting:
            host_port = key
            container_port = ports_setting[key]
            if host_port in ports:
                raise RuntimeError("Duplicate host port {}".format(host_port))
            ports[host_port] = container_port

    volumes = {
        ctx.project_info.dir: ctx.container_project_dir,
        ctx.dot_dir: ctx.container_dot_dir
    }

    volumes_setting = ctx.settings.get("volumes", None)
    if volumes_setting is not None:
        for key in volumes_setting:
            local_dir = ctx.resolve_local_path(key)
            container_dir = volumes_setting[key]
            if local_dir in volumes:
                raise RuntimeError("Duplicate volume {}".format(local_dir))
            volumes[local_dir] = container_dir

    _, _, _, user_name = ctx.user_info()

    env_vars = {
        "IBTPROJECTDIR": ctx.container_project_dir,
        "IBTUSER": user_name
    }

    command = [
        "docker",
        "run",
        "-w",
        container_working_dir,
        "-u",
        user_name,
        "--rm"
    ] + \
        sum([["-p", "{}:{}".format(key, ports[key])] for key in ports], []) + \
        sum([["-v", "{}:{}".format(key, expand(env_vars, volumes[key]))] for key in volumes], []) + \
        sum([["-e", "{}={}".format(key, env_vars[key])] for key in env_vars], []) + \
        additional_args + \
        ([] if command_args is None else command_args) + \
        [ctx.image_id] + \
        ([] if subcommand is None else subcommand)

    return command, volumes

def shell_join(command):
    return " ".join(pipes.quote(s) for s in command)

def trace_command(command):
    print(colorama.Fore.YELLOW + shell_join(command) + colorama.Style.RESET_ALL)

def check_process_in_container(ctx, args, container_working_dir, command_args=None, subcommand=None):
    command, volumes = build_command(ctx, container_working_dir, command_args, subcommand)
    if args.trace:
        trace_command(command)
    with ensure_mount_sources(volumes.keys()):
        subprocess.check_call(command)

def call_process_in_container(ctx, args, container_working_dir, command_args=None, subcommand=None):
    command, volumes = build_command(ctx, container_working_dir, command_args, subcommand)
    if args.trace:
        trace_command(command)
    with ensure_mount_sources(volumes.keys()):
        return subprocess.call(command)
