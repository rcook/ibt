###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import os
import yaml

# Detects current project directory and configuration path based on following
# strategy:
# (1) Look in current directory for Ibtfile
# (2) Look in ancestor directories for Ibtfile up until root of file system
# (3) Look in user .ibtprojects for an entry corresponding to a parent of the
# current directory
class ProjectInfo(object):
    def __init__(self, dir, config_path):
        self._dir = dir
        self._config_path = config_path

    @staticmethod
    def read(dir):
        def find_matching_config_path(projects, original_dir):
            user_dir = os.path.expanduser("~")
            longest_prefix = os.path.abspath("/")
            longest_dir = None
            longest_config_path = None
            for key in projects:
                dir = os.path.abspath(os.path.join(user_dir, key))
                prefix = os.path.commonprefix([dir, original_dir])
                if prefix == dir and len(prefix) > len(longest_prefix):
                    longest_prefix = prefix
                    longest_dir = dir
                    longest_config_path = os.path.abspath(os.path.join(user_dir, projects[key]))
            return longest_dir, longest_config_path

        def read_config(original_dir):
            user_project_path = os.path.expanduser("~/.ibtprojects")
            if not os.path.isfile(user_project_path):
                return None

            with open(user_project_path, "rt") as f:
                config = yaml.load(f)

            projects = config.get("projects", None)
            if projects is None:
                return None

            dir, config_path = find_matching_config_path(projects, original_dir)
            if dir is None:
                return None

            return ProjectInfo(dir, config_path)

        def read_helper(original_dir, dir):
            config_path = os.path.join(dir, "Ibtfile")
            if os.path.isfile(config_path):
                return ProjectInfo(dir, config_path)

            parent_dir = os.path.dirname(dir)
            if parent_dir == dir:
                return read_config(original_dir)
            else:
                return read_helper(original_dir, parent_dir)

        return read_helper(dir, dir)

    @property
    def dir(self): return self._dir

    @property
    def config_path(self): return self._config_path