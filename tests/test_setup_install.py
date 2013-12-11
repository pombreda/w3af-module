import os
import sys
import shlex
import unittest
import subprocess


class TestInstall(unittest.TestCase):

    UNINSTALL_CMD = 'pip uninstall -y w3af'
    INSTALL_CMD = '%s setup.py install' % sys.executable
    NULL = open(os.devnull, 'w')

    @classmethod
    def setUpClass(cls):
        subprocess.check_call(shlex.split(cls.INSTALL_CMD),
                              stdout=cls.NULL, stderr=subprocess.STDOUT)

    @classmethod
    def tearDownClass(cls):
        subprocess.check_call(shlex.split(cls.UNINSTALL_CMD),
                              stdout=cls.NULL, stderr=subprocess.STDOUT)

    def test_version_txt(self):
        # Get the location for the w3af module
        FILE_CMD = "%s -c 'import w3af; print w3af.__file__'" % sys.executable
        module_file = subprocess.check_output(shlex.split(FILE_CMD))

        # Append it with the location for the version.txt file
        module_dir = module_file.replace('__init__.pyc', '')
        version_txt = os.path.join(module_dir, 'core/data/constants/version.txt')

        # Check that the file was installed
        msg = '"%s" does NOT exist' % version_txt
        self.assertTrue(os.path.exists(version_txt), msg)

    def test_get_version_call(self):
        VERSION_CMD = "%s -c 'from w3af.core.controllers.misc.get_w3af_version"\
                      " import get_w3af_version; print get_w3af_version()'"
        subprocess.check_call(shlex.split(VERSION_CMD % sys.executable),
                              stdout=self.NULL, stderr=subprocess.STDOUT)

    def test_import(self):
        IMPORT_CMD = "%s -c 'import w3af'" % sys.executable
        subprocess.check_call(shlex.split(IMPORT_CMD),
                              stdout=self.NULL, stderr=subprocess.STDOUT)