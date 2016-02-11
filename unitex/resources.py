#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

from unitex import UnitexException, LOGGER, LIBUNITEX



def load_persistent_dictionary(path):
    """This function loads a dictionary in persistent space.

    Argument:
        path [str] -- the exisent file path in filespace (hard disk or virtual file system)

    Return [str]:
        The persistent file path [str] (derived from filename but not strictly identical,
        depending of implementation). This path must be used by the unitex tools and the
        'free_persistent_dictionary' function.
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    size = len(path) + 0x200
    persistent_filename_buffer = ctypes.create_string_buffer(size)
    buffer_size = ctypes.c_int(size+1)

    LOGGER.info("Load persistent dictionary '%s'..." % path)
    ret = LIBUNITEX.persistence_public_load_dictionary(filename, persistent_filename_buffer, buffer_size)
    if ret == 0:
        LOGGER.debug("Loading dictionary '%s' failed..." % path)
        raise UnitexException("Unable to load persistent dictionary '%s'..." % path)

    output = persistent_filename_buffer.value
    output = output.decode("utf-8")

    return output

def is_persistent_dictionary(path):
    """This function checks if a dictionary path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the dictionary is persitent otherwise False
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    ret = LIBUNITEX.persistence_public_is_persisted_dictionary_filename(filename)
    if ret == 0:
        return False
    return True

def free_persistent_dictionary(path):
    """This function unloads a dictionary from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_dictionary'
                      function
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    LIBUNITEX.persistence_public_unload_dictionary(filename)



def load_persistent_fst2(path):
    """This function loads a fst2 in persistent space.

    Argument:
        path [str] -- the exisent file path in filespace (hard disk or virtual file system)

    Return [str]:
        The persistent file path [str] (derived from filename but not strictly identical,
        depending of implementation). This path must be used by the unitex tools and the
        'free_persistent_fst2' function.
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    size = len(path) + 0x200
    persistent_filename_buffer = ctypes.create_string_buffer(size)
    buffer_size = ctypes.c_int(size+1)

    LOGGER.info("Load persistent fst2 '%s'..." % path)
    ret = LIBUNITEX.persistence_public_load_fst2(filename, persistent_filename_buffer, buffer_size)
    if ret == 0:
        LOGGER.debug("Loading fst2 '%s' failed..." % path)
        raise UnitexException("Unable to load persistent fst2 '%s'..." % path)

    output = persistent_filename_buffer.value
    output = output.decode("utf-8")

    return output

def is_persistent_fst2(path):
    """This function checks if a fst2 path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the fst2 is persitent otherwise False
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    ret = LIBUNITEX.persistence_public_is_persisted_fst2_filename(filename)
    if ret == 0:
        return False
    return True

def free_persistent_fst2(path):
    """This function unloads a fst2 from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_fst2'
                      function
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    LIBUNITEX.persistence_public_unload_fst2(filename)



def load_persistent_alphabet(path):
    """This function loads a alphabet in persistent space.

    Argument:
        path [str] -- the exisent file path in filespace (hard disk or virtual file system)

    Return [str]:
        The persistent file path [str] (derived from filename but not strictly identical,
        depending of implementation). This path must be used by the unitex tools and the
        'free_persistent_alphabet' function.
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    size = len(path) + 0x200
    persistent_filename_buffer = ctypes.create_string_buffer(size)
    buffer_size = ctypes.c_int(size+1)

    LOGGER.info("Load persistent alphabet '%s'..." % path)
    ret = LIBUNITEX.persistence_public_load_alphabet(filename, persistent_filename_buffer, buffer_size)
    if ret == 0:
        LOGGER.debug("Loading alphabet '%s' failed..." % path)
        raise UnitexException("Unable to load persistent alphabet '%s'..." % path)

    output = persistent_filename_buffer.value
    output = output.decode("utf-8")

    return output

def is_persistent_alphabet(path):
    """This function checks if a alphabet path points to the persistent space.

    Argument:
        path [str] -- the file path to check

    Return [bool]:
        True if the alphabet is persitent otherwise False
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    ret = LIBUNITEX.persistence_public_is_persisted_alphabet_filename(filename)
    if ret == 0:
        return False
    return True

def free_persistent_alphabet(path):
    """This function unloads a alphabet from persistent space.

    Argument:
        path [str] -- the persistent file path returned by the 'load_persistent_alphabet'
                      function
    """
    filename = ctypes.c_char_p(bytes(str(path), "utf-8"))

    LIBUNITEX.persistence_public_unload_alphabet(filename)
