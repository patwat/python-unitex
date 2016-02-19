#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _unitex import unitex_tool
from unitex import UnitexException, UnitexConstants, LOGGER



def check_dic(dictionary, dtype, alphabet, **kwargs):
    """This function checks the format of <dela> and produces a file named
    CHECK_DIC.TXT that contains check result informations. This file is
    stored in the <dela> directory.

    Arguments:
        dictionary [str] -- the dictionary file path
        dtype [str]      -- the dictionary type: UnitexConstants.DELAF (inflected)
                                                 UnitexConstants.DELAS (non inflected)
        alphabet [str]   -- the alphabet file path

    Keyword arguments:
        strict [bool]           -- strict syntax checking against unprotected dot and comma (default: False) 
        no_space_warning [bool] -- tolerates spaces in grammatical/semantic/inflectional codes (default: True) 

    Return [bool]:
        The function returns 'True' if it succeeds and 'False' otherwise.
    """
    options = CheckDicOptions()
    options.load(kwargs)

    if os.path.exists(dictionary) is False:
        raise UnitexException("[CHECKDIC] Dictionary file '%s' doesn't exists" % dictionary)

    command = ["UnitexTool", "CheckDic"]

    if dtype == UnitexConstants.DELAF:
        command.append("--delaf")
    elif dtype == UnitexConstants.DELAS:
        command.append("--delas")

    if options["strict"] is True:
        command.append("--strict")
    if options["no_space_warning"] is True:
        command.append("--no_space_warning")

    command .append("--alphabet=%s" % alphabet)

    command.append(dictionary)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Checking dic '%s'" % dictionary)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def compress(dictionary, **kwargs):
    """This function takes a DELAF dictionary as a parameter and compresses it. The
    compression of a dictionary dico.dic produces two files:

        - dico.bin: a binary file containing the minimum automaton of the inflected
                    forms of the dictionary;
        - dico.inf: a text file containing the compressed forms required for the reconstruction
                    of the dictionary lines from the inflected forms contained in the
                    automaton.

    Arguments:
        dictionary [str] -- the dictionary file path

    Keyword arguments:
        output [str]   -- sets the output file. By default, a file xxx.dic will
                          produce a file xxx.bin
        flip [bool]    -- indicates that the inflected and canonical forms should be swapped in the
                          compressed dictionary. This option is used to construct an inverse dictionary
                          which is necessary for the program 'Reconstrucao' (default: False)
        semitic [bool] -- indicates that the semitic compression algorithm should be used. Setting this
                          option with semitic languages like Arabic significantly reduces the size of
                          the output dictionary (default: False)
        version [str]  -- 'v1': produces an old style .bin file
                          'v2': produces a new style .bin file, with no file size limitation to 16 Mb
                                and a smaller size (default)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = CompressOptions()
    options.load(kwargs)

    if os.path.exists(dictionary) is False:
        raise UnitexException("[COMPRESS] Dictionary file '%s' doesn't exists" % dictionary)

    command = ["UnitexTool", "Compress"]

    if options["output"] is not None:
        command.append("--output=%s" % options["output"])
    if options["flip"] is True:
        command.append("--flip")
    if options["semitic"] is True:
        command.append("--semitic")

    if options["version"] == UnitexConstants.DICTIONARY_VERSION_1:
        command.append("--v1")
    elif options["version"] == UnitexConstants.DICTIONARY_VERSION_2:
        command.append("--v2")

    command.append(dictionary)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Compressing dic '%s'" % dictionary)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def concord(index, alphabet, **kwargs):
    """This function takes a concordance index file produced by the function Locate and
    produces a concordance. It is also possible to produce a modified text version taking
    into account the transducer outputs associated to the occurrences. 

    The result of the application of this function is a file called concord.txt if the concordance
    was constructed in text mode, a file called concord.html if the output
    mode was --html, --glossanet or --script, and a text file with the name de-
    fined by the user of the function if the function has constructed a modified version
    of the text.

    In --html mode, the occurrence is coded as a hypertext link. The reference associated
    to this link is of the form <a href="X Y Z">. X et Y represent the beginning
    and ending positions of the occurrence in characters in the file text_name.snt. Z
    represents the number of the sentence in which the occurrence was found.

    Arguments:
        index [str]     -- the index file path (produced by the 'locate' function)
        alphabet [str]  -- alphabet file used for sorting

    Keyword arguments:

      - Generic options:
            font [str]            -- the name of the font to use if the output is an HTML
                                     file
            fontsize [int]        -- the font size to use if the output is an HTML file. The
                                     font parameters are required if the output is an HTML file;
            only_ambiguous [bool] -- Only displays identical occurrences with ambiguous
                                     outputs, in text order (default: False)
            only_matches [bool]   -- this option will force empty right and left contexts. Moreover,
                                     if used with -t/–text, Concord will not surround matches with
                                     tabulations (default: False)
            left [str]            -- number of characters on the left of the occurrences (default=0).
                                     In Thai mode, this means the number of non-diacritic characters.
            right [str]           -- number of characters (non-diacritic ones in Thai mode) on
                                     the right of the occurrences (default=0). If the occurrence is
                                     shorter than this value, the concordance line is completed up to
                                     right. If the occurrence is longer than the length defined by
                                     right, it is nevertheless saved as whole.

            NOTE: For both --left and --right, you can add the s character to stop at
            the first {S} tag. For instance, if you set 40s for the left value, the left context
            will end at 40 characters at most, less if the {S} tag is found before.

      - Sort options:
            sort [str] -- 'UnitexConstants.SORT_TEXT_ORDER': order in which the occurrences appear in the text (default)
                          'UnitexConstants.SORT_LEFT_CENTER': left context for primary sort, then occurrence for secondary sort
                          'UnitexConstants.SORT_LEFT_RIGHT': left context, then right context
                          'UnitexConstants.SORT_CENTER_LEFT': occurrence, then left context
                          'UnitexConstants.SORT_CENTER_RIGHT': occurrence, then right context
                          'UnitexConstants.SORT_RIGHT_LEFT': right context, then left context
                          'UnitexConstants.SORT_RIGHT_CENTER': left context, then occurrence

      - Output options:
            format [str]   -- 'html': produces a concordance in HTML format encoded in UTF-8 (default)
                              'text': produces a concordance in Unicode text format
                              'glossanet': produces a concordance for GlossaNet in HTML format where occurrences
                                           are links described by the 'script' argument (cf. Unitex manual p. 268).
                                           The HTML file is encoded in UTF-8
                              'script': produces a HTML concordance file where occurrences are links described by
                                        the 'script' argument
                              'index': produces an index of the concordance, made of the content of the occurrences
                                       (with the grammar outputs, if any), preceded by the positions of the
                                       occurrences in the text file given in characters
                              'uima': produces an index of the concordance relative to the original text file,
                                      before any Unitex operation. The 'offsets' argument must be provided
                              'prlg': produces a concordance for PRLG corpora where each line is prefixed by
                                      information extracted with Unxmlize’s 'prlg' option. You must provide both the
                                      'offsets' and the 'unxmlize' argument
                              'xml': produces xml index of the concordance
                              'xml-with-header': produces xml index of the concordance with full xml header
                              'axis': quite the same as 'index', but the numbers represent the median character of
                                      each occurrence
                              'xalign': another index file, used by the text alignment module. Each line is made of
                                        3 integers X Y Z followed by the content of the occurrence. X is the sentence
                                        number, starting from 1. Y and Z are the starting and ending positions of the
                                        occurrence in the sentence, given in characters
                              'merge': indicates to the function that it is supposed to produce a modified version of
                                       the text and save it in a file. The filename must be provided with the 'output'
                                       argument
            script [str]   -- string describing the links format for 'glossanet' and 'script' output. For instance,
                              if you use 'http://www.google.com/search?q=', you will obtain a HTML concordance
                              file where occurrences are hyperlinks to Google queries
            offsets [str]  -- the file produced by Tokenize’s output_offsets option (needed by the 'uima' and the
                              'prlg' format)
            unxmlize [str] -- file produced by Unxmlize’s 'prlg' option (needed by the 'prlg' format)
            output [str]   -- the output filename (needed by the 'merge' format)

      - Other options:
            directory [str] -- indicates to the function that it must not work in the same directory
                               than <index> but in 'directory'
            thai [bool]     -- option to use for Thai concordances (default: False)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = ConcordOptions()
    options.load(kwargs)

    if os.path.exists(index) is False:
        raise UnitexException("[CONCORD] Index file '%s' doesn't exists" % index)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[CONCORD] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Concord"]

    if self["font"] is not None:
        command.append("--font=%s" % self["font"])
    if self["fontsize"] is not None:
        command.append("--fontsize=%s" % self["fontsize"])
    if self["only_ambiguous"] is True:
        command.append("--only_ambiguous")
    if self["only_matches"] is True:
        command.append("--only_matches")

    command.append("--left=%s" % self["left"])
    command.append("--right=%s" % self["right"])

    if self["sort"] == UnitexConstants.SORT_TEXT_ORDER:
        command.append("--TO")
    elif self["sort"] == UnitexConstants.SORT_LEFT_CENTER:
        command.append("--LC")
    elif self["sort"] == UnitexConstants.SORT_LEFT_RIGHT:
        command.append("--LR")
    elif self["sort"] == UnitexConstants.SORT_CENTER_LEFT:
        command.append("--CL")
    elif self["sort"] == UnitexConstants.SORT_CENTER_RIGHT:
        command.append("--CR")
    elif self["sort"] == UnitexConstants.SORT_RIGHT_LEFT:
        command.append("--RL")
    elif self["sort"] == UnitexConstants.SORT_RIGHT_CENTER:
        command.append("--RC")

    if self["format"] == UnitexConstants.FORMAT_HTML:
        command.append("--html")
    elif self["format"] == UnitexConstants.FORMAT_TEXT:
        command.append("--text")
    elif self["format"] == UnitexConstants.FORMAT_GLOSSANET:
        command.append("--glossanet=%s" % self["script"])
    elif self["format"] == UnitexConstants.FORMAT_SCRIPT:
        command.append("--script=%s" % self["script"])
    elif self["format"] == UnitexConstants.FORMAT_INDEX:
        command.append("--index")
    elif self["format"] == UnitexConstants.FORMAT_UIMA:
        command.append("--uima=%s" % self["offsets"])
    elif self["format"] == UnitexConstants.FORMAT_PRLG:
        command.append("--PRLG=%s,%s" % self["unxmlize"], self["offsets"])
    elif self["format"] == UnitexConstants.FORMAT_XML:
        command.append("--xml")
    elif self["format"] == UnitexConstants.FORMAT_XML_WITH_HEADERS:
        command.append("--xml-with-header")
    elif self["format"] == UnitexConstants.FORMAT_AXIS:
        command.append("--axis")
    elif self["format"] == UnitexConstants.FORMAT_XALIGN:
        command.append("--xalign")
    elif self["format"] == UnitexConstants.FORMAT_MERGE:
        command.append("--merge=%s" % self["output"])

    if self["directory"] is not None:
        command.append("--directory=%s" % self["directory"])

    command.append("--alphabet=%s" % alphabet)

    if self["thai"] is not True:
        command.append("--thai")

    command.append(index)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Create concordance for '%s'" % index)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def dico(dictionaries, text, alphabet, **kwargs):
    """This function applies dictionaries to a text. The text must have been cut up into
    lexical units by the 'tokenize' function.

    The function 'dico' produces the following files, and saves them in the directory of
    the text:
        - dlf: dictionary of simple words in the text
        - dlc: dictionary of compound words in the text
        - err: list of unknown words in the text
        - tags_err: unrecognized simple words that are not matched by the tags.ind
                    file
        - tags.ind: sequences to be inserted in the text automaton (see section 3.8.3,
                    page 69)
        - stat_dic.n: file containing the number of simple words, the number of compound
                      words, and the number of unknown words in the text

    NOTE: Files dlf, dlc, err and tags_err are not sorted. Use the function sort_txt
    to sort them

    Arguments:
        dictionaries [list(str)] -- list of dictionary pathes ('bin' or 'fst2' formats)
        text     [str]           -- text (snt format) file path
        alphabet [str]           -- alphabet file path

    Keyword arguments:
        morpho [list(str)] -- this optional argument indicates which morphological mode
                              dictionaries are to be used, if needed by some .fst2
                              dictionaries. The argument is a list of dictionary path
                              (bin format)
        korean [bool]      -- specify the dictionary is in korean (default: False)
        semitic [bool]     -- specify the dictionary is in a semitic language (default: False)
        arabic_rules [str] -- specifies the Arabic typographic rule configuration file path
        raw [str]          -- alternative output file path containing both simple and compound
                              words, without requiring a text directory

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = DicoOptions()
    options.load(kwargs)

    for dictionary in dictionaries:
        if os.path.exists(dictionary) is False:
            raise UnitexException("[DICO] Dictionary file '%s' doesn't exists" % dictionary)
    if os.path.exists(text) is False:
        raise UnitexException("[DICO] Text file '%s' doesn't exists" % text)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[DICO] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Dico"]

    command.append("--text=%s" % text)
    command.append("--alphabet=%s" % alphabet)

    if options["morpho"] is not None:
        command.append("--morpho=%s" % ",".join(self["morpho"]))
    if options["korean"] is True:
        command.append("--korean")
    if options["semitic"] is True:
        command.append("--semitic")
    if options["arabic_rules"] is not None:
        command.append("--arabic_rules=%s" % self["arabic_rules"])
    if options["raw"] is not None:
        command.append("--raw=%s" % raw)

    command += dictionaries

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Applying dictionaries")
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def extract(text, output, index, **kwargs):
    """This program extracts from the given text all sentences that contain at least one
    occurrence from the concordance. The parameter <text> represents the complete
    path of the text file, without omitting the extension .snt.

    Arguments:
        text [str]   -- the text file (.snt format)
        output [str] -- the output text file
        index [str]  -- the index file path (produced by the 'locate' function)

    Keyword arguments:
        non_matching_sentences [bool] -- extracts all sentences that don’t contain matching
                                         units (default: False)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = ExtractOptions()
    options.load(kwargs)

    if os.path.exists(text) is False:
        raise UnitexException("[EXTRACT] Text file '%s' doesn't exists" % text)
    if os.path.exists(index) is False:
        raise UnitexException("[EXTRACT] Index file '%s' doesn't exists" % index)

    command = ["UnitexTool", "Extract"]

    if self["non_matching_sentence"] is False:
        command.append("--yes")
    else:
        command.append("--no")

    command.append("--output=%s" % output)
    command.append("--index=%s" % index)

    command.append(text)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Extracting sentences")
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def fst2txt(grammar, text, alphabet, **kwargs):
    """This function applies a transducer to a text in longest match mode at the preprocessing
    stage, when the text has not been cut into lexical units yet. This function modifies the input
    text file.

    This function modifies the input text file.

    Arguments:
        grammar [str]  -- The fst2 to apply on the text
        text [str]     -- the text file to be modified, with extension .snt
        alphabet [str] -- the alphabet file of the language of the text

    Keyword arguments:
        start_on_space [bool] -- this parameter indicates that the search will start at
                                 any position in the text, even before a space. This parameter
                                 should only be used to carry out morphological searches
                                 (default: False)
        char_by_char [bool]   -- works in character by character tokenization mode.
                                 This is useful for languages like Thai (default: False)
        merge [bool]          -- merge (instead of replace) transducer outputs with text inputs
                                 (default: True)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = Fst2TxtOptions()
    options.load(kwargs)

    if os.path.exists(grammar) is False:
        raise UnitexException("[FST2TXT] Grammar file '%s' doesn't exists" % grammar)
    if os.path.exists(text) is False:
        raise UnitexException("[FST2TXT] Text file '%s' doesn't exists" % text)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[FST2TXT] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Fst2Txt"]

    command.append("--text=%s" % text)
    command.append("--alphabet=%s" % alphabet)

    if options["start_on_space"] is False:
        command.append("--dont_start_on_space")
    else:
        command.append("--start_on_space")

    if options["char_by_char"] is False:
        command.append("--word_by_word")
    else:
        command.append("--char_by_char")

    if options["merge"] is True:
        command.append("--merge")
    else:
        command.append("--replace")

    command.append(grammar)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Applying grammar '%s'..." % grammar)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def grf2fst2(grammar, alphabet, **kwargs):
    """This program compiles a grammar into a .fst2 file (for more details see section
    6.2). The parameter <grf> denotes the complete path of the main graph of the
    grammar, without omitting the extension .grf.

    The result is a file with the same name as the graph passed to the program as a
    parameter, but with extension .fst2. This file is saved in the same directory as
    <grf>.

    Arguments:
        grammar [str]  -- The grf to compile
        alphabet [str] -- specifies the alphabet file to be used for tokenizing the content of
                          the grammar boxes into lexical units

    Keyword arguments:
        loop_check [bool]              -- enables error (loop) checking (default: False)
        char_by_char [bool]            -- tokenization will be done character by character.
                                          If neither -c nor -a option is used, lexical units
                                          will be sequences of any Unicode letters (default: False)
        pkgdir [str]                   -- specifies the repository directory to use (see section
                                          5.2.2, page 99)
        no_empty_graph_warning [bool]  -- no warning will be emitted when a graph matches the
                                          empty word. This option is used by MultiFlex in order
                                          not to scare users with meaningless error messages when
                                          they design an inflection grammar that matches the
                                          empty word (default: False)
        tfst_check [bool]              -- checks wether the given graph can be considered as a
                                          valid sentence automaton or not (default: False)
        silent_grf_name [bool]         -- does not print the graph names (needed for consistent
                                          log files across several systems; default: False)
        named_repositories [list(str)] -- declaration of named repositories. This argument is made
                                          of one or more X=Y sequences, separated by ‘;’, where X is
                                          the name of the repository denoted by pathname Y. You can
                                          use this option several times
        debug [bool]                   -- compile graphs in debug mode (default: False)
        check_variables [bool]         -- check output validity to avoid malformed variable
                                          expressions (default: False)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = Grf2Fst2Options()
    options.load(kwargs)

    if os.path.exists(grammar) is False:
        raise UnitexException("[GRF2FST2] Grammar file '%s' doesn't exists" % grammar)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[GRF2FST2] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Grf2Fst2"]

    if options["loop_check"] is False:
        command.append("--no_loop_check")
    else:
        command.append("--loop_check")

    command.append("--alphabet=%s" % options["alphabet"])

    if options["char_by_char"] is True:
        command.append("--char_by_char")
    if options["pkgdir"] is not None:
        command.append("--pkgdir=%s" % options["pkgdir"])
    if options["no_empty_graph_warning"] is True:
        command.append("--no_empty_graph_warning")
    if options["tfst_check"] is True:
        command.append("--tfst_check")
    if options["silent_grf_name"] is True:
        command.append("--silent_grf_name")
    if options["named_repositories"] is not None:
        command.append("--named_repositories=%s" % ";".join(options["named_repositories"]))
    if options["debug"] is True:
        command.append("--debug")
    if options["check_variables"] is True:
        command.append("--check_variables")

    command.append(grammar)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Compiling grammar '%s'..." % grammar)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def locate(grammar, text, alphabet, **kwargs):
    """This function applies a grammar to a text and constructs an index of the occurrences
    found.

    This function saves the references to the found occurrences in a file called concord.ind.
    The number of occurrences, the number of units belonging to those occurrences, as
    well as the percentage of recognized units within the text are saved in a file called
    concord.n. These two files are stored in the directory of the text.

    Arguments:
        grammar [str]  -- The fst2 to apply on the text
        text [str]     -- the text file, with extension .snt
        alphabet [str] -- the alphabet file of the language of the text

    Keyword arguments:
      - Generic options:
            start_on_space [bool]   -- this parameter indicates that the search will start at
                                       any position in the text, even before a space. This parameter
                                       should only be used to carry out morphological searches
                                       (default: False)
            char_by_char [bool]     -- works in character by character tokenization mode.
                                       This is useful for languages like Thai (default: False)
            morpho [list(str)]      -- this optional argument indicates which morphological mode
                                       dictionaries are to be used, if needed by some .fst2
                                       dictionaries. The argument is a list of dictionary path
                                       (bin format)
            korean [bool]           -- specify the dictionary is in korean (default: False)
            arabic_rules [str]      -- specifies the Arabic typographic rule configuration file path
            sntdir [str]            -- puts produced files in 'sntdir' instead of the text directory
                                       Note that 'sntdir' must end with a file separator (\ or /);
            negation_operator [str] -- specifies the negation operator to be used in Locate patterns.
                                       The two legal values for X are minus and tilde (default).
                                       Using minus provides backward compatibility with previous versions
                                       of Unitex.

      - Search limit options:
            number_of_matches [int] -- stops after the first N matches (default: all matches)

      - Maximum iterations per token options:
            stop_token_count [list(int_1, int_2)] -- emits a warning after 'int_1' iterations on a
                                                     token and stops after 'int_2' iterations.

      - Matching mode options:
            match_mode [str] -- 'shortest': shortest match mode
                                'longest': longest match mode (default)
                                'all': all match mode

      - Output options:
            output_mode [str]             -- 'ignore': ignore transducer outputs (default)
                                             'merge': merge transducer outputs with text inputs 
                                             'replace': replace texts inputs with corresponding transducer
                                                        outputs
            protect_dic_chars [bool]      -- when 'merge' or 'replace' mode is used, this option protects some
                                             input characters with a backslash. This is useful when Locate is
                                             called by Dico in order to avoid producing bad lines like: 3,14,.PI.NUM
                                             (default: True)
            variable [list(str_1, str_2)] -- sets an output variable named str_1 with content str_2. Note that str_2
                                             must be ASCII.

      - Ambiguous output options:
            ambiguous_outputs [bool] -- allows the production of several matches with same input but different
                                        outputs. If False, in case of ambiguous outputs, one will be arbitrarily
                                        chosen and kept, depending on the internal state of the function
                                        (default: True)
            variable_error [str]     -- 'exit': kills the function if variable has an empty content
                                        'ignore': ignore the errors (default)
                                        'backtrack': stop the current path exploration

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = LocateOptions()
    options.load(kwargs)

    if os.path.exists(grammar) is False:
        raise UnitexException("[LOCATE] Grammar file '%s' doesn't exists" % grammar)
    if os.path.exists(text) is False:
        raise UnitexException("[LOCATE] Text file '%s' doesn't exists" % text)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[LOCATE] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Locate"]

    command.append("--text=%s" % text)
    command.append("--alphabet=%s" % alphabet)

    if options["morpho"] is not None:
        command.append("--morpho=%s" % ",".join(self["morpho"]))

    if options["start_on_space"] is False:
        command.append("--dont_start_on_space")
    else:
        command.append("--start_on_space")

    if options["char_by_char"] is False:
        command.append("--word_by_word")
    else:
        command.append("--char_by_char")

    if options["sntdir"] is not None:
        command.append("--sntdir=%s" % self["sntdir"])
    if options["korean"] is True:
        command.append("--korean")
    if options["arabic_rules"] is not None:
        command.append("--arabic_rules=%s" % self["arabic_rules"])
    if options["negation_operator"] is not None:
        command.append("--negation_operator=%s" % self["negation_operator"])

    if options["number_of_matches"] is None:
        command.append("--all")
    else:
        command.append("--number_of_matches=%s" % self["number_of_matches"])

    if options["stop_token_count"] is not None:
        if options["stop_token_count[0]"] is None:
            command.append("--stop_token_count=%s" % stop_token_count[1])
        else:
            command.append("--stop_token_count=%s,%s" % (stop_token_count[0], stop_token_count[1]))

    if options["match_mode"] == UnitexConstants.MATCH_MODE_LONGEST:
        command.append("--longest_matches")
    elif options["match_mode"] == UnitexConstants.MATCH_MODE_SHORTEST:
        command.append("--shortest_matches")
    elif options["match_mode"] == UnitexConstants.MATCH_MODE_ALL:
        command.append("--all_matches")

    if options["output_mode"] == UnitexConstants.OUTPUT_MODE_IGNORE:
        command.append("--ignore")
    elif options["output_mode"] == UnitexConstants.OUTPUT_MODE_MERGE:
        command.append("--merge")
    elif options["output_mode"] == UnitexConstants.OUTPUT_MODE_RELACE:
        command.append("--replace")

    if options["protect_dic_chars"] is True:
        command.append("--protect_dic_chars")

    if options["variable"] is not None:
        command.append("--variable=%s=%s" % (self["variable"][0], self["variable"][1]))

    if options["ambiguous_outputs"] is True:
        command.append("--ambiguous_outputs")
    else:
        command.append("--no_ambiguous_outputs")

    if options["variable_error"] == UnitexConstants.ON_ERROR_IGNORE:
        command.append("--ignore_variable_error")
    elif options["variable_error"] == UnitexConstants.ON_ERROR_EXIT:
        command.append("--exit_on_variable_error")
    elif options["variable_error"] == UnitexConstants.ON_ERROR_BACKTRACK:
        command.append("--backtrack_on_variable_error")

    command.append(grammar)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Locating pattern '%s'..." % grammar)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def normalize(text, **kwargs):
    """This function carries out a normalization of text separators. The separators are
    space, tab, and newline. Every sequence of separators that contains at least one
    newline is replaced by a unique newline. All other sequences of separators are replaced
    by a single space.

    This function also checks the syntax of lexical tags found in the text. All sequences in
    curly brackets should be either the sentence delimiter {S}, the stop marker {STOP},
    or valid entries in the DELAF format ({aujourd’hui,.ADV}).

    Parameter <text> represents the complete path of the text file. The function creates
    a modified version of the text that is saved in a file with extension .snt.

    WARNING: if you specify a normalization rule file, its rules will be applied prior to
    anything else. So, you have to be very careful if you manipulate separators in such
    rules.

    Arguments:
        text [str] -- The text file to normalize

    Keyword arguments:
        no_carriage_return [bool]         -- every separator sequence will be turned into a single
                                             space (default: False)
        input_offsets [str]               -- base offset file to be used
        output_offsets [str]              -- offset file to be produced
        replacement_rules [str]           -- specifies the normalization rule file
                                             to be used. See section 14.13.6 for details about the
                                             format of this file. By default, the program only
                                             replaces { and } by [ and ]
        no_separator_normalization [bool] -- only applies replacement rules specified with -r
                                             (default: False)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = NormalizeOptions()
    options.load(kwargs)

    if os.path.exists(text) is False:
        raise UnitexException("[NORMALIZE] Text file '%s' doesn't exists" % text)

    command = ["UnitexTool", "Normalize"]

    if options["no_carriage_return"] is True:
        command.append("--no_carriage_return")

    if options["input_offsets"] is not None:
        command.append("--input_offsets=%s" % self["input_offsets"])
    if options["output_offsets"] is not None:
        command.append("--output_offsets=%s" % self["output_offsets"])

    if options["replacement_rules"] is not None:
        command.append("--replacement_rules=%s" % self["replacement_rules"])

    if options["no_separator_normalization"] is True:
        command.append("--no_separator_normalization")

    command.append(text)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Normalizing text '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def sort_txt(text, **kwargs):
    """This function carries out a lexicographical sorting of the lines of file <txt>. <txt>
    represents the complete path of the file to be sorted.

    The input text file is modified. By default, the sorting is performed in the order of
    Unicode characters, removing duplicate lines.

    Arguments:
        text [str] -- The text file to sort

    Keyword arguments:
        duplicates [bool]                   -- keep duplicate lines (default: False)
        reverse [bool]                      -- sort in descending order (default: False)
        sort_order [str]                    -- sorts using the alphabet order defined in this
                                               file. If this parameter is missing, the sorting
                                               is done according to the order of Unicode
                                               characters
        line_info [str]                     -- backup the number of lines of the result file
                                               in this file
        thai [bool]                         -- option for sorting Thai text (default: False)
        factorize_inflectional_codes [bool] -- makes two entries XXX,YYY.ZZZ:A and XXX,YYY.ZZZ:B
                                               become a single entry XXX,YYY.ZZZ:A:B
                                               (default: False)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = SortTxtOptions()
    options.load(kwargs)

    if os.path.exists(text) is False:
        raise UnitexException("[SORTTXT] Text file '%s' doesn't exists" % text)

    command = ["UnitexTool", "SortTxt"]

    if options["duplicates"] is False:
        command.append("--no_duplicates")
    else:
        command.append("--duplicates")

    if options["reverse"] is True:
        command.append("--reverse")
    if options["sort_order"] is None:
        command.append("--sort_order=%s" % self["sort_order"])
    if options["line_info"] is None:
        command.append("--line_info=%s" % self["line_info"])
    if options["thai"] is True:
        command.append("--thai")
    if options["factorize_inflectional_codes"] is True:
        command.append("--factorize_inflectional_codes")

    command.append(text)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Sorting file '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def tokenize(text, alphabet, **kwargs):
    """This function tokenizes a tet text into lexical units. <txt> the complete path of the
    text file, without omitting the .snt extension.

    The program codes each unit as a whole. The list of units is saved in a text file called
    tokens.txt. The sequence of codes representing the units now allows the coding
    of the text. This sequence is saved in a binary file named text.cod. The program
    also produces the following four files:
        - tok_by_freq.txt: text file containing the units sorted by frequency
        - tok_by_alph.txt: text file containing the units sorted alphabetically
        - stats.n: text file containing information on the number of sentence separators,
                   the number of units, the number of simple words and the number of
                   numbers
        - enter.pos: binary file containing the list of newline positions in the text. The
                     coded representation of the text does not contain newlines, but spaces.
                     Since a newline counts as two characters and a space as a single one,
                     it is necessary to know where newlines occur in the text when the
                     positions of occurrences located by the Locate program are to be
                     synchronized with the text file. File enter.pos is used for this by
                     the Concord program. Thanks to this, when clicking on an occurrence in
                     a concordance, it is correctly selected in the text. File enter.pos is
                     a binary file containing the list of the positions of newlines in the
                     text.

    All produced files are saved in the text directory

    Arguments:
        text [str]     -- the text file to tokenize (snt format)
        alphabet [str] -- the alphabet file

    Keyword arguments:
      - Generic options:
            char_by_char [bool] -- indicates whether the program is applied character by
                                   character, with the exceptions of the sentence delimiter
                                   {S}, the stop marker {STOP} and lexical tags like
                                   {today,.ADV} which are considered to be single units
                                   (default: False)
            tokens [str]        -- specifies a tokens.txt file to load and modify, instead
                                   of creating a new one from scratch

      - Offsets options:
            input_offsets [str]  -- base offset file to be used;
            output_offsets [str] -- offset file to be produced;

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = TokenizeOptions()
    options.load(kwargs)

    if os.path.exists(text) is False:
        raise UnitexException("[TOKENIZE] Text file '%s' doesn't exists" % text)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[TOKENIZE] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Tokenize"]

    command.append("--alphabet=%s" % alphabet)

    if options["char_by_char"] is True:
        command.append("--char_by_char")
    else:
        command.append("--word_by_word")

    if options["tokens"] is not None:
        command.append("--tokens=%s" % self["tokens"])

    if options["input_offsets"] is not None:
        command.append("--input_offsets=%s" % self["input_offsets"])
    if options["output_offsets"] is not None:
        command.append("--output_offsets=%s" % self["output_offsets"])

    command.append(text)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Tokenizing file '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret



