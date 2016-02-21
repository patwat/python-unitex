#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import yaml

from unitex import *
from unitex.config import UnitexConfig
from unitex.io import *
from unitex.resources import *
from unitex.tools import *

_LOGGER = logging.getLogger(__name__)



class UnitexProcessor(object):

    def __init__(self, config):
        self.__options = None

        self.__persisted_objects = None
        self.__working_directory = None

        self.init(config)

    def init(self, config):
        options = None
        with open(config, "r") as f:
            options = yaml.load(f)

        self.__options = UnitexConfig()
        self.__options.load(options)

        verbose = self.__options["verbose"]
        debug = self.__options["debug"]
        log = self.__options["log"]

        init_log_system(verbose, debug, log)

        self.load()

    def load(self):
        if self.__options["persistence"] is False:
            return
        self.__persisted_objects = []

        if self.__options["resources"]["alphabet"] is not None:
            _type = UnitexConstants.ALPHABET
            _object = load_persistent_alphabet(self.__options["resources"]["alphabet"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["alphabet"] = _object

        if self.__options["resources"]["alphabet-sorted"] is not None:
            _type = UnitexConstants.ALPHABET
            _object = load_persistent_alphabet(self.__options["resources"]["alphabet-sorted"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["alphabet-sorted"] = _object

        if self.__options["resources"]["sentence"] is not None:
            _type = UnitexConstants.GRAMMAR
            _object = load_persistent_fst2(self.__options["resources"]["sentence"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["sentence"] = _object

        if self.__options["resources"]["replace"] is not None:
            _type = UnitexConstants.GRAMMAR
            _object = load_persistent_fst2(self.__options["resources"]["replace"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["replace"] = _object

        if self.__options["resources"]["dictionaries"] is not None:
            _objects = []

            _type = UnitexConstants.DICTIONARY
            for dictionary in self.__options["resources"]["dictionaries"]:
                _object = load_persistent_dictionary(dictionary)

                self.__persisted_objects.append((_type, _object))
                _objects.append(_object)

            self.__options["resources"]["dictionaries"] = _objects

    def free(self):
        if self.__persisted_objects is None:
            return

        for _type, _object in self.__persisted_objects:
            if _type == UnitexConstants.GRAMMAR:
                free_persistent_fst2(_object)
            elif _type == UnitexConstants.DICTIONARY:
                free_persistent_dictionary(_object)
            elif _type == UnitexConstants.ALPHABET:
                free_persistent_alphabet(_object)

    def clean(self):
        if self.__working_directory is None:
            return
        rmdir(self.__working_directory)

    def open(self, path, mode="srtlf", tagged=False):
        pass

    def close(self, clean=True, free=False):
        if clean is True:
            self.clean()

        if free is True:
            self.free()

    def tag(self, grammar, output, **kwargs):
        raise NotImplementedError

    def search(self, grammar, output, **kwargs):
        raise NotImplementedError

    def extract(self, grammar, output, **kwargs):
        raise NotImplementedError
