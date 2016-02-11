#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

from unitex import UnitexException, LOGGER, LIBUNITEX



def enable_stdout():
    """This function enable Unitex standard output. This should be used
    for debug purposes only.
    """
    pass

def disable_stdout():
    """This function disable Unitex standard output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.
    """
    pass



class UnitexFile(object):

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
