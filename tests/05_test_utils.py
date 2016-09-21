#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from unitex.utils.fsa import Automaton



class Arguments:

    def __init__(self, language=None):
        self.__arguments = {}

        self.__arguments["raw"] = "data/grf-raw.dot"
        self.__arguments["determinized"] = "data/grf-determinized.dot"
        self.__arguments["minimized"] = "data/grf-minimized.dot"

        self.__arguments["automaton"] = None

    def __getitem__(self, key):
        if key not in self.__arguments:
            raise KeyError("Argument '%s' not found ..." % key)
        return self.__arguments[key]

    def __setitem__(self, key, value):
        self.__arguments[key] = value



class TestUnitexUtils(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._arguments = Arguments()

    @classmethod
    def tearDownClass(self):
        if os.path.exists(self._arguments["raw"]):
            os.remove(self._arguments["raw"])

        if os.path.exists(self._arguments["determinized"]):
            os.remove(self._arguments["determinized"])

        if os.path.exists(self._arguments["minimized"]):
            os.remove(self._arguments["minimized"])

    def test_01_automaton_build(self):
        self._arguments["automaton"] = Automaton("MWU Test")

        path1 = "président français de la république"
        path2 = "président de la république"
        path3 = "ministre islandais de la défense"
        path4 = "ministre islandais à la défense"
        path5 = "secrétaire d'état à la défense"
        path6 = "secrétaire d'état"
        path7 = "secrétaire"
        path8 = "adjoint au secrétaire d'état"
        path9 = "adjoint au secrétaire d'état à la défense"

        self._arguments["automaton"].add_path(path1.split())
        self._arguments["automaton"].add_path(path2.split())
        self._arguments["automaton"].add_path(path3.split())
        self._arguments["automaton"].add_path(path4.split())
        self._arguments["automaton"].add_path(path5.split())
        self._arguments["automaton"].add_path(path6.split())
        self._arguments["automaton"].add_path(path7.split())
        self._arguments["automaton"].add_path(path8.split())
        self._arguments["automaton"].add_path(path9.split())

        self._arguments["automaton"].todot(self._arguments["raw"])
        self.assertTrue(os.path.exists(self._arguments["raw"]), "Automaton building failed!")

    def test_02_automaton_determinize(self):
        self._arguments["automaton"].determinize()
        self._arguments["automaton"].todot(self._arguments["determinized"])

        self.assertTrue(os.path.exists(self._arguments["determinized"]), "Automaton determinization failed!")


    def test_03_automaton_minimize(self):
        self._arguments["automaton"].minimize()
        self._arguments["automaton"].todot(self._arguments["minimized"])

        self.assertTrue(os.path.exists(self._arguments["minimized"]), "Automaton minimization failed!")

if __name__ == '__main__':
    unittest.main()
