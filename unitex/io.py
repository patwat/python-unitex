#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _unitex import *
from unitex import UnitexException, LOGGER



def enable_stdout():
    """This function enable Unitex standard output. This should be used
    for debug purposes only.
    """
    ret = unitex_enable_stdout()
    if ret == 0:
        raise UnitexException("Enabling stdout failed!")

def disable_stdout():
    """This function disable Unitex standard output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.
    """
    ret = unitex_disable_stdout()
    if ret == 0:
        raise UnitexException("Disabling stdout failed!")

def enable_stderr():
    """This function enable Unitex error output. This should be used
    for debug purposes only.
    """
    ret = unitex_enable_stderr()
    if ret == 0:
        raise UnitexException("Enabling stderr failed!")

def disable_stderr():
    """This function disable Unitex error output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.
    """
    ret = unitex_disable_stderr()
    if ret == 0:
        raise UnitexException("Disabling stderr failed!")



class UnitexIOConstants:

    VFS_PREFIX = "$:"



def cp(source_path, target_path):
    ret = unitex_cp(source_path, target_path)
    if ret != 0:
        raise UnitexException("File copy failed!")

def rm(path):
    ret = unitex_rm(path)
    if ret != 0:
        raise UnitexException("File suppression failed!")

def mv(old_path, new_path):
    ret = unitex_mv(old_path, new_path)
    if ret != 0:
        raise UnitexException("File renaming failed!")

def mkdir(path):
    ret = unitex_mkdir(path)
    if ret != 0:
        raise UnitexException("Folder creation failed!")

def rmdir(path):
    ret = unitex_rmdir(path)
    if ret != 0:
        raise UnitexException("Folder suppression failed!")

def ls(path):
    return unitex_ls(path)



class VirtualFile(object):

    def __init__(self):
        self.__file = None
        self.__mode = None

    def open(self, file, mode=None):
        self.__file = file
        self.__mode = mode
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def write(self, data):
        if self.__mode not in ("w", "a"):
            raise UnitexException("File '%s' is opened in read mode..." % self.__file)
        raise NotImplementedError

    def read(self):
        raise NotImplementedError
