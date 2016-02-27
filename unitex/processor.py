#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import os
import re
import yaml

# Compatibility Python 2/3
from io import open

from xml.sax.saxutils import escape

from unitex import *
from unitex.config import UnitexConfig
from unitex.io import *
from unitex.resources import *
from unitex.tools import *

_LOGGER = logging.getLogger(__name__)



RULES = []
RULES.append((re.compile(r"&"), "&amp;"))

def escape(sequence):
    for pattern, substitute in RULES:
        sequence = pattern.sub(substitute, sequence)
    return sequence



class UnitexProcessor(object):
    """
    This class hides mots of the Unitex (pre-)processing in order to
    facilitate his usage.
    """

    def __init__(self, config):
        self.__options = None

        self.__persisted_objects = None

        self.__txt = None
        self.__snt = None
        self.__dir = None

        self.init(config)

    def init(self, config):
        options = None
        with open(config, "r") as f:
            options = yaml.load(f)

        self.__options = UnitexConfig()
        self.__options.load(options)

        verbose = self.__options["verbose"]
        debug = self.__options["debug"]
        log = self.__options["log"]

        init_log_system(verbose, debug, log)

        self._load()

    def _load(self):
        if self.__options["persistence"] is False:
            return
        self.__persisted_objects = []

        if self.__options["resources"]["alphabet"] is not None:
            _type = UnitexConstants.ALPHABET
            _object = load_persistent_alphabet(self.__options["resources"]["alphabet"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["alphabet"] = _object

        if self.__options["resources"]["alphabet-sorted"] is not None:
            _type = UnitexConstants.ALPHABET
            _object = load_persistent_alphabet(self.__options["resources"]["alphabet-sorted"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["alphabet-sorted"] = _object

        if self.__options["resources"]["sentence"] is not None:
            _type = UnitexConstants.GRAMMAR
            _object = load_persistent_fst2(self.__options["resources"]["sentence"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["sentence"] = _object

        if self.__options["resources"]["replace"] is not None:
            _type = UnitexConstants.GRAMMAR
            _object = load_persistent_fst2(self.__options["resources"]["replace"])

            self.__persisted_objects.append((_type, _object))
            self.__options["resources"]["replace"] = _object

        if self.__options["resources"]["dictionaries"] is not None:
            _objects = []

            _type = UnitexConstants.DICTIONARY
            for dictionary in self.__options["resources"]["dictionaries"]:
                _object = load_persistent_dictionary(dictionary)

                self.__persisted_objects.append((_type, _object))
                _objects.append(_object)

            self.__options["resources"]["dictionaries"] = _objects

    def _free(self):
        if self.__persisted_objects is None:
            return

        for _type, _object in self.__persisted_objects:
            if _type == UnitexConstants.GRAMMAR:
                free_persistent_fst2(_object)
            elif _type == UnitexConstants.DICTIONARY:
                free_persistent_dictionary(_object)
            elif _type == UnitexConstants.ALPHABET:
                free_persistent_alphabet(_object)

    def _clean(self):
        if self.__txt is None:
            _LOGGER.error("Unable to clean processor. No file opened!")
            return

        if self.__options["virtualization"] is True:
            if self.__dir is not None:
                for vf in ls("%s%s" % (UnitexConstants.VFS_PREFIX, self.__dir)):
                    rm(vf)
            rm(self.__snt)
            rm(self.__txt)
        else:
            rmdir(self.__dir)
            rm(self.__snt)

    def _normalize(self):
        kwargs = self.__options["tools"]["normalize"]

        ret = normalize(self.__txt, **kwargs)
        if ret is False:
            raise UnitexException("Text normalization failed!")

    def _segment(self):
        grammar = self.__options["resources"]["sentence"]
        if grammar is None:
            raise UnitexException("Unable to segment text. No sentence grammar provided.")

        alphabet = self.__options["resources"]["alphabet"]
        if alphabet is None:
            raise UnitexException("Unable to segment text. No alphabet file provided.")

        kwargs = {}
        kwargs["start_on_space"] = self.__options["tools"]["fst2txt"]["start_on_space"]
        kwargs["char_by_char"] = self.__options["tools"]["fst2txt"]["char_by_char"]
        kwargs["merge"] = True

        ret = fst2txt(grammar, self.__snt, alphabet, **kwargs)
        if ret is False:
            raise UnitexException("Text segmentation failed!")

    def _replace(self):
        grammar = self.__options["resources"]["replace"]
        if grammar is None:
            raise UnitexException("Unable to normalize text. No replace grammar provided.")

        alphabet = self.__options["resources"]["alphabet"]
        if alphabet is None:
            raise UnitexException("Unable to normalize text. No alphabet file provided.")

        kwargs = {}
        kwargs["start_on_space"] = self.__options["tools"]["fst2txt"]["start_on_space"]
        kwargs["char_by_char"] = self.__options["tools"]["fst2txt"]["char_by_char"]
        kwargs["merge"] = False

        ret = fst2txt(grammar, self.__snt, alphabet, **kwargs)
        if ret is False:
            raise UnitexException("Text normalization failed!")

    def _tokenize(self):
        alphabet = self.__options["resources"]["alphabet"]
        if alphabet is None:
            raise UnitexException("Unable to tokenize text. No alphabet file provided.")

        kwargs = self.__options["tools"]["tokenize"]

        ret = tokenize(self.__snt, alphabet, **kwargs)
        if ret is False:
            raise UnitexException("Text tokenization failed!")

    def _lexicalize(self):
        dictionaries = self.__options["resources"]["dictionaries"]
        if not dictionaries:
            raise UnitexException("Unable to lexicalize text. No dictionaries provided.")

        alphabet = self.__options["resources"]["alphabet"]
        if alphabet is None:
            raise UnitexException("Unable to tokenize text. No alphabet file provided.")

        kwargs = self.__options["tools"]["dico"]

        ret = dico(dictionaries, self.__snt, alphabet, **kwargs)
        if ret is False:
            raise UnitexException("Text lexicalization failed!")

    def _locate(self, grammar, match_mode, output_mode):
        alphabet = self.__options["resources"]["alphabet"]
        if alphabet is None:
            raise UnitexException("Unable to locate pattern. No alphabet file provided.")

        kwargs = {}
        kwargs["morpho"] = self.__options["tools"]["locate"]["morpho"]
        kwargs["start_on_space"] = self.__options["tools"]["locate"]["start_on_space"]
        kwargs["char_by_char"] = self.__options["tools"]["locate"]["char_by_char"]
        kwargs["korean"] = self.__options["tools"]["locate"]["korean"]
        kwargs["arabic_rules"] = self.__options["tools"]["locate"]["arabic_rules"]
        kwargs["negation_operator"] = self.__options["tools"]["locate"]["negation_operator"]
        kwargs["stop_token_count"] = self.__options["tools"]["locate"]["stop_token_count"]
        kwargs["protect_dic_chars"] = self.__options["tools"]["locate"]["protect_dic_chars"]
        kwargs["variable"] = self.__options["tools"]["locate"]["variable"]
        kwargs["variable_error"] = self.__options["tools"]["locate"]["variable_error"]

        kwargs["sntdir"] = None
        kwargs["number_of_matches"] = None
        kwargs["ambiguous_outputs"] = False

        if match_mode not in (UnitexConstants.MATCH_MODE_LONGEST,
                              UnitexConstants.MATCH_MODE_SHORTEST):
            raise UnitexException("Wrong value for the 'match_mode' option. UnitexConstants.MATCH_MODE_X required.")
        kwargs["match_mode"] = match_mode

        if output_mode not in (UnitexConstants.OUTPUT_MODE_IGNORE,
                               UnitexConstants.OUTPUT_MODE_MERGE,
                               UnitexConstants.OUTPUT_MODE_RELACE):
            raise UnitexException("Wrong value for the 'output_mode' option. UnitexConstants.OUTPUT_MODE_X required.")
        kwargs["output_mode"] = output_mode

        ret = locate(grammar, self.__snt, alphabet, **kwargs)
        if ret is False:
            raise UnitexException("Locate failed!")

        index = os.path.join(self.__dir, "concord.ind")
        if self.__options["virtualization"] is True:
            index = "%s%s" % (UnitexConstants.VFS_PREFIX, index)

        if exists(index) is False:
            raise UnitexException("Locate failed! No index produced.")
        return index

    def _concord(self, index, merge=False, output=None):
        alphabet = self.__options["resources"]["alphabet"]
        if alphabet is None:
            raise UnitexException("Unable to build concordance. No alphabet file provided.")

        kwargs = {}
        kwargs["font"] = None
        kwargs["fontsize"] = None
        kwargs["only_ambiguous"] = False
        kwargs["left"] = "0"
        kwargs["right"] = "0"
        kwargs["sort"] = UnitexConstants.SORT_TEXT_ORDER
        kwargs["script"] = None
        kwargs["offsets"] = None
        kwargs["unxmlize"] = None
        kwargs["directory"] = None
        kwargs["thai"] = self.__options["tools"]["concord"]["thai"]

        result = None

        if merge is True:
            kwargs["format"] = UnitexConstants.FORMAT_MERGE
            if output is None:
                raise UnitexException("You must provide the output file path to use the merge option.")
            kwargs["output"] = output
            kwargs["only_matches"] = False

            result = output

        else:
            kwargs["format"] = UnitexConstants.FORMAT_TEXT
            kwargs["output"] = None
            kwargs["only_matches"] = False

            result = os.path.join(self.__dir, "concord.txt")
            if self.__options["virtualization"] is True:
                result = "%s%s" % (UnitexConstants.VFS_PREFIX, result)

        ret = concord(index, alphabet, **kwargs)
        if ret is False:
            raise UnitexException("Concord failed!")

        if exists(result) is False:
            raise UnitexException("Concord failed! No concordances produced.")
        return result

    def open(self, path, mode="srtl", tagged=False):
        """
        This function opens the text in a Unitex way. It means that it
        applies all the preprocessing operations: normalization of
        separators, splitting into sentences, normalization of
        non-ambiguous forms, tokenization and application of
        dictionaries.

        Arguments:
            path [str] -- the input corpus file path.

            mode [str] -- this parameter (de)activates all the
                pre-processing operations. Possible values are: 's' for
                sentence segmentation, 'r' to apply Replace.fst2, 't'
                to tokenize and 'l' to lexicalize (apply the
                dictionaries). For instance, if you want to segment,
                tokenize and lexicalize, the mode will be 'stl'.

            tagged [bool] -- this parameter specifies if the input text
                is tagged or not. Tf True, this parameter deactivate two
                preprocessing options: sentence segmentation and
                Replace.fst2 application.
        """
        directory, filename = os.path.split(path)
        name, extension = os.path.splitext(filename)

        self.__txt = path
        self.__snt = os.path.join(directory, "%s.snt" % name)
        self.__dir = os.path.join(directory, "%s_snt" % name)

        if self.__options["virtualization"] is True:
            txt = "%s%s" % (UnitexConstants.VFS_PREFIX, self.__txt)
            cp(self.__txt, txt)

            self.__txt = txt
            self.__snt = "%s%s" % (UnitexConstants.VFS_PREFIX, self.__snt)

        else:
            if os.path.exists(self.__dir) is False:
                mkdir(self.__dir)

        self._normalize()

        if tagged is False:
            if "s" in mode:
                self._segment()
            if "r" in mode:
                self._replace()

        if "t" in mode:
            self._tokenize()
        if "l" in mode:
            self._lexicalize()

    def close(self, clean=True, free=False):
        """
        This function resets all the internal parameters used by the
        Unitex processor such as the working directory (*_snt) and the
        normalized text file (*.snt).

        Arguments:
            clean [bool] -- if set to False, all the files created by
                the Unitex processor will be kept on the disk or the
                virtual filesystem if the virtualization is activated.
                This option must be activated for debugging purposes
                only (default: True).

            free [bool] -- if persistence is activated, by setting this
                option to True, all the persisted resources will be
                freed from memory. You should use this option when all
                your corpus are processed (default: False).
        """
        if clean is True:
            self._clean()

        if free is True:
            self._free()

        self.__txt = None
        self.__snt = None
        self.__dir = None

    def tag(self, grammar, output, **kwargs):
        """
        This function tags the current opened corpus.

        Arguments:
            grammar [str] -- fst2 transducer used to tag the corpus.

            output [str] -- the output file path.

        Keyword arguments:
            xml [bool] -- if set to True, the resulting file will
                contain the XML headers.

            match_mode [str] -- Possible values are:
                - UnitexConstants.MATCH_MODE_SHORTEST
                - UnitexConstants.MATCH_MODE_LONGEST (default)
        """
        xml = kwargs.get("xml", False)
        match_mode = kwargs.get("match_mode", UnitexConstants.MATCH_MODE_LONGEST)
        if match_mode not in (UnitexConstants.MATCH_MODE_LONGEST, UnitexConstants.MATCH_MODE_SHORTEST):
            raise UnitexException("Invalid match mode '%s'...")
        output_mode = UnitexConstants.OUTPUT_MODE_MERGE

        index = self._locate(grammar, match_mode, output_mode)

        if xml is False:
            self._concord(index, merge=True, output=output)
            if exists(output) is False:
                raise UnitexException("No tagged file produced!")
            return True

        _output = os.path.join(self.__dir, "concord-merge-temp.txt")
        if self.__options["virtualization"] is True:
            _output = "%s%s" % (UnitexConstants.VFS_PREFIX, _output)

        self._concord(index, merge=True, output=_output)
        if exists(_output) is False:
            raise UnitexException("No (temporary) tagged file produced!")

        tagged = open(output, "w", encoding="utf-8")
        tagged.write(u"<?xml version='1.0' encoding='UTF-8'?>\n")
        tagged.write(u"<TAGFILE query='%s'>\n" % grammar)

        merged = UnitexFile()
        merged.open(_output, "r")
        content = merged.read()
        merged.close()

        content = escape(content)
        tagged.write(content)

        tagged.write(u"</TAGFILE>\n")
        tagged.close()
        rm(_output)

        return True

    def search(self, grammar, output, **kwargs):
        raise NotImplementedError

    def extract(self, grammar, output, **kwargs):
        raise NotImplementedError
