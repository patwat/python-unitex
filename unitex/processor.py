#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

from unitex import UnitexException, LOGGER, LIBUNITEX



class UnitexSettings:

    def __init__(self):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError



class UnitexProcessor:

    def __init__(self):
        raise NotImplementedError

    def open(self, path, mode=None, encoding=None):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

