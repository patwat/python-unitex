#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest

from unitex import *
from unitex.tools import *


class Arguments:

    def __init__(self, language=None):
        self.__arguments = {}

        self.__arguments["dic"] = "data/dictionary.dic" 
        self.__arguments["dic_type"] = UnitexConstants.DELAF
        self.__arguments["dic_check"] = "data/CHECK_DIC.TXT" 

        self.__arguments["bin"] = "data/dictionary.bin" 
        self.__arguments["inf"] = "data/dictionary.inf" 

        self.__arguments["alphabet"] = "data/Alphabet.txt" 
        self.__arguments["alphabet_sort"] = "data/Alphabet_sort.txt" 

        self.__arguments["sentence"] = "data/Sentence.fst2" 

        self.__arguments["txt"] = "data/corpus.txt" 
        self.__arguments["snt"] = "data/corpus.snt" 
        self.__arguments["dir"] = "data/corpus_snt" 
        self.__arguments["xtr"] = "data/corpus.xtr" 

        self.__arguments["text.cod"] = os.path.join(self.__arguments["dir"], "text.cod")
        self.__arguments["tok_by_freq.txt"] = os.path.join(self.__arguments["dir"], "tok_by_freq.txt")
        self.__arguments["tok_by_alph.txt"] = os.path.join(self.__arguments["dir"], "tok_by_alph.txt")
        self.__arguments["stats.n"] = os.path.join(self.__arguments["dir"], "stats.n")
        self.__arguments["enter.pos"] = os.path.join(self.__arguments["dir"], "enter.pos")

        self.__arguments["dlf"] = os.path.join(self.__arguments["dir"], "dlf")
        self.__arguments["dlc"] = os.path.join(self.__arguments["dir"], "dlc")
        self.__arguments["err"] = os.path.join(self.__arguments["dir"], "err")
        self.__arguments["tags_err"] = os.path.join(self.__arguments["dir"], "tags_err")
        self.__arguments["tags.ind"] = os.path.join(self.__arguments["dir"], "tags.ind")
        self.__arguments["stat_dic.n"] = os.path.join(self.__arguments["dir"], "stat_dic.n")

        self.__arguments["text.tfst"] = os.path.join(self.__arguments["dir"], "text.tfst")
        self.__arguments["text.tind"] = os.path.join(self.__arguments["dir"], "text.tind")

        self.__arguments["grf"] = "data/grammar.grf" 
        self.__arguments["fst"] = "data/grammar.fst2" 

        self.__arguments["ind"] = os.path.join(self.__arguments["dir"], "concord.ind") 
        self.__arguments["concord.n"] = os.path.join(self.__arguments["dir"], "concord.n") 
        self.__arguments["concordances"] = os.path.join(self.__arguments["dir"], "concord.txt") 

    def __getitem__(self, key):
        if key not in self.__arguments:
            raise KeyError("Argument '%s' not found ..." % key)
        return self.__arguments[key]



