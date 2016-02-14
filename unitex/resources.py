#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _unitex import *
from unitex import LOGGER



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
    return unitex_load_persistent_dictionary(path)

def is_persistent_dictionary(path):
    """This function checks if a dictionary path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the dictionary is persitent otherwise False
    """
    return unitex_is_persistent_dictionary(path)

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
    return unitex_load_persistent_fst2(path)

def is_persistent_fst2(path):
    """This function checks if a fst2 path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the fst2 is persitent otherwise False
    """
    return unitex_is_persistent_fst2(path)

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
    return unitex_load_persistent_alphabet(path)

def is_persistent_alphabet(path):
    """This function checks if a alphabet path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the alphabet is persitent otherwise False
    """
    return unitex_is_persistent_alphabet(path)

def free_persistent_alphabet(path):
    """This function unloads a alphabet from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_alphabet'
                      function
    """
    unitex_free_persistent_alphabet(path)
