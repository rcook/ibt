###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

import argparse

class Command(object):
    def __init__(self, name, description):
        self._name = name
        self._parser = argparse.ArgumentParser(description=description)

    @property
    def name(self): return self._name

    @property
    def parser(self): return self._parser