class TestUnitexTools(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._arguments = Arguments()

    @classmethod
    def tearDownClass(self):
        # Removing output file from the 'check_dic' command.
        if os.path.exists(self._arguments["dic_check"]):
            os.remove(self._arguments["dic_check"])

        # Removing output file from the 'compress' command.
        if os.path.exists(self._arguments["bin"]):
            os.remove(self._arguments["bin"])
        if os.path.exists(self._arguments["inf"]):
            os.remove(self._arguments["inf"])

        # Removing output file from the 'normalize' and 'fst2txt' commands.
        if os.path.exists(self._arguments["snt"]):
            os.remove(self._arguments["snt"])

        # Removing (recursively) the text directory.
        if os.path.exists(self._arguments["dir"]):
            shutil.rmtree(self._arguments["dir"])

        # Removing output file from the 'grf2fst2' command.
        if os.path.exists(self._arguments["fst"]):
            os.remove(self._arguments["fst"])

        # Removing output file from the 'extract' command.
        if os.path.exists(self._arguments["xtr"]):
            os.remove(self._arguments["xtr"])

    def test_01_check_dic(self):
        dictionary = self._arguments["dic"]
        dtype = self._arguments["dic_type"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["strict"] = False
        kwargs["no_space_warning"] = True

        ret = check_dic(dictionary, dtype, alphabet, **kwargs)

        ok = os.path.exists(self._arguments["dic_check"]) and ret

        self.assertTrue(ok, "Dictionary checking failed!")

    def test_02_compress(self):
        dictionary = self._arguments["dic"]

        kwargs = {}
        kwargs["output"] = None
        kwargs["flip"] = False
        kwargs["semitic"] = False
        kwargs["version"] = UnitexConstants.DICTIONARY_VERSION_1

        ret = compress(dictionary, **kwargs)

        ok = os.path.exists(self._arguments["bin"]) and os.path.exists(self._arguments["inf"]) and ret

        self.assertTrue(ok, "Compression failed!")

    def test_03_normalize(self):
        text = self._arguments["txt"]

        kwargs = {}
        kwargs["no_carriage_return"] = False
        kwargs["input_offsets"] = None
        kwargs["output_offsets"] = None
        kwargs["replacement_rules"] = None
        kwargs["no_separator_normalization"] = False

        ret = normalize(text, **kwargs)

        ok = os.path.exists(self._arguments["snt"]) and ret

        self.assertTrue(ok, "Normalisation failed!")

    def test_04_fst2txt(self):
        grammar = self._arguments["sentence"]
        text = self._arguments["snt"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["start_on_space"] = False
        kwargs["char_by_char"] = False
        kwargs["merge"] = True

        ret = fst2txt(grammar, text, alphabet, **kwargs)

        ok = ret

        self.assertTrue(ok, "FST application failed!")

    def test_05_tokenize(self):
        if not os.path.exists(self._arguments["dir"]):
            os.mkdir(self._arguments["dir"])

        text = self._arguments["snt"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["char_by_char"] = False
        kwargs["tokens"] = None
        kwargs["input_offsets"] = None
        kwargs["output_offsets"] = None

        ret = tokenize(text, alphabet, **kwargs)

        ok = ret
        ok = ok and os.path.exists(self._arguments["text.cod"])
        ok = ok and os.path.exists(self._arguments["tok_by_freq.txt"])
        ok = ok and os.path.exists(self._arguments["tok_by_alph.txt"])
        ok = ok and os.path.exists(self._arguments["stats.n"])
        ok = ok and os.path.exists(self._arguments["enter.pos"])

        self.assertTrue(ok, "Tokenisation failed!")

    def test_06_dico(self):
        dictionaries = [self._arguments["bin"]]
        text = self._arguments["snt"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["morpho"] = None
        kwargs["korean"] = False
        kwargs["semitic"] = False
        kwargs["arabic_rules"] = None
        kwargs["raw"] = None

        ret = dico(dictionaries, text, alphabet, **kwargs)

        ok = ret
        ok = ok and os.path.exists(self._arguments["dlf"])
        ok = ok and os.path.exists(self._arguments["dlc"])
        ok = ok and os.path.exists(self._arguments["err"])
        ok = ok and os.path.exists(self._arguments["tags_err"])
        ok = ok and os.path.exists(self._arguments["tags.ind"])
        ok = ok and os.path.exists(self._arguments["stat_dic.n"])

        self.assertTrue(ok, "Dictionary application failed!")

    def test_07_sort_txt(self):
        files = []
        files.append(self._arguments["dlf"])
        files.append(self._arguments["dlc"])
        files.append(self._arguments["err"])
        files.append(self._arguments["tags_err"])

        kwargs = {}
        kwargs["duplicates"] = False
        kwargs["reverse"] = False
        kwargs["sort_order"] = self._arguments["alphabet_sort"]
        kwargs["line_info"] = self._arguments["stat_dic.n"]
        kwargs["thai"] = False
        kwargs["factorize_inflectional_codes"] = False

        ok = True

        for text in files:
            ret = sort_txt(text, **kwargs)

            ok = ok and ret

        self.assertTrue(ok, "Sorting failed!")

    def test_08_grf2fst2(self):
        grammar = self._arguments["grf"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["loop_check"] = False
        kwargs["char_by_char"] = False
        kwargs["pkgdir"] = None
        kwargs["no_empty_graph_warning"] = False
        kwargs["tfst_check"] = False
        kwargs["silent_grf_name"] = False
        kwargs["named_repositories"] = None
        kwargs["debug"] = False
        kwargs["check_variables"] = False

        ret = grf2fst2(grammar, alphabet, **kwargs)

        ok = os.path.exists(self._arguments["fst"]) and ret

        self.assertTrue(ok, "Grammar compilation failed!")

    def test_09_locate(self):
        grammar = self._arguments["fst"]
        text = self._arguments["snt"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["start_on_space"] = False
        kwargs["char_by_char"] = False
        kwargs["morpho"] = None
        kwargs["korean"] = False
        kwargs["arabic_rules"] = None
        kwargs["sntdir"] = None
        kwargs["negation_operator"] = UnitexConstants.NEGATION_OPERATOR

        kwargs["number_of_matches"] = None

        kwargs["stop_token_count"] = None

        kwargs["match_mode"] = UnitexConstants.MATCH_MODE_LONGEST

        kwargs["output_mode"] = UnitexConstants.OUTPUT_MODE_MERGE
        kwargs["protect_dic_chars"] = True
        kwargs["variable"] = None

        kwargs["ambiguous_outputs"] = True
        kwargs["variable_error"] = UnitexConstants.ON_ERROR_IGNORE

        ret = locate(grammar, text, alphabet, **kwargs)

        ok = os.path.exists(self._arguments["ind"]) and os.path.exists(self._arguments["concord.n"]) and ret

        self.assertTrue(ok, "Locate failed!")

    def test_10_concord(self):
        index = self._arguments["ind"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["font"] = None
        kwargs["fontsize"] = None
        kwargs["only_ambiguous"] = False
        kwargs["only_matches"] = False
        kwargs["left"] = "1000s"
        kwargs["right"] = "1000s"

        kwargs["sort"] = UnitexConstants.SORT_CENTER_RIGHT

        kwargs["format"] = UnitexConstants.FORMAT_TEXT
        kwargs["script"] = None
        kwargs["offsets"] = None
        kwargs["unxmlize"] = None
        kwargs["output"] = None

        kwargs["directory"] = None
        kwargs["thai"] = False

        ret = concord(index, alphabet, **kwargs)

        ok = os.path.exists(self._arguments["concordances"]) and ret

        self.assertTrue(ok, "Concord failed!")

    def test_11_txt2tfst(self):
        text = self._arguments["snt"]
        alphabet = self._arguments["alphabet"]

        kwargs = {}
        kwargs["clean"] = False
        kwargs["normalization_grammar"] = None
        kwargs["tagset"] = None
        kwargs["korean"] = False

        ret = txt2tfst(text, alphabet, **kwargs)

        ok = ret
        ok = ok and os.path.exists(self._arguments["text.tfst"])
        ok = ok and os.path.exists(self._arguments["text.tind"])

        self.assertTrue(ok, "Txt2Tfst failed!")

    def test_12_extract(self):
        text = self._arguments["snt"]
        output = self._arguments["xtr"]
        index = self._arguments["ind"]

        kwargs = {}
        kwargs["non_matching_sentences"] = False

        ret = extract(text, output, index, **kwargs)

        ok = ret
        ok = ok and os.path.exists(self._arguments["xtr"])

        self.assertTrue(ok, "Extract failed!")


if __name__ == '__main__':
    unittest.main()
