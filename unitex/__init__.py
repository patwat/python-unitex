#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import os
import sys

import _unitex



class UnitexException(Exception):

    def __init__(self, message):
        message = "## UNITEX EXCEPTION ## %s" % message
        super(UnitexException, self).__init__(message)



class UnitexConstants(object):
    """
    This class lists all the constants used by the Unitex processor.
    """

    DEFAULT_ENCODING=sys.getfilesystemencoding()

    VFS_PREFIX = "$:"

    RESOURCE_GRAMMAR = "grammar"
    RESOURCE_DICTIONARY = "dictionary"
    RESOURCE_ALPHABET = "alphabet"

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
    OUTPUT_MODE_REPLACE = "replace"

    ON_ERROR_EXIT = "exit"
    ON_ERROR_IGNORE = "ignore"
    ON_ERROR_BACKTRACK = "backtrack"



# VERBOSE = 0: ERROR logging level
# VERBOSE = 1: WARNING logging level
# VERBOSE = 2: INFO logging level
# VERBOSE = 3: activate Unitex standard output
VERBOSE = os.path.expandvars('$UNITEX_VERBOSE')
if VERBOSE == '$UNITEX_VERBOSE':
    VERBOSE = 0
else:
    VERBOSE = int(VERBOSE)
    if VERBOSE not in (0, 1, 2, 3):
        raise UnitexException( "Wrong $UNITEX_VERBOSE value..." )

# DEBUG = 0: --
# DEBUG = 1: DEBUG logging level
# DEBUG = 2: activate Unitex error output
DEBUG = os.path.expandvars('$UNITEX_DEBUG')
if DEBUG == '$UNITEX_DEBUG':
    DEBUG = 0
else:
    DEBUG = int(DEBUG)
    if DEBUG not in (0, 1, 2):
        raise UnitexException( "Wrong $UNITEX_DEBUG value..." )

# If a log file is specified, the log will be redirected
# to this file
LOG = os.path.expandvars('$UNITEX_LOG')
if LOG != '$UNITEX_LOG':
    os.path.expandvars('$UNITEX_LOG')
else:
    LOG = None

_LOGGER = logging.getLogger(__name__)



def enable_stdout():
    """
    This function enables Unitex standard output. This is the default
    but should be used for debug purposes only.

    *No argument.*

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Enabling standard output...")
    ret = _unitex.unitex_enable_stdout()
    if ret is False:
        _LOGGER.error("Enabling standard output failed!")

    return ret

def disable_stdout():
    """
    This function disables Unitex standard output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.

    *No argument.*

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Disabling standard output...")
    ret = _unitex.unitex_disable_stdout()
    if ret is False:
        _LOGGER.error("Disabling standard output failed!")

    return ret

def enable_stderr():
    """
    This function enables Unitex error output. This is the default but
    should be used for debug purposes only.

    *No argument.*

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Enabling error output...")
    ret = _unitex.unitex_enable_stderr()
    if ret is False:
        _LOGGER.error("Enabling error output failed!")

    return ret

def disable_stderr():
    """
    This function disables Unitex error output to ensure multithread
    output consistency (i.e. avoid output mixing between threads) and to
    improve performances.

    *No argument.*

    *Return [bool]:*

      **True** if it succeeds, **False** otherwise.
    """
    _LOGGER.info("Disabling error output...")
    ret = _unitex.unitex_disable_stderr()
    if ret is False:
        _LOGGER.error("Disabling error output failed!")

    return ret



def init_log_system(verbose, debug, log=None):
    """
    This function enables/disables the logging system.

    *Arguments:*

    - **verbose [int]** -- enables/disables the standard output.
      Possible values are:

      - 0: the standard output is disabled;
      - 1: the standard output shows 'warnings' emitted by the bindings
        logging system;
      - 2: the standard output shows 'warnings' and various
        processing informations emitted by the bindings logging system;
      - 3: the full standard output is activated for both the bindings
        and the Unitex processor.

    - **debug [int]** --  enables/disables the error output. Possible
      values are: 

      - 0: the error output is disabled;
      - 1: the error output is limited to the logging system implemented
        in the bindings;
      - 2: the error output is activated for both the bindings and the
        Unitex processor.

    - **log [str]** -- if not None, the error and standard outputs are
      redirected to the file specified by this argument. Be sure to have
      write access to this file.

    *No return.*
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    kwargs = {}

    if debug >= 1:
        kwargs["level"] = logging.DEBUG
    elif verbose == 1:
        kwargs["level"] = logging.WARNING
    elif verbose >= 2:
        kwargs["level"] = logging.INFO
    else:
        kwargs["level"] = logging.ERROR

    if log:
        kwargs["format"] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        kwargs["filename"] = LOG
        kwargs["filemode"] = "a"
    else:
        kwargs["format"] = "%(name)-12s: %(levelname)-8s %(message)s"

    logging.basicConfig(**kwargs)

    if verbose == 3:
        enable_stdout()
    else:
        disable_stdout()

    if debug == 2:
        enable_stderr()
    else:
        disable_stderr()

init_log_system(VERBOSE, DEBUG, LOG)
