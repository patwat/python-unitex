#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import tempfile

from unitex import *
from unitex.io import exists

LOGGER = logging.getLogger(__name__)



class Options(object):

    def __init__(self, options=None):
        self.__options = {}

        if options is not None:
            self.load(options)

    def __contains__(self, key):
        return key in self.__options

    def __getitem__(self, key):
        if key not in self.__options:
            raise UnitexException("Key '%s' not found!" % key)
        return self.__options[key]

    def __setitem__(self, key, value):
        self.__options[key] = value

    def load(self, options):
        raise NotImplementedError



class CheckDicOptions(Options):

    def __init__(self):
        super(CheckDicOptions, self).__init__()

    def load(self, options):
        strict = options.get("strict", False)
        if isinstance(strict, bool) is False:
            raise UnitexException("[CHECK_DIC] Wrong value for the 'strict' option. Boolean required.")
        self["strict"] = strict

        no_space_warning = options.get("no_space_warning", True)
        if isinstance(no_space_warning, bool) is False:
            raise UnitexException("[CHECK_DIC] Wrong value for the 'no_space_warning' option. Boolean required.")
        self["no_space_warning"] = no_space_warning



class CompressOptions(Options):

    def __init__(self):
        super(CompressOptions, self).__init__()

    def load(self, options):
        output = options.get("output", None)
        if output is not None and isinstance(output, str) is False:
            raise UnitexException("[COMPRESS] Wrong value for the 'output' option. String required.")
        self["output"] = output

        flip = options.get("flip", False)
        if isinstance(flip, bool) is False:
            raise UnitexException("[COMPRESS] Wrong value for the 'flip' option. Boolean required.")
        self["flip"] = flip

        semitic = options.get("semitic", False)
        if isinstance(semitic, bool) is False:
            raise UnitexException("[COMPRESS] Wrong value for the 'semitic' option. Boolean required.")
        self["semitic"] = semitic

        version = options.get("version", UnitexConstants.DICTIONARY_VERSION_2)
        if version not in (UnitexConstants.DICTIONARY_VERSION_1, UnitexConstants.DICTIONARY_VERSION_2):
            raise UnitexException("[COMPRESS] Wrong value for the 'version' option. UnitexConstants.DICTIONARY_VERSION_X required.")
        self["version"] = version



