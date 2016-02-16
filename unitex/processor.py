#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml

from unitex import UnitexException, LOGGER, DEFAULT_ENCODING



class UnitexSettings(object):

    def __init__(self):
        self.__settings = None

    def __contains__(self, key):
        return key in self.__settings

    def __getitem__(self, key):
        if key not in self.__settings:
            raise UnitexException("Key '%s' not found!" % key)
        return self.__settings[key]

    def set(self, key, value):
        self.__settings[key] = value

    def load(self, f):
        with open(f, 'r') as config:
            self.__settings = yaml.load(config)
        self.check()

    def check(self):
        resources = self.__settings.get("resources", None)
        if resources is None:
            raise UnitexException("You must provide the 'resources' config element.")

        language = resources.get("language", None)
        if language is None:
            raise UnitexException("The 'resources' section must contain the 'language' element.")

        alphabet = resources.get("alphabet", None)
        if alphabet is None:
            LOGGER.warning("No alphabet file provided.")
        elif not os.path.exists(alphabet):
            raise UnitexException("Alphabet file '%s' doesn't exist." % alphabet)

        alphabet_sort = resources.get("alphabet-sort", None)
        if alphabet_sort is None:
            LOGGER.warning("No sorted alphabet file provided.")
        elif not os.path.exists(alphabet_sort):
            raise UnitexException("Sorted alphabet file '%s' doesn't exist." % alphabet_sort)

        sentence = resources.get("sentence", None)
        if sentence is None:
            LOGGER.warning("No sentence grammar provided.")
        else:
            _, extension = os.path.splitext(sentence)
            if extension != ".fst2":
                raise UnitexException("Wrong extension for '%s'. Grammars must be compiled and have the '.fst2' extension.")
            if not os.path.exists(sentence):
                raise UnitexException("Sentence grammar file '%s' doesn't exist." % sentence)

        replace = resources.get("replace", None)
        if replace is None:
            LOGGER.warning("No replace grammar provided.")
        else:
            _, extension = os.path.splitext(replace)
            if extension != ".fst2":
                raise UnitexException("Wrong extension for '%s'. Grammars must be compiled and have the '.fst2' extension.")
            if not os.path.exists(replace):
                raise UnitexException("Replace grammar file '%s' doesn't exist." % replace)

        dictionaries = resources.get("dictionaries", None)
        if dictionaries is None:
            LOGGER.warning("No dictionaries provided.")
        else:
            if not isinstance(dictionaries, list):
                raise UnitexException("The 'dictionaries' element must be a list of .bin files.")
            for dictionary in dictionaries:
                prefix, extension = os.path.splitext(dictionary)
                if extension != ".bin":
                    raise UnitexException("Wrong extension for '%s'. Dictionaries must be compiled and have the '.bin' extension.")
                if not os.path.exists(dictionary):
                    raise UnitexException("Dictionary file '%s' doesn't exist." % dictionary)
                if not os.path.exists("%s.bin" % prefix):
                    raise UnitexException("Dictionary .inf file missing for '%s'." % dictionary)



class UnitexProcessor(object):

    def __init__(self, config=None):
        self.__settings = None

        if config is not None:
            self.reset(config)

    def reset(self, config):
        self.__settings = UnitexSettings()
        self.__settings.load(config)

    def open(self, path, mode="srtlf", encoding=None, tagged=False, virtualize=False):
        if encoding is None:
            encoding = DEFAULT_ENCODING

    def close(self):
        raise NotImplementedError
