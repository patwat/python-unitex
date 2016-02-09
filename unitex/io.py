#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

from unitex import UnitexException, LOGGER, LIBUNITEX



class UnitexFile:

    def __init__(self):
        raise NotImplementedError

    def open(self, path, mode=None, encoding=None):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def seek(self, offset):
        raise NotImplementedError

    def tell(self):
        raise NotImplementedError

    def write(self, data):
        raise NotImplementedError

    def writelines(self, lines):
        raise NotImplementedError

    def read(self, size=None):
        raise NotImplementedError

    def readline(self):
        raise NotImplementedError

    def readlines(self):
        raise NotImplementedError
