#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _unitex import *
from unitex import UnitexException, LOGGER



def enable_stdout():
    """This function enables Unitex standard output. This is the default but
    should be used for debug purposes only.

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Enabling standard output...")
    ret = unitex_enable_stdout()
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def disable_stdout():
    """This function disables Unitex standard output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Disabling standard output...")
    ret = unitex_disable_stdout()
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def enable_stderr():
    """This function enables Unitex error output. This is the default but
    should be used for debug purposes only.

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Enabling error output...")
    ret = unitex_enable_stderr()
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def disable_stderr():
    """This function disables Unitex error output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Disabling error output...")
    ret = unitex_disable_stderr()
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret



def cp(source_path, target_path):
    """This function copies a file. Both pathes can be on the virtual filesystem
    or the disk filesystem. Therefor, this function can be used to virtualize a
    file or to dump a virtual file.

    Arguments:
        source_path [str] -- source file path
        target_path [str] -- target file path

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Copying file '%s' to '%s'..." % (source_path, target_path))
    ret = unitex_cp(source_path, target_path)
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def rm(path):
    """This function removes a file. The path can be on the virtual filesystem
    or the disk filesystem.

    Argument:
        path [str] -- file path

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Removing file '%s'..." % path)
    ret = unitex_rm(path)
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def mv(old_path, new_path):
    """This function moves/renames a file. Both pathes can be on the virtual
    filesystem or the disk filesystem.

    Arguments:
        old_path [str] -- old file path
        new_path [str] -- new file path

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Moving file '%s' to '%s'..." % (old_path, new_path))
    ret = unitex_mv(old_path, new_path)
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def mkdir(path):
    """This function creates a directory on the disk.

    Argument:
        path [str] -- directory path

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Creating directory '%s'..." % path)
    ret = unitex_mkdir(path)
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def rmdir(path):
    """This function removes a directory on the disk.

    Argument:
        path [str] -- directory path

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    LOGGER.info("Removing directory '%s'..." % path)
    ret = unitex_rmdir(path)
    if ret is False:
        LOGGER.info("[FAILED!]")

    return ret

def ls(path):
    """This function lists (disk or virtual) directory contents.

    Argument:
        path [str] -- directory path

    Return [list(str)]:
        The function returns a list of files (not directories) if the directory
        is not empty and an empty list otherwise.
    """
    LOGGER.info("Listing directory '%s'..." % path)
    return unitex_ls(path)



class UnitexFile(object):
    """The UnitexFile class provides the minimum functionality necessary to
    manipulate files on the disk and the virtual filesystems. It's mainly
    useful to read files from virtual filesystem whithout having to copy them
    to the disk.
    
    **WARNING: the encoding must be UTF-8 and the data Unicode strings.**
    """

    def __init__(self):
        self.__use_bom = None

        self.__file = None
        self.__mode = None

    def open(self, file, mode=None, use_bom=False):
        if self.__file is not None:
            raise UnitexException("You must close the current file (%s) before open another one..." % self.__file)
        self.__use_bom = use_bom

        self.__file = file
        self.__mode = mode

    def close(self):
        if self.__file is None:
            raise UnitexException("There is no file to close...")
        self.__file = None
        self.__mode = None

    def write(self, data):
        if self.__mode not in ("w", "a"):
            raise UnitexException("File '%s' is opened in read mode..." % self.__file)
        if self.__file is None: 
            raise UnitexException("You must open a file before writing...")

        if self.__mode == "w":
            bom = 1 if self.__use_bom is True else 0
            unitex_write_file(self.__file, data, bom)
        else:
            unitex_append_to_file(self.__file, data)

    def read(self):
        if self.__mode != "r":
            raise UnitexException("File '%s' is opened in write/append mode..." % self.__file)
        return unitex_read_file(self.__file)
