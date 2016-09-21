#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from unitex.utils.formats import *



class Arguments:

    def __init__(self, language=None):
        self.__arguments = {}

        self.__arguments["bin-v1"] = "data/dictionary-v1.bin"
        self.__arguments["inf-v1"] = "data/dictionary-v1.inf"
        self.__arguments["enc-v1"] = "utf-16-le"

        self.__arguments["grf"] = "data/automaton.grf"

    def __getitem__(self, key):
        if key not in self.__arguments:
            raise KeyError("Argument '%s' not found ..." % key)
        return self.__arguments[key]



class TestUnitexUtils(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._arguments = Arguments()

    @classmethod
    def tearDownClass(self):
        if os.path.exists(self._arguments["grf"]):
            os.remove(self._arguments["grf"])

    def test_01_grf_build(self):
        grf = GRF("GRF")

        path1 = "président français de la république"
        path2 = "président de la république"
        path3 = "ministre islandais de la défense"
        path4 = "ministre islandais à la défense"
        path5 = "secrétaire d'état à la défense"
        path6 = "secrétaire d'état"
        path7 = "secrétaire"
        path8 = "adjoint au secrétaire d'état"
        path9 = "adjoint au secrétaire d'état à la défense"

        grf.add_path(path1.split())
        grf.add_path(path2.split())
        grf.add_path(path3.split())
        grf.add_path(path4.split())
        grf.add_path(path5.split())
        grf.add_path(path6.split())
        grf.add_path(path7.split())
        grf.add_path(path8.split())
        grf.add_path(path9.split())

        grf.save(self._arguments["grf"])
        self.assertTrue(os.path.exists(self._arguments["grf"]), "GRF creation failed!")

    def test_02_old_dictionary(self):
        dictionary = OldCompiledDictionary()
        dictionary.load(self._arguments["bin-v1"],\
                        self._arguments["inf-v1"],\
                        self._arguments["enc-v1"])

        ret = True if dictionary.find("Sébastien") else False

        self.assertTrue(ret, "Dictionary lookup failed!")

if __name__ == '__main__':
    unittest.main()
