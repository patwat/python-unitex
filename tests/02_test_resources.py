#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, unittest

from unitex.resources import *
from unitex.tools import compress



class Arguments:

    def __init__(self, language=None):
        self.__arguments = {}

        self.__arguments["dic"] = "data/dictionary.dic" 
        self.__arguments["bin"] = "data/dictionary.bin" 
        self.__arguments["inf"] = "data/dictionary.inf" 

        self.__arguments["fst2"] = "data/Sentence.fst2" 

        self.__arguments["alphabet"] = "data/Alphabet.txt" 

    def __getitem__(self, key):
        if key not in self.__arguments:
            raise KeyError("Value key '%s' not found..." % key)
        return self.__arguments[key]

    def __setitem__(self, key, value):
        if key in self.__arguments:
            raise KeyError("Value key '%s' already exists" % key)
        self.__arguments[key] = value



class TestUnitexResources(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._arguments = Arguments()

    @classmethod
    def tearDownClass(self):
        # Removing output file from the 'compress' command.
        if os.path.exists(self._arguments["bin"]):
            os.remove(self._arguments["bin"])
        if os.path.exists(self._arguments["inf"]):
            os.remove(self._arguments["inf"])

    def test_01_load_dictionary(self):
        args = [self._arguments["dic"]]

        kwargs = {}
        kwargs["flip"] = False
        kwargs["semitic"] = False
        kwargs["version"] = "v2"

        ret = compress(*args, **kwargs)

        path = self._arguments["bin"]

        output = load_persistent_dictionary(path)
        self._arguments["persistent-dictionary"] = output

        ok = is_persistent_dictionary(output)

        self.assertTrue(ok, "Dictionary loading failed!")

    def test_02_unload_dictionary(self):
        path = self._arguments["persistent-dictionary"]

        free_persistent_dictionary(path)
        ok = not is_persistent_dictionary(path)

        self.assertTrue(ok, "Dictionary freeing failed!")

    def test_03_load_fst2(self):
        path = self._arguments["fst2"]

        output = load_persistent_fst2(path)
        self._arguments["persistent-fst2"] = output

        ok = is_persistent_fst2(output)

        self.assertTrue(ok, "Fst2 loading failed!")

    def test_04_unload_fst2(self):
        path = self._arguments["persistent-fst2"]

        free_persistent_fst2(path)
        ok = not is_persistent_fst2(path)

        self.assertTrue(ok, "Fst2 freeing failed!")

    def test_05_load_alphabet(self):
        path = self._arguments["alphabet"]

        output = load_persistent_alphabet(path)
        self._arguments["persistent-alphabet"] = output

        ok = is_persistent_alphabet(output)

        self.assertTrue(ok, "Alphabet loading failed!")

    def test_06_unload_alphabet(self):
        path = self._arguments["persistent-alphabet"]

        free_persistent_alphabet(path)
        ok = not is_persistent_alphabet(path)

        self.assertTrue(ok, "Alphabet freeing failed!")



if __name__ == '__main__':
    unittest.main()
