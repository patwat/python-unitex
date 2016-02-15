#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, unittest

from unitex.io import *



class Arguments:

    def __init__(self, language=None):
        self.__arguments = {}

        self.__arguments["file_source"] = "data/corpus.txt"
        self.__arguments["file_target_hdd_01"] = "data/corpus-hdd-01.txt"
        self.__arguments["file_target_hdd_02"] = "data/corpus-hdd-02.txt"
        self.__arguments["file_target_vfs_01"] = "%sdata/corpus-vfs-01.txt" % UnitexIOConstants.VFS_PREFIX
        self.__arguments["file_target_vfs_02"] = "%sdata/corpus-vfs-02.txt" % UnitexIOConstants.VFS_PREFIX

        self.__arguments["virtual_file_hdd_01"] = "data/corpus-virtual-file-01.txt"
        self.__arguments["virtual_file_hdd_02"] = "data/corpus-virtual-file-02.txt"
        self.__arguments["virtual_file_vfs_01"] = "%sdata/corpus-virtual-file-01.txt" % UnitexIOConstants.VFS_PREFIX
        self.__arguments["virtual_file_vfs_02"] = "%sdata/corpus-virtual-file-02.txt" % UnitexIOConstants.VFS_PREFIX

        self.__arguments["directory"] = "data/biniou/"

    def __getitem__(self, key):
        if key not in self.__arguments:
            raise KeyError("Argument '%s' not found ..." % key)
        return self.__arguments[key]



class TestUnitexIO(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._arguments = Arguments()

    @classmethod
    def tearDownClass(self):
        if os.path.exists(self._arguments["file_target_hdd_01"]):
            os.remove(self._arguments["file_target_hdd_01"])

        if os.path.exists(self._arguments["file_target_hdd_02"]):
            os.remove(self._arguments["file_target_hdd_02"])

        if os.path.exists(self._arguments["directory"]):
            shutil.rmtree(self._arguments["directory"])

    def test_01_enable_stdout(self):
        ret = enable_stdout()
        self.assertTrue(ok, "STDOUT enabling failed!")

    def test_02_disable_stdout(self):
        ret = disable_stdout()
        self.assertTrue(ok, "STDOUT disabling failed!")

    def test_03_enable_stderr(self):
        ret = enable_stderr()
        self.assertTrue(ok, "STDERR enabling failed!")

    def test_04_disable_stderr(self):
        ret = disable_stderr()
        self.assertTrue(ok, "STDERR disabling failed!")

    def test_05_01_cp_hdd(self):
        raise NotImplementedError

    def test_05_02_cp_vfs(self):
        raise NotImplementedError

    def test_06_01_rm_hdd(self):
        raise NotImplementedError

    def test_06_02_rm_vfs(self):
        raise NotImplementedError

    def test_07_01_mv_hdd(self):
        raise NotImplementedError

    def test_07_02_mv_vfs(self):
        raise NotImplementedError

    def test_08_mkdir(self):
        raise NotImplementedError

    def test_09_rmdir(self):
        raise NotImplementedError

    def test_10_ls_hdd(self):
        raise NotImplementedError

    def test_10_ls_vfs(self):
        raise NotImplementedError

    def test_11_01_01_virtual_file_read_hdd(self):
        raise NotImplementedError

    def test_11_01_02_virtual_file_read_vfs(self):
        raise NotImplementedError

    def test_11_02_01_virtual_file_write_hdd(self):
        raise NotImplementedError

    def test_11_02_02_virtual_file_write_vfs(self):
        raise NotImplementedError

    def test_11_03_01_virtual_file_append_hdd(self):
        raise NotImplementedError

    def test_11_03_02_virtual_file_append_vfs(self):
        raise NotImplementedError



if __name__ == '__main__':
    unittest.main()
