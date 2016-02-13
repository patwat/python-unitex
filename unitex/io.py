#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

from _unitex import unitex_get_vfs_file_list
from unitex import UnitexException, LOGGER, LIBUNITEX



def enable_stdout():
    """This function enable Unitex standard output. This should be used
    for debug purposes only.
    """
    swk = 0
    trashOutput = ctypes.c_int(0)
    fnc_stdOutWrite = None
    privatePtr = None

    ret = LIBUNITEX.SetStdWriteCB(swk, trashOutput, fnc_stdOutWrite, privatePtr)
    if ret == 0:
        raise UnitexException("Enabling stdout failed!")

def disable_stdout():
    """This function disable Unitex standard output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.
    """
    swk = 0
    trashOutput = ctypes.c_int(1)
    fnc_stdOutWrite = None
    privatePtr = None

    ret = LIBUNITEX.SetStdWriteCB(swk, trashOutput, fnc_stdOutWrite, privatePtr)
    if ret == 0:
        raise UnitexException("Disabling stdout failed!")

def enable_stderr():
    """This function enable Unitex error output. This should be used
    for debug purposes only.
    """
    swk = 1
    trashOutput = ctypes.c_int(0)
    fnc_stdOutWrite = None
    privatePtr = None

    ret = LIBUNITEX.SetStdWriteCB(swk, trashOutput, fnc_stdOutWrite, privatePtr)
    if ret == 0:
        raise UnitexException("Enabling stderr failed!")

def disable_stderr():
    """This function disable Unitex error output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.
    """
    swk = 1
    trashOutput = ctypes.c_int(1)
    fnc_stdOutWrite = None
    privatePtr = None

    ret = LIBUNITEX.SetStdWriteCB(swk, trashOutput, fnc_stdOutWrite, privatePtr)
    if ret == 0:
        raise UnitexException("Disabling stderr failed!")



class UnitexIOConstants:

    VFS_PREFIX = "$:"



def cp(source_path, target_path):
    _source_path = ctypes.c_char_p(bytes(str(source_path), "utf-8"))
    _target_path = ctypes.c_char_p(bytes(str(target_path), "utf-8"))

    ret = LIBUNITEX.CopyUnitexFile(_source_path, _target_path)
    if ret != 0:
        raise UnitexException("File copy failed!")

def rm(path):
    _path = ctypes.c_char_p(bytes(str(path), "utf-8"))

    ret = LIBUNITEX.RemoveUnitexFile(_path)
    if ret != 0:
        raise UnitexException("File suppression failed!")

def mv(old_path, new_path):
    _old_path = ctypes.c_char_p(bytes(str(old_path), "utf-8"))
    _new_path = ctypes.c_char_p(bytes(str(new_path), "utf-8"))

    ret = LIBUNITEX.RenameUnitexFile(_old_path, _new_path)
    if ret != 0:
        raise UnitexException("File renaming failed!")

def ls(path):
    return unitex_get_vfs_file_list(path)

def mkdir(path):
    _path = ctypes.c_char_p(bytes(str(path), "utf-8"))

    ret = LIBUNITEX.CreateUnitexFolder(_path)
    if ret != 0:
        raise UnitexException("Folder creation failed!")

def rmdir(path):
    _path = ctypes.c_char_p(bytes(str(path), "utf-8"))

    ret = LIBUNITEX.RemoveUnitexFolder(_path)
    if ret != 0:
        raise UnitexException("Folder suppression failed!")



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