class ConcordOptions(Options):

    def __init__(self):
        super(ConcordOptions, self).__init__()

    def load(self, options):
        font = options.get("font", None)
        if font is not None and isinstance(font, str) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'font' option. String required.")
        self["font"] = font

        fontsize = options.get("fontsize", None)
        if fontsize is not None and isinstance(fontsize, int) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'fontsize' option. Integer required.")
        self["fontsize"] = fontsize

        only_ambiguous = options.get("only_ambiguous", False)
        if isinstance(only_ambiguous, bool) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'only_ambiguous' option. Boolean required.")
        self["only_ambiguous"] = only_ambiguous

        only_matches = options.get("only_matches", False)
        if isinstance(only_matches, bool) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'only_matches' option. Boolean required.")
        self["only_matches"] = only_matches

        left = options.get("left", "0")
        if left is not None and isinstance(left, str) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'left' option. String required.")
        self["left"] = left

        right = options.get("right", "0")
        if right is not None and isinstance(right, str) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'right' option. String required.")
        self["right"] = right

        sort = options.get("sort", UnitexConstants.SORT_TEXT_ORDER)
        if sort not in (UnitexConstants.SORT_TEXT_ORDER,
                        UnitexConstants.SORT_LEFT_CENTER,
                        UnitexConstants.SORT_LEFT_RIGHT,
                        UnitexConstants.SORT_CENTER_LEFT,
                        UnitexConstants.SORT_CENTER_RIGHT,
                        UnitexConstants.SORT_RIGHT_LEFT,
                        UnitexConstants.SORT_RIGHT_CENTER):
            raise UnitexException("[CONCORD] Wrong value for the 'sort' option. UnitexConstants.SORT_XXX required.")
        self["sort"] = sort

        format = options.get("format", UnitexConstants.FORMAT_TEXT)
        if format not in (UnitexConstants.FORMAT_HTML,
                          UnitexConstants.FORMAT_TEXT,
                          UnitexConstants.FORMAT_GLOSSANET,
                          UnitexConstants.FORMAT_SCRIPT,
                          UnitexConstants.FORMAT_INDEX,
                          UnitexConstants.FORMAT_UIMA,
                          UnitexConstants.FORMAT_PRLG,
                          UnitexConstants.FORMAT_XML,
                          UnitexConstants.FORMAT_XML_WITH_HEADERS,
                          UnitexConstants.FORMAT_AXIS,
                          UnitexConstants.FORMAT_XALIGN,
                          UnitexConstants.FORMAT_MERGE):
            raise UnitexException("[CONCORD] Wrong value for the 'format' option. UnitexConstants.FORMAT_XXX required.")
        self["format"] = format

        self["script"] = None
        self["offsets"] = None
        self["unxmlize"] = None
        self["output"] = None

        if self["format"] in (UnitexConstants.FORMAT_HTML, UnitexConstants.FORMAT_GLOSSANET, UnitexConstants.FORMAT_SCRIPT):
            if self["font"] is None:
                self["font"] = "Courier new"
            if self["fontsize"] is None:
                self["fontsize"] = 12

            if self["format"] in (UnitexConstants.FORMAT_GLOSSANET, UnitexConstants.FORMAT_SCRIPT):
                script = options.get("script", None)
                if script is None:
                    raise UnitexException("You must provide the 'script' option for UnitexConstants.FORMAT_(GLOSSANET|SCRIPT) formats...")
                self["script"] = script

        elif self["format"] == UnitexConstants.FORMAT_UIMA:
            offsets = options.get("offsets", None)
            if offsets is None:
                raise UnitexException("You must provide the 'offsets' option for UnitexConstants.FORMAT_UIMA formats...")
            self["offsets"] = offsets

        elif self["format"] == UnitexConstants.FORMAT_PRLG:
            offsets = options.get("offsets", None)
            if offsets is None:
                raise UnitexException("You must provide the 'offsets' option for UnitexConstants.FORMAT_PRLG formats...")
            self["offsets"] = offsets

            unxmlize = options.get("unxmlize", None)
            if unxmlize is None:
                raise UnitexException("You must provide the 'unxmlize' option for UnitexConstants.FORMAT_PRLG format...")
            self["unxmlize"] = unxmlize

        elif self["format"] == UnitexConstants.FORMAT_MERGE:
            output = options.get("output", None)
            if output is None:
                raise UnitexException("You must provide the 'output' option for UnitexConstants.FORMAT_MERGE format...")
            self["output"] = output

        directory = options.get("directory", None)
        if directory is not None:
            if isinstance(directory, str) is False:
                raise UnitexException("[CONCORD] Wrong value for the 'directory' option. String required.")
            if exists(directory) is False:
                raise UnitexException("[CONCORD] The text 'directory' doesn't exist.")
        self["directory"] = directory

        thai = options.get("thai", False)
        if isinstance(thai, bool) is False:
            raise UnitexException("[CONCORD] Wrong value for the 'thai' option. Boolean required.")
        self["thai"] = thai



class DicoOptions(Options):

    def __init__(self):
        super(DicoOptions, self).__init__()

    def load(self, options):
        morpho = options.get("morpho", None)
        if morpho is not None:
            if isinstance(morpho, list) is False:
                raise UnitexException("[DICO] Wrong value for the 'morpho' option. List of string required.")
            for dictionary in morpho:
                if exists(dictionary) is False:
                    raise UnitexException("[DICO] Morphological dictionary '%s' doesn't exist." % dictionary)
        self["morpho"] = morpho

        korean = options.get("korean", False)
        if isinstance(korean, bool) is False:
            raise UnitexException("[DICO] Wrong value for the 'korean' option. Boolean required.")
        self["korean"] = korean

        semitic = options.get("semitic", False)
        if isinstance(semitic, bool) is False:
            raise UnitexException("[DICO] Wrong value for the 'semitic' option. Boolean required.")
        self["semitic"] = semitic

        arabic_rules = options.get("arabic_rules", None)
        if arabic_rules is not None:
            if isinstance(arabic_rules, str) is False:
                raise UnitexException("[DICO] Wrong value for the 'arabic_rules' option. String required.")
            if exists(arabic_rules) is False:
                raise UnitexException("[DICO] Rules file '%s' doesn't exist." % arabic_rules)
        self["arabic_rules"] = arabic_rules

        raw = options.get("raw", None)
        if raw is not None and isinstance(raw, str) is False:
            raise UnitexException("[DICO] Wrong value for the 'raw' option. String required.")
        self["raw"] = raw



