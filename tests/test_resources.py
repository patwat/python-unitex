#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from unitex.resources import *



class Values:

    def __init__(self, language=None):
        self.__values = {}

        self.__values["dictionary"] = "data/persistent-dictionary.bin" 
        self.__values["fst2"] = "data/persistent-fst2.fst2" 
        self.__values["alphabet"] = "data/Alphabet.txt" 

    def __getitem__(self, key):
        if key not in self.__values:
            raise KeyError("Value key '%s' not found..." % key)
        return self.__values[key]

    def __setitem__(self, key, value):
        if key in self.__values:
            raise KeyError("Value key '%s' already exists" % key)
        self.__values[key] = value



class TestUnitexResources(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._values = Values()

    def test_01_load_dictionary(self):
        path = self._values["dictionary"]

        output = load_persistent_dictionary(path)
        self._values["persistent-dictionary"] = output

        ok = is_persistent_dictionary(output)

        self.assertTrue(ok, "Dictionary loading failed!")

    def test_02_unload_dictionary(self):
        path = self._values["persistent-dictionary"]

        free_persistent_dictionary(path)
        ok = not is_persistent_dictionary(path)

        self.assertTrue(ok, "Dictionary freeing failed!")

    def test_03_load_fst2(self):
        path = self._values["fst2"]

        output = load_persistent_fst2(path)
        self._values["persistent-fst2"] = output

        ok = is_persistent_fst2(output)

        self.assertTrue(ok, "Fst2 loading failed!")

    def test_04_unload_fst2(self):
        path = self._values["persistent-fst2"]

        free_persistent_fst2(path)
        ok = not is_persistent_fst2(path)

        self.assertTrue(ok, "Fst2 freeing failed!")

    def test_05_load_alphabet(self):
        path = self._values["alphabet"]

        output = load_persistent_alphabet(path)
        self._values["persistent-alphabet"] = output

        ok = is_persistent_alphabet(output)

        self.assertTrue(ok, "Alphabet loading failed!")

    def test_06_unload_alphabet(self):
        path = self._values["persistent-alphabet"]

        free_persistent_alphabet(path)
        ok = not is_persistent_alphabet(path)

        self.assertTrue(ok, "Alphabet freeing failed!")



if __name__ == '__main__':
    unittest.main()
