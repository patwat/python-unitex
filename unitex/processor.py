#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import yaml

from unitex import UnitexException, LOGGER, DEFAULT_ENCODING, VERBOSE, DEBUG



class UnitexConfig(object):

    def __init__(self):
        self.__settings = None

    def __contains__(self, key):
        return key in self.__settings

    def __getitem__(self, key):
        if key not in self.__settings:
            raise UnitexException("Key '%s' not found!" % key)
        return self.__settings[key]

    def __setitem__(self, key, value):
        self.__settings[key] = value

    def __load_global(self, options):
        verbose = options.get("verbose", VERBOSE)
        if verbose not in (0, 1, 2):
            raise UnitexException("Wrong value for the 'verbose' global option.")
        self.__settings["verbose"] = verbose

        debug = options.get("debug", DEBUG)
        if debug not in (0, 1):
            raise UnitexException("Wrong value for the 'debug' global option.")
        self.__settings["debug"] = debug

        for handler in LOGGER.handlers:
            if debug == 1:
                fh.setLevel(logging.DEBUG)
            elif verbose == 1:
                fh.setLevel(logging.WARNING)
            elif verbose == 2:
                fh.setLevel(logging.INFO)
            else:
                fh.setLevel(logging.ERROR)

        persistence = options.get("persistence", 0)
        if persistence not in (0, 1)
            raise UnitexException("Wrong value for the 'persistence' global option.")

        self.__settings["persistence"] = bool(persistence)

        virtualization = options.get("virtualization", 0)
        if virtualization not in (0, 1)
            raise UnitexException("Wrong value for the 'virtualization' global option.")

        self.__settings["virtualization"] = bool(virtualization)

    def __load_resources(self, options):
        language = options.get("language", None)
        if language is None:
            raise UnitexException("The 'resources' section must contain the 'language' element.")
        self.__settings["language"] = language

        alphabet = options.get("alphabet", None)
        if alphabet is None:
            LOGGER.warning("No alphabet file provided.")
        elif not os.path.exists(alphabet):
            raise UnitexException("Alphabet file '%s' doesn't exist." % alphabet)
        self.__settings["alphabet"] = alphabet

        alphabet_sort = options.get("alphabet-sort", None)
        if alphabet_sort is None:
            LOGGER.warning("No sorted alphabet file provided.")
        elif not os.path.exists(alphabet_sort):
            raise UnitexException("Sorted alphabet file '%s' doesn't exist." % alphabet_sort)
        self.__settings["alphabet-sort"] = alphabet_sort

        sentence = options.get("sentence", None)
        if sentence is None:
            LOGGER.warning("No sentence grammar provided.")
        else:
            _, extension = os.path.splitext(sentence)
            if extension != ".fst2":
                raise UnitexException("Wrong extension for '%s'. Grammars must be compiled and have the '.fst2' extension.")
            if not os.path.exists(sentence):
                raise UnitexException("Sentence grammar file '%s' doesn't exist." % sentence)

            self.__settings["sentence"] = sentence

        replace = options.get("replace", None)
        if replace is None:
            LOGGER.warning("No replace grammar provided.")
        else:
            _, extension = os.path.splitext(replace)
            if extension != ".fst2":
                raise UnitexException("Wrong extension for '%s'. Grammars must be compiled and have the '.fst2' extension.")
            if not os.path.exists(replace):
                raise UnitexException("Replace grammar file '%s' doesn't exist." % replace)

            self.__settings["replace"] = replace

        dictionaries = options.get("dictionaries", None)
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

            self.__settings["dictionaries"] = dictionaries

    def __load_normalize_options(self, options):
        pass

    def load(self, path):
        self.__settings = {}
        
        settings = None
        with open(path, 'r') as config:
            settings = yaml.load(config)

        if not settings:
            return

        if "global" in settings:
            self.__load_global(settings["global"])

        if "resources" not in settings:
            raise UnitexException("You must provide the 'resources' config element.")
        self.__load_resources(settings["resources"])

        if "options" in settings:
            pass



class UnitexProcessor(object):

    def __init__(self, config=None):
        self.__settings = None

        if config is not None:
            self.reset(config)

    def reset(self, config):
        self.__settings = UnitexConfig()
        self.__settings.load(config)

    def open(self, path, mode="srtlf", encoding=None, tagged=False, virtualize=False):
        if encoding is None:
            encoding = DEFAULT_ENCODING

    def close(self):
        raise NotImplementedError