def txt2tfst(text, alphabet, **kwargs):
    """This function constructs an automaton of a text.

    If the text is separated into sentences, the function constructs an automaton for each
    sentence. If this is not the case, the program arbitrarily cuts the text into sequences
    of 2000 tokens and produces an automaton for each of these sequences.

    The result is a file called text.tfst which is saved in the directory of the text.
    Another file named text.tind is also produced.

    Arguments:
        text [str]     -- the path to the text file in snt format.
        alphabet [str] -- the alphabet file

    Keyword arguments:
        clean [bool]                -- indicates whether the rule of conservation of the best
                                       paths (see section 7.2.4) should be applied
                                       (default: False)
        normalization_grammar [str] -- name of a normalization grammar that is to be applied
                                       to the text automaton
        tagset [str]                -- Elag tagset file to use to normalize dictionary entries
        korean [bool]               -- tells the function that it works on Korean
                                       (default: False)

    Return [bool]:
        The function return 'True' if it succeeds and 'False' otherwise.
    """
    options = Txt2TFstOptions()
    options.load(kwargs)

    if os.path.exists(text) is False:
        raise UnitexException("[TXT2TFST] Text file '%s' doesn't exists" % text)
    if os.path.exists(alphabet) is False:
        raise UnitexException("[TXT2TFST] Alphabet file '%s' doesn't exists" % alphabet)

    command = ["UnitexTool", "Txt2Tfst"]

    command.append("--alphabet=%s" % alphabet)

    if options["clean"] is not False:
        command.append("--clean")
    if options["normalization_grammar"] is not None:
        command.append("--normalization_grammar=%s" % self["normalization_grammar"])
    if options["tagset"] is not None:
        command.append("--tagset=%s" % self["tagset"])
    if options["korean"] is not False:
        command.append("--korean")

    command.append(text)

    command.append("-qutf8-no-bom")
    command = " ".join(command)

    LOGGER.info("Building text automaton for '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = unitex_tool(command)

    return ret
