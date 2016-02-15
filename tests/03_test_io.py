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

        self.__arguments["hdd_root"] = "data/"
        self.__arguments["vfs_root"] = "%sdata/" % UnitexIOConstants.VFS_PREFIX

        self.__arguments["hdd_name"] = "corpus.txt"
        self.__arguments["vfs_name"] = "$:data/unitex-file-corpus.txt"

        self.__arguments["unitex_file_hdd"] = "data/unitex-file-corpus.txt"
        self.__arguments["unitex_file_vfs"] = "%sdata/unitex-file-corpus.txt" % UnitexIOConstants.VFS_PREFIX

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

        if os.path.exists(self._arguments["unitex_file_hdd"]):
            os.remove(self._arguments["unitex_file_hdd"])

    def test_01_enable_stdout(self):
        ret = enable_stdout()
        self.assertTrue(ret, "STDOUT enabling failed!")

    def test_02_disable_stdout(self):
        ret = disable_stdout()
        self.assertTrue(ret, "STDOUT disabling failed!")

    def test_03_enable_stderr(self):
        ret = enable_stderr()
        self.assertTrue(ret, "STDERR enabling failed!")

    def test_04_disable_stderr(self):
        ret = disable_stderr()
        self.assertTrue(ret, "STDERR disabling failed!")

    def test_05_01_cp_hdd(self):
        ret = cp(self._arguments["file_source"], self._arguments["file_target_hdd_01"])

        ok = ret and os.path.exists(self._arguments["file_target_hdd_01"])

        self.assertTrue(ok, "Copy to disk failed!")

    def test_05_02_cp_vfs(self):
        ret = cp(self._arguments["file_source"], self._arguments["file_target_vfs_01"])

        # Note that this check needs the 'ls' function working...
        vfs_content = ls(self._arguments["vfs_root"])

        ok = ret and self._arguments["file_target_vfs_01"] in vfs_content

        self.assertTrue(ok, "Copy to VFS failed!")

    def test_06_01_mv_hdd(self):
        ret = mv(self._arguments["file_target_hdd_01"], self._arguments["file_target_hdd_02"])

        ok = ret
        ok = ok and not os.path.exists(self._arguments["file_target_hdd_01"])
        ok = ok and os.path.exists(self._arguments["file_target_hdd_02"])

        self.assertTrue(ok, "Move from/to disk failed!")

    def test_06_02_mv_vfs(self):
        ret = mv(self._arguments["file_target_vfs_01"], self._arguments["file_target_vfs_02"])

        # Note that this check needs the 'ls' function working...
        vfs_content = ls(self._arguments["vfs_root"])

        ok = ret
        ok = ok and not self._arguments["file_target_vfs_01"] in vfs_content
        ok = ok and self._arguments["file_target_vfs_02"] in vfs_content

        self.assertTrue(ok, "Move from/to VFS failed!")

    def test_07_01_rm_hdd(self):
        ret = rm(self._arguments["file_target_hdd_02"])

        ok = ret
        ok = ok and not os.path.exists(self._arguments["file_target_hdd_02"])

        self.assertTrue(ok, "Remove from disk failed!")

    def test_07_02_rm_vfs(self):
        ret = rm(self._arguments["file_target_vfs_02"])

        # Note that this check needs the 'ls' function working...
        vfs_content = ls(self._arguments["vfs_root"])

        ok = ret
        ok = ok and not self._arguments["file_target_vfs_02"] in vfs_content

        self.assertTrue(ok, "Remove from disk failed!")

    def test_08_mkdir(self):
        ret = mkdir(self._arguments["directory"])

        ok = ret and os.path.exists(self._arguments["directory"])

        self.assertTrue(ok, "Make disk directory failed!")

    def test_09_rmdir(self):
        ret = rmdir(self._arguments["directory"])

        ok = ret and not os.path.exists(self._arguments["directory"])

        self.assertTrue(ok, "Remove disk directory failed!")

    def test_10_ls_hdd(self):
        hdd_content = ls(self._arguments["hdd_root"])

        ok = self._arguments["hdd_name"] in hdd_content

        self.assertTrue(ok, "Listing disk directory failed!")

    def test_10_ls_vfs(self):
        ret = cp(self._arguments["file_source"], self._arguments["unitex_file_vfs"])

        vfs_content = ls(self._arguments["vfs_root"])

        ret = rm(self._arguments["unitex_file_vfs"])

        ok = self._arguments["vfs_name"] in vfs_content

        self.assertTrue(ok, "Listing VFS directory failed!")

    def test_11_01_01_unitex_file_read_hdd(self):
        rf = open(self._arguments["file_source"], "r", encoding="utf-8")
        original = rf.read()
        rf.close()

        uf = UnitexFile()
        uf.open(self._arguments["file_source"], "r")
        content = uf.read()
        uf.close()

        ok = original == content

        self.assertTrue(ok, "UnitexFile disk read failed!")

    def test_11_01_02_unitex_file_read_vfs(self):
        rf = open(self._arguments["file_source"], "r", encoding="utf-8")
        original = rf.read()
        rf.close()

        ret = cp(self._arguments["file_source"], self._arguments["unitex_file_vfs"])

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_vfs"], "r")
        content = uf.read()
        uf.close()

        ret = rm(self._arguments["unitex_file_vfs"])

        ok = original == content

        self.assertTrue(ok, "UnitexFile VFS read failed!")

    def test_11_02_01_unitex_file_write_hdd(self):
        rf = open(self._arguments["file_source"], "r", encoding="utf-8")
        original = rf.read()
        rf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_hdd"], "w")
        uf.write(original)
        uf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_hdd"], "r")
        content = uf.read()
        uf.close()

        ok = original == content

        self.assertTrue(ok, "UnitexFile disk write failed!")

    def test_11_02_02_unitex_file_write_vfs(self):
        rf = open(self._arguments["file_source"], "r", encoding="utf-8")
        original = rf.read()
        rf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_vfs"], "w")
        uf.write(original)
        uf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_vfs"], "r")
        content = uf.read()
        uf.close()

        ok = original == content

        self.assertTrue(ok, "UnitexFile VFS write failed!")

    def test_11_03_01_unitex_file_append_hdd(self):
        rf = open(self._arguments["file_source"], "r", encoding="utf-8")
        original = rf.read()
        rf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_hdd"], "a")
        uf.write(original)
        uf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_hdd"], "r")
        content = uf.read()
        uf.close()

        ok = (original+original) == content

        self.assertTrue(ok, "UnitexFile disk append failed!")

    def test_11_03_02_unitex_file_append_vfs(self):
        rf = open(self._arguments["file_source"], "r", encoding="utf-8")
        original = rf.read()
        rf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_vfs"], "a")
        uf.write(original)
        uf.close()

        uf = UnitexFile()
        uf.open(self._arguments["unitex_file_vfs"], "r")
        content = uf.read()
        uf.close()

        ret = rm(self._arguments["unitex_file_vfs"])

        ok = (original+original) == content

        self.assertTrue(ok, "UnitexFile VFS append failed!")



if __name__ == '__main__':
    unittest.main()
