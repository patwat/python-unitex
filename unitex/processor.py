#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unitex import *
from unitex.resources import *
from unitex.tools import *



class UnitexProcessor(object):

    def __init__(self, config=None):
        self.__config = None

        self.__persisted_objects = None
        self.__working_directory = None

        if config is not None:
            self.reset(config)

    def reset(self, config):
        self.__config = UnitexConfig()
        self.__config.load(config)

        for handler in LOGGER.handlers:
            if self.__config["debug"] == 1:
                fh.setLevel(logging.DEBUG)
            elif self.__config["verbose"] == 1:
                fh.setLevel(logging.WARNING)
            elif self.__config["verbose"] == 2:
                fh.setLevel(logging.INFO)
            else:
                fh.setLevel(logging.ERROR)

        self.load()

    def load(self):
        if self.__config["persistence"] is False:
            return

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
        rmdir

    def open(self, path, mode="srtlf", encoding=None, tagged=False, virtualize=False):
        if encoding is None:
            encoding = DEFAULT_ENCODING

    def close(self, clean=True, free=False):
        raise NotImplementedError

    def tag(self, *args, **kwargs):
        raise NotImplementedError

    def search(self, *args, **kwargs):
        raise NotImplementedError

    def extract(self, *args, **kwargs):
        raise NotImplementedError
