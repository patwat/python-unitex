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
        else:



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

