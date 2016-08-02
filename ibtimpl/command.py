###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

class Command(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self): return self._name
