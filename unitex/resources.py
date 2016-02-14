#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _unitex import *
from unitex import UnitexException, LOGGER



def load_persistent_dictionary(path):
    """This function loads a dictionary in persistent space.

    Argument:
        path [str] -- the exisent file path in filespace (hard disk or virtual file system)

    Return [str]:
        The persistent file path [str] (derived from filename but not strictly identical,
        depending of implementation). This path must be used by the unitex tools and the
        'free_persistent_dictionary' function.
    """
    LOGGER.info("Load persistent dictionary '%s'..." % path)
    ret = unitex_load_persistent_dictionary(path)
    if ret == 0:
        LOGGER.debug("Loading dictionary '%s' failed..." % path)
        raise UnitexException("Unable to load persistent dictionary '%s'..." % path)

    return ret

def is_persistent_dictionary(path):
    """This function checks if a dictionary path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the dictionary is persitent otherwise False
    """
    ret = unitex_is_persistent_dictionary(path)
    if ret == 0:
        return False
    return True

def free_persistent_dictionary(path):
    """This function unloads a dictionary from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_dictionary'
                      function
    """
    unitex_free_persistent_dictionary(path)



def load_persistent_fst2(path):
    """This function loads a fst2 in persistent space.

    Argument:
        path [str] -- the exisent file path in filespace (hard disk or virtual file system)

    Return [str]:
        The persistent file path [str] (derived from filename but not strictly identical,
        depending of implementation). This path must be used by the unitex tools and the
        'free_persistent_fst2' function.
    """
    LOGGER.info("Load persistent fst2 '%s'..." % path)
    ret = unitex_load_persistent_fst2(path)
    if ret == 0:
        LOGGER.debug("Loading fst2 '%s' failed..." % path)
        raise UnitexException("Unable to load persistent fst2 '%s'..." % path)

    return ret

def is_persistent_fst2(path):
    """This function checks if a fst2 path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the fst2 is persitent otherwise False
    """
    ret = unitex_is_persistent_fst2(path)
    if ret == 0:
        return False
    return True

def free_persistent_fst2(path):
    """This function unloads a fst2 from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_fst2'
                      function
    """
    unitex_free_persistent_fst2(path)



def load_persistent_alphabet(path):
    """This function loads a alphabet in persistent space.

    Argument:
        path [str] -- the exisent file path in filespace (hard disk or virtual file system)

    Return [str]:
        The persistent file path [str] (derived from filename but not strictly identical,
        depending of implementation). This path must be used by the unitex tools and the
        'free_persistent_alphabet' function.
    """
    LOGGER.info("Load persistent alphabet '%s'..." % path)
    ret = unitex_load_persistent_alphabet(path)
    if ret == 0:
        LOGGER.debug("Loading alphabet '%s' failed..." % path)
        raise UnitexException("Unable to load persistent alphabet '%s'..." % path)

    return ret

def is_persistent_alphabet(path):
    """This function checks if a alphabet path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the alphabet is persitent otherwise False
    """
    ret = unitex_is_persistent_alphabet(path)
    if ret == 0:
        return False
    return True

def free_persistent_alphabet(path):
    """This function unloads a alphabet from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_alphabet'
                      function
    """
    unitex_free_persistent_alphabet(path)
