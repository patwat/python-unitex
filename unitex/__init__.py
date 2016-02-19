#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["io", "tools", "processor"]

import logging
import os
import sys



class UnitexException(Exception):

    def __init__(self, message):
        message = "## UNITEX EXCEPTION ## %s" % message
        super(UnitexException, self).__init__(message)



class UnitexConstants(object):

    VFS_PREFIX = "$:"

    GRAMMAR = "grammar"
    DICTIONARY = "dictionary"
    ALPHABET = "alphabet"

    DELAF = "delaf"
    DELAS = "delas"

    DICTIONARY_VERSION_1 = "v1"
    DICTIONARY_VERSION_2 = "v2"

    SORT_TEXT_ORDER = "TO"
    SORT_LEFT_CENTER = "LC"
    SORT_LEFT_RIGHT = "LR"
    SORT_CENTER_LEFT = "CL"
    SORT_CENTER_RIGHT = "CR"
    SORT_RIGHT_LEFT = "RL"
    SORT_RIGHT_CENTER = "RC"

    FORMAT_HTML = "html"
    FORMAT_TEXT = "text"
    FORMAT_GLOSSANET = "glossanet"
    FORMAT_SCRIPT = "script"
    FORMAT_INDEX = "index"
    FORMAT_UIMA = "uima"
    FORMAT_PRLG = "prlg"
    FORMAT_XML = "xml"
    FORMAT_XML_WITH_HEADERS = "xml-with-headers"
    FORMAT_AXIS = "axis"
    FORMAT_XALIGN = "xalign"
    FORMAT_MERGE = "merge"

    NEGATION_OPERATOR = "tilde"
    NEGATION_OPERATOR_OLD = "minus"

    MATCH_MODE_LONGEST = "longest"
    MATCH_MODE_SHORTEST = "shortest"
    MATCH_MODE_ALL = "all"

    OUTPUT_MODE_MERGE = "merge"
    OUTPUT_MODE_IGNORE = "ignore"
    OUTPUT_MODE_RELACE = "replace"

    ON_ERROR_EXIT = "exit"
    ON_ERROR_IGNORE = "ignore"
    ON_ERROR_BACKTRACK = "backtrack"



DEFAULT_ENCODING="utf-8"

# VERBOSE = 0: ERROR logging level
# VERBOSE = 1: WARNING logging level
# VERBOSE = 2: INFO logging level
VERBOSE = os.path.expandvars('$UNITEX_VERBOSE')
if VERBOSE == '$UNITEX_VERBOSE':
    VERBOSE = 0
else:
    VERBOSE = int(VERBOSE)
    if VERBOSE not in (0, 1, 2):
        raise UnitexException( "Wrong $UNITEX_VERBOSE value..." )

# DEBUG = 0: --
# DEBUG = 1: DEBUG logging level
#  -> if set to 1, it overrides the VERBOSE variable
DEBUG = os.path.expandvars('$UNITEX_DEBUG')
if DEBUG == '$UNITEX_DEBUG':
    DEBUG = 0
else:
    DEBUG = int(DEBUG)
    if DEBUG not in (0, 1):
        raise UnitexException( "Wrong $UNITEX_DEBUG value..." )

# If a log file is specified, the log will be duplicated
# to this file
LOG = os.path.expandvars('$UNITEX_LOG')
if LOG != '$UNITEX_LOG':
    os.path.expandvars('$UNITEX_LOG')
else:
    LOG = None

LOGGER = logging.getLogger("unitex")

ch = logging.StreamHandler()

if DEBUG == 1:
    ch.setLevel(logging.DEBUG)
elif VERBOSE == 1:
    ch.setLevel(logging.WARNING)
elif VERBOSE == 2:
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.ERROR)

cf = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
ch.setFormatter(cf)

LOGGER.addHandler(ch)

if LOG is not None:
    fh = logging.FileHandler(LOG)

    if DEBUG == 1:
        fh.setLevel(logging.DEBUG)
    elif VERBOSE == 1:
        fh.setLevel(logging.WARNING)
    elif VERBOSE == 2:
        fh.setLevel(logging.INFO)
    else:
        fh.setLevel(logging.ERROR)

    ff = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(ff)

    LOGGER.addHandler(fh)
