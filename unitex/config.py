#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

from unitex import UnitexException, LOGGER



class UnitexSettings:

    def __init__(self):
        self.__settings = None

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def load(self, f):
        with open(f, 'r') as ymlfile:
            self.__config = yaml.load(ymlfile)
        raise NotImplementedError

