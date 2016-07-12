###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import hashlib
import os
import yaml

class Context(object):
    def __init__(self, dir, config_path):
        self._dir = dir
        self._config_path = config_path
        self._project_id = hashlib.md5(self._config_path).hexdigest()
        self._image_id = "ibt-{}".format(self._project_id)
        self._project_dir = os.path.dirname(self._config_path)
        self._dot_dir = os.path.join(self._project_dir, ".ibt")
        self._container_project_dir = "/{}".format(os.path.basename(self._project_dir))
        self._container_dot_dir = os.path.join(self._container_project_dir, ".ibt")
        self._settings = None

    @property
    def config_path(self): return self._config_path

    @property
    def dir(self): return self._dir

    @property
    def project_id(self): return self._project_id

    @property
    def image_id(self): return self._image_id

    @property
    def project_dir(self): return self._project_dir

    @property
    def dot_dir(self): return self._dot_dir

    @property
    def container_project_dir(self): return self._container_project_dir

    @property
    def container_dot_dir(self): return self._container_dot_dir

    @property
    def settings(self):
        if self._settings is None:
            with open(self._config_path, "rt") as f:
                self._settings = yaml.load(f)
        return self._settings
