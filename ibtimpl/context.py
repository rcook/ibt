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
import re
import yaml

from ibtimpl.util import *

class Context(object):
    def __init__(self, project_info, dir):
        self._project_info = project_info
        self._dir = dir
        self._project_id = hashlib.md5(self._project_info.dir).hexdigest()
        self._image_id = "ibt-{}".format(self._project_id)
        self._dot_dir = os.path.join(os.path.dirname(self._project_info.config_path), ".ibt")
        self._default_container_project_dir = "/{}".format(os.path.basename(self._project_info.dir))
        self._container_dot_dir = "/.ibt"
        self._settings = None

    @property
    def project_info(self): return self._project_info

    @property
    def dir(self): return self._dir

    @property
    def project_id(self): return self._project_id

    @property
    def image_id(self): return self._image_id

    @property
    def dot_dir(self): return self._dot_dir

    @property
    def default_container_project_dir(self): return self._default_container_project_dir

    @property
    def container_dot_dir(self): return self._container_dot_dir

    @property
    def settings(self):
        if self._settings is None:
            with open(self._project_info.config_path, "rt") as f:
                self._settings = yaml.load(f)
        return self._settings

    def resolve_local_path(self, path):
        return os.path.abspath(os.path.join(self._project_info.dir, path))

    def user_info(self):
      def sanitize(s):
        return re.sub("[{}]".format(re.escape("^")), "_", s)
      return map(sanitize, check_process(["stat", "-c", "%u:%G:%g:%U", self._project_info.dir]).strip().split(":"))
