###############################################################################
#
# IBT: Isolated Build Tool
# Copyright (C) 2016, Richard Cook. All rights reserved.
#
# Simple wrappers around Docker etc. for fully isolated build environments
#
###############################################################################

from __future__ import print_function
import doctest
import importlib
import pkgutil
import unittest

def _get_module_names(package_name):
    return ["{}.{}".format(package_name, name) for _, name, _ in pkgutil.walk_packages([package_name])]

def _get_test_suite(module_name):
    try:
        return doctest.DocTestSuite(importlib.import_module(module_name))
    except ValueError:
        return

def suite():
    suite = unittest.TestSuite()
    for module_name in _get_module_names("ibt"):
        tests = _get_test_suite(module_name)
        if tests:
            suite.addTests(tests)

    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