class ExtractOptions(Options):

    def __init__(self):
        super(ExtractOptions, self).__init__()

    def load(self, options):
        non_matching_sentences = options.get("non_matching_sentences", False)
        if isinstance(non_matching_sentences, bool) is False:
            raise UnitexException("[EXTRACT] Wrong value for the 'non_matching_sentences' option. Boolean required.")
        self["non_matching_sentences"] = non_matching_sentences



class Fst2TxtOptions(Options):

    def __init__(self):
        super(Fst2TxtOptions, self).__init__()

    def load(self, options):
        start_on_space = options.get("start_on_space", False)
        if isinstance(start_on_space, bool) is False:
            raise UnitexException("[FST2TXT] Wrong value for the 'start_on_space' option. Boolean required.")
        self["start_on_space"] = start_on_space

        char_by_char = options.get("char_by_char", False)
        if isinstance(char_by_char, bool) is False:
            raise UnitexException("[FST2TXT] Wrong value for the 'char_by_char' option. Boolean required.")
        self["char_by_char"] = char_by_char

        merge = options.get("merge", True)
        if isinstance(merge, bool) is False:
            raise UnitexException("[FST2TXT] Wrong value for the 'merge' option. Boolean required.")
        self["merge"] = merge



class Grf2Fst2Options(Options):

    def __init__(self):
        super(Grf2Fst2Options, self).__init__()

    def load(self, options):
        loop_check = options.get("loop_check", False)
        if isinstance(loop_check, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'loop_check' option. Boolean required.")
        self["loop_check"] = loop_check

        char_by_char = options.get("char_by_char", False)
        if isinstance(char_by_char, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'char_by_char' option. Boolean required.")
        self["char_by_char"] = char_by_char

        pkgdir = options.get("pkgdir", None)
        if pkgdir is not None and isinstance(pkgdir, str) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'pkgdir' option. String required.")
        self["pkgdir"] = pkgdir

        no_empty_graph_warning = options.get("no_empty_graph_warning", False)
        if isinstance(no_empty_graph_warning, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'no_empty_graph_warning' option. Boolean required.")
        self["no_empty_graph_warning"] = no_empty_graph_warning

        tfst_check = options.get("tfst_check", False)
        if isinstance(tfst_check, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'tfst_check' option. Boolean required.")
        self["tfst_check"] = tfst_check

        silent_grf_name = options.get("silent_grf_name", False)
        if isinstance(silent_grf_name, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'silent_grf_name' option. Boolean required.")
        self["silent_grf_name"] = silent_grf_name

        named_repositories = options.get("named_repositories", None)
        if named_repositories is not None and isinstance(named_repositories, str) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'named_repositories' option. String required.")
        self["named_repositories"] = named_repositories

        debug = options.get("debug", False)
        if isinstance(debug, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'debug' option. Boolean required.")
        self["debug"] = debug

        check_variables = options.get("check_variables", True)
        if isinstance(check_variables, bool) is False:
            raise UnitexException("[GRF2FST2] Wrong value for the 'check_variables' option. Boolean required.")
        self["check_variables"] = check_variables



class LocateOptions(Options):

    def __init__(self):
        super(LocateOptions, self).__init__()

    def load(self, options):
        start_on_space = options.get("start_on_space", False)
        if isinstance(start_on_space, bool) is False:
            raise UnitexException("[LOCATE] Wrong value for the 'start_on_space' option. Boolean required.")
        self["start_on_space"] = start_on_space

        char_by_char = options.get("char_by_char", False)
        if isinstance(char_by_char, bool) is False:
            raise UnitexException("[LOCATE] Wrong value for the 'char_by_char' option. Boolean required.")
        self["char_by_char"] = char_by_char

        morpho = options.get("morpho", None)
        if morpho is not None:
            if isinstance(morpho, list) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'morpho' option. List of string required.")
            for dictionary in morpho:
                if exists(dictionary) is False:
                    raise UnitexException("[LOCATE] Morphological dictionary '%s' doesn't exist." % dictionary)
        self["morpho"] = morpho

        korean = options.get("korean", False)
        if isinstance(korean, bool) is False:
            raise UnitexException("[LOCATE] Wrong value for the 'korean' option. Boolean required.")
        self["korean"] = korean

        arabic_rules = options.get("arabic_rules", False)
        if arabic_rules is not None:
            if isinstance(arabic_rules, str) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'arabic_rules' option. String required.")
            if exists(arabic_rules) is False:
                raise UnitexException("[LOCATE] Rules file '%s' doesn't exist." % arabic_rules)
        self["arabic_rules"] = arabic_rules

        sntdir = options.get("sntdir", None)
        if sntdir is not None:
            if isinstance(sntdir, str) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'sntdir' option. String required.")
            if exists(sntdir) is False:
                raise UnitexException("[LOCATE] Directory '%s' doesn't exist." % sntdir)
        self["sntdir"] = sntdir

        negation_operator = options.get("negation_operator", UnitexConstants.NEGATION_OPERATOR)
        if negation_operator not in (UnitexConstants.NEGATION_OPERATOR, UnitexConstants.NEGATION_OPERATOR_OLD):
            raise UnitexException("[LOCATE] Wrong value for the 'negation_operator' option. UnitexConstants.NEGATION_OPERATOR(_OLD) required.")
        self["negation_operator"] = negation_operator

        number_of_matches = options.get("number_of_matches", None)
        if number_of_matches is not None and isinstance(number_of_matches, int) is False:
            raise UnitexException("[LOCATE] Wrong value for the 'number_of_matches' option. Integer required.")
        self["number_of_matches"] = number_of_matches

        stop_token_count = options.get("stop_token_count", None)
        if stop_token_count is not None:
            if isinstance(stop_token_count, list) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'stop_token_count' option. List of 2 integers required.")
            if len(stop_token_count) != 2:
                raise UnitexException("[LOCATE] Wrong value for the 'stop_token_count' option. List of 2 integers required.")
            for i in stop_token_count:
                if isinstance(i, int) is False:
                    raise UnitexException("[LOCATE] Wrong value for the 'stop_token_count' option. List of 2 integers required.")
        self["stop_token_count"] = stop_token_count

        match_mode = options.get("match_mode", UnitexConstants.MATCH_MODE_LONGEST)
        if match_mode not in (UnitexConstants.MATCH_MODE_LONGEST,
                              UnitexConstants.MATCH_MODE_SHORTEST,
                              UnitexConstants.MATCH_MODE_ALL):
            raise UnitexException("[LOCATE] Wrong value for the 'match_mode' option. UnitexConstants.MATCH_MODE_X required.")
        self["match_mode"] = match_mode

        output_mode = options.get("output_mode", UnitexConstants.OUTPUT_MODE_IGNORE)
        if output_mode not in (UnitexConstants.OUTPUT_MODE_IGNORE,
                              UnitexConstants.OUTPUT_MODE_MERGE,
                              UnitexConstants.OUTPUT_MODE_RELACE):
            raise UnitexException("[LOCATE] Wrong value for the 'output_mode' option. UnitexConstants.OUTPUT_MODE_X required.")
        self["output_mode"] = output_mode

        protect_dic_chars = options.get("protect_dic_chars", True)
        if isinstance(protect_dic_chars, bool) is False:
            raise UnitexException("[LOCATE] Wrong value for the 'protect_dic_chars' option. Boolean required.")
        self["protect_dic_chars"] = protect_dic_chars

        variable = options.get("variable", None)
        if variable is not None:
            if isinstance(variable, list) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'variable' option. List of 2 strings required.")
            if len(variable) != 2:
                raise UnitexException("[LOCATE] Wrong value for the 'variable' option. List of 2 strings required.")
            if isinstance(variable[0], str) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'variable' option. List of 2 strings required.")
            # Checks if the second argument is in ascii
            if isinstance(variable[1], str) is False and all(ord(c) < 128 for c in variable[1]) is False:
                raise UnitexException("[LOCATE] Wrong value for the 'variable' option. List of 2 strings required (the second must be *ascii*).")
        self["variable"] = variable

        ambiguous_outputs = options.get("ambiguous_outputs", True)
        if isinstance(ambiguous_outputs, bool) is False:
            raise UnitexException("[LOCATE] Wrong value for the 'ambiguous_outputs' option. Boolean required.")
        self["ambiguous_outputs"] = ambiguous_outputs

        variable_error = options.get("variable_error", UnitexConstants.ON_ERROR_IGNORE)
        if variable_error not in (UnitexConstants.ON_ERROR_IGNORE,
                              UnitexConstants.ON_ERROR_EXIT,
                              UnitexConstants.ON_ERROR_BACKTRACK):
            raise UnitexException("[LOCATE] Wrong value for the 'variable_error' option. UnitexConstants.OUTPUT_MODE_X required.")
        self["variable_error"] = variable_error



class NormalizeOptions(Options):

    def __init__(self):
        super(NormalizeOptions, self).__init__()

    def load(self, options):
        no_carriage_return = options.get("no_carriage_return", False)
        if isinstance(no_carriage_return, bool) is False:
            raise UnitexException("[NORMALIZE] Wrong value for the 'no_carriage_return' option. Boolean required.")
        self["no_carriage_return"] = no_carriage_return

        input_offsets = options.get("input_offsets", None)
        if input_offsets is not None:
            if isinstance(input_offsets, str) is False:
                raise UnitexException("[NORMALIZE] Wrong value for the 'input_offsets' option. String required.")
            if exists(input_offsets) is False:
                raise UnitexException("[NORMALIZE] Offsets file '%s' doesn't exist." % input_offsets)
        self["input_offsets"] = input_offsets

        output_offsets = options.get("output_offsets", None)
        if output_offsets is not None and isinstance(output_offsets, str) is False:
                raise UnitexException("[NORMALIZE] Wrong value for the 'output_offsets' option. String required.")
        self["output_offsets"] = output_offsets

        if self["input_offsets"] is None and self["output_offsets"] is not None:
            raise UnitexException("[NORMALIZE] You must provide both input and output offsets...")
        if self["input_offsets"] is not None and self["output_offsets"] is None:
            raise UnitexException("[NORMALIZE] You must provide both input and output offsets...")

        no_separator_normalization = options.get("no_separator_normalization", False)
        if isinstance(no_separator_normalization, bool) is False:
            raise UnitexException("[NORMALIZE] Wrong value for the 'no_separator_normalization' option. Boolean required.")
        self["no_separator_normalization"] = no_separator_normalization

        replacement_rules = options.get("replacement_rules", None)
        if replacement_rules is not None:
            if isinstance(replacement_rules, str) is False:
                raise UnitexException("[NORMALIZE] Wrong value for the 'replacement_rules' option. String required.")
            if exists(replacement_rules) is False:
                raise UnitexException("[NORMALIZE] Rules file '%s' doesn't exist." % replacement_rules)
        self["replacement_rules"] = replacement_rules



class SortTxtOptions(Options):

    def __init__(self):
        super(SortTxtOptions, self).__init__()

    def load(self, options):
        duplicates = options.get("duplicates", False)
        if isinstance(duplicates, bool) is False:
            raise UnitexException("[SORTTXT] Wrong value for the 'duplicates' option. Boolean required.")
        self["duplicates"] = duplicates

        reverse = options.get("reverse", False)
        if isinstance(reverse, bool) is False:
            raise UnitexException("[SORTTXT] Wrong value for the 'reverse' option. Boolean required.")
        self["reverse"] = reverse

        sort_order = options.get("sort_order", None)
        if sort_order is not None:
            if isinstance(sort_order, str) is False:
                raise UnitexException("[SORTTXT] Wrong value for the 'sort_order' option. String required.")
            if exists(sort_order) is False:
                raise UnitexException("[SORTTXT] Alphabet file '%s' doesn't exist." % sort_order)
        self["sort_order"] = sort_order

        line_info = options.get("line_info", None)
        if line_info is not None and isinstance(line_info, str) is False:
            raise UnitexException("[SORTTXT] Wrong value for the 'line_info' option. String required.")
        self["line_info"] = line_info

        thai = options.get("thai", False)
        if isinstance(thai, bool) is False:
            raise UnitexException("[SORTTXT] Wrong value for the 'thai' option. Boolean required.")
        self["thai"] = thai

        factorize_inflectional_codes = options.get("factorize_inflectional_codes", False)
        if isinstance(factorize_inflectional_codes, bool) is False:
            raise UnitexException("[SORTTXT] Wrong value for the 'factorize_inflectional_codes' option. Boolean required.")
        self["factorize_inflectional_codes"] = factorize_inflectional_codes



class TokenizeOptions(Options):

    def __init__(self):
        super(TokenizeOptions, self).__init__()

    def load(self, options):
        char_by_char = options.get("char_by_char", False)
        if isinstance(char_by_char, bool) is False:
            raise UnitexException("[TOKENIZE] Wrong value for the 'char_by_char' option. Boolean required.")
        self["char_by_char"] = char_by_char

        tokens = options.get("tokens", None)
        if tokens is not None:
            if isinstance(tokens, str) is False:
                raise UnitexException("[TOKENIZE] Wrong value for the 'tokens' option. String required.")
            if exists(tokens) is False:
                raise UnitexException("[TOKENIZE] Tokens file '%s' doesn't exist." % tokens)
        self["tokens"] = tokens

        input_offsets = options.get("input_offsets", None)
        if input_offsets is not None:
            if isinstance(input_offsets, str) is False:
                raise UnitexException("[TOKENIZE] Wrong value for the 'input_offsets' option. String required.")
            if exists(input_offsets) is False:
                raise UnitexException("[TOKENIZE] Offsets file '%s' doesn't exist." % input_offsets)
        self["input_offsets"] = input_offsets

        output_offsets = options.get("output_offsets", None)
        if output_offsets is not None and isinstance(output_offsets, str) is False:
                raise UnitexException("[TOKENIZE] Wrong value for the 'output_offsets' option. String required.")
        self["output_offsets"] = output_offsets

        if self["input_offsets"] is None and self["output_offsets"] is not None:
            raise UnitexException("[TOKENIZE] You must provide both input and output offsets...")
        if self["input_offsets"] is not None and self["output_offsets"] is None:
            raise UnitexException("[TOKENIZE] You must provide both input and output offsets...")



class Txt2TFstOptions(Options):

    def __init__(self):
        super(Txt2TFstOptions, self).__init__()

    def load(self, options):
        clean = options.get("clean", False)
        if isinstance(clean, bool) is False:
            raise UnitexException("[TXT2TFST] Wrong value for the 'clean' option. Boolean required.")
        self["clean"] = clean

        normalization_grammar = options.get("normalization_grammar", None)
        if normalization_grammar is not None:
            if isinstance(normalization_grammar, str) is False:
                raise UnitexException("[TXT2TFST] Wrong value for the 'normalization_grammar' option. String required.")
            if exists(normalization_grammar) is False:
                raise UnitexException("[TXT2TFST] Offsets file '%s' doesn't exist." % normalization_grammar)
        self["normalization_grammar"] = normalization_grammar

        tagset = options.get("tagset", None)
        if tagset is not None:
            if isinstance(tagset, str) is False:
                raise UnitexException("[TXT2TFST] Wrong value for the 'tagset' option. String required.")
            if exists(tagset) is False:
                raise UnitexException("[TXT2TFST] Offsets file '%s' doesn't exist." % tagset)
        self["tagset"] = tagset

        korean = options.get("korean", False)
        if isinstance(korean, bool) is False:
            raise UnitexException("[TXT2TFST] Wrong value for the 'korean' option. Boolean required.")
        self["korean"] = korean



class ResourcesOptions(Options):

    def __init__(self):
        super(ResourcesOptions, self).__init__()

    def load(self, options):
        language = options.get("language", None)
        if language is None:
            raise UnitexException("[RESOURCES] You must specify the 'language' element.")
        self["language"] = language

        alphabet = options.get("alphabet", None)
        if alphabet is None:
            LOGGER.warning("[RESOURCES] No alphabet file provided.")
        elif not exists(alphabet):
            raise UnitexException("[RESOURCES] Alphabet file '%s' doesn't exist." % alphabet)
        self["alphabet"] = alphabet

        alphabet_sort = options.get("alphabet-sort", None)
        if alphabet_sort is None:
            LOGGER.warning("[RESOURCES] No sorted alphabet file provided.")
        elif not exists(alphabet_sort):
            raise UnitexException("[RESOURCES] Sorted alphabet file '%s' doesn't exist." % alphabet_sort)
        self["alphabet-sort"] = alphabet_sort

        sentence = options.get("sentence", None)
        if sentence is None:
            LOGGER.warning("[RESOURCES] No sentence grammar provided.")
        else:
            _, extension = os.path.splitext(sentence)
            if extension != ".fst2":
                raise UnitexException("[RESOURCES] Wrong extension for '%s'. Grammars must be compiled and have the '.fst2' extension.")
            if not exists(sentence):
                raise UnitexException("[RESOURCES] Sentence grammar file '%s' doesn't exist." % sentence)
        self["sentence"] = sentence

        replace = options.get("replace", None)
        if replace is None:
            LOGGER.warning("[RESOURCES] No replace grammar provided.")
        else:
            _, extension = os.path.splitext(replace)
            if extension != ".fst2":
                raise UnitexException("[RESOURCES] Wrong extension for '%s'. Grammars must be compiled and have the '.fst2' extension.")
            if not exists(replace):
                raise UnitexException("[RESOURCES] Replace grammar file '%s' doesn't exist." % replace)
        self["replace"] = replace

        dictionaries = options.get("dictionaries", None)
        if dictionaries is None:
            LOGGER.warning("[RESOURCES] No dictionaries provided.")
        else:
            if not isinstance(dictionaries, list):
                raise UnitexException("[RESOURCES] The 'dictionaries' element must be a list of .bin or .fst2 files.")
            for dictionary in dictionaries:
                prefix, extension = os.path.splitext(dictionary)
                if extension != ".bin" or extension != ".fst2":
                    raise UnitexException("[RESOURCES] Wrong extension for '%s'. Dictionaries must be compiled and have the '.bin' or the '.fst2' extension.")
                if not exists(dictionary):
                    raise UnitexException("[RESOURCES] Dictionary file '%s' doesn't exist." % dictionary)
                if extension == ".bin" and not exists("%s.inf" % prefix):
                    raise UnitexException("[RESOURCES] Dictionary .inf file missing for '%s'." % dictionary)
        self["dictionaries"] = dictionaries



class UnitexConfig(Options):

    def __init__(self):
        super(UnitexConfig, self).__init__()

    def load(self, settings):
        options = settings.get("global", {})

        verbose = options.get("verbose", VERBOSE)
        if verbose not in (0, 1, 2):
            raise UnitexException("Wrong value for the 'verbose' global option.")
        self["verbose"] = verbose

        debug = options.get("debug", DEBUG)
        if debug not in (0, 1):
            raise UnitexException("Wrong value for the 'debug' global option.")
        self["debug"] = debug

        tempdir = options.get("tempdir", tempfile.gettempdir())
        if not exists(tempdir):
            raise UnitexException("Temporary directory '%s' doesn't exist." % tempdir)
        self["tempdir"] = tempdir

        persistence = options.get("persistence", 0)
        if persistence not in (0, 1):
            raise UnitexException("Wrong value for the 'persistence' global option.")
        self["persistence"] = bool(persistence)

        virtualization = options.get("virtualization", 0)
        if virtualization not in (0, 1):
            raise UnitexException("Wrong value for the 'virtualization' global option.")
        self["virtualization"] = bool(virtualization)

        self["resources"] = ResourcesOptions(settings.get("resources", {}))

        options = settings.get("options", {})

        self["check_dic"] = CheckDicOptions(options.get("normalize", {}))
        self["compress"] = CheckDicOptions(options.get("normalize", {}))
        self["concord"] = ConcordOptions(options.get("concord", {}))
        self["dico"] = DicoOptions(options.get("dico", {}))
        self["extract"] = ExtractOptions(options.get("extract", {}))
        self["fst2txt"] = Fst2TxtOptions(options.get("extract", {}))
        self["Grf2Fst2"] = Grf2Fst2Options(options.get("extract", {}))
        self["locate"] = LocateOptions(options.get("locate", {}))
        self["normalize"] = NormalizeOptions(options.get("normalize", {}))
        self["sort_txt"] = SortTxtOptions(options.get("normalize", {}))
        self["tokenize"] = TokenizeOptions(options.get("tokenize", {}))
        self["txt2tfst"] = Txt2TFstOptions(options.get("tokenize", {}))
