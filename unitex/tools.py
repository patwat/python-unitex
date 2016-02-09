#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unitex import UnitexException, LOGGER, LIBUNITEX



def check_dic(*args, **kwargs):
    """This function checks the format of <dela> and produces a file named
    CHECK_DIC.TXT that contains check result informations. This file is
    stored in the <dela> directory.

    Arguments (length: 1):
        0 -- the dictionary file

    Keyword arguments:
        type [str]              -- 'delas' checks a non inflected dictionary
                                   'delaf' checks an inflected dictionary
        alphabet [str]          -- alphabet file to use
        strict [bool]           -- strict syntax checking against unprotected dot and comma (default: False) 
        no_space_warning [bool] -- tolerates spaces in grammatical/semantic/inflectional codes (default: True) 
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one dictionary to check...")
    dictionary = args[0]

    dtype = kwargs.get("type", None)
    if dtype is None:
        raise UnitexException("You must specify the dictionary type...")
    elif dtype not in ("delaf", "delas"):
        raise UnitexException("Unknown dictionary type '%s'..." % dtype)

    alphabet = kwargs.get("alphabet")
    if alphabet is None:
        raise UnitexException("You must specify the alphabet file path...")

    strict = kwargs.get("strict", False)
    no_space_warning = kwargs.get("no_space_warning", True)

    command = ["UnitexTool", "CheckDic"]

    if dtype == "delaf":
        command.append("--delaf")
    elif dtype == "delas":
        command.append("--delas")

    if strict is True:
        command.append("--strict")
    if no_space_warning is True:
        command.append("--no_space_warning")

    command .append("--alphabet=%s" % alphabet)

    command.append(dictionary)

    command = " ".join(command)

    LOGGER.info("Checking dic '%s'" % dictionary)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def compress(*args, **kwargs):
    """This function takes a DELAF dictionary as a parameter and compresses it. The
    compression of a dictionary dico.dic produces two files:

        - dico.bin: a binary file containing the minimum automaton of the inflected
                    forms of the dictionary;
        - dico.inf: a text file containing the compressed forms required for the reconstruction
                    of the dictionary lines from the inflected forms contained in the
                    automaton.

    Arguments (length: 1):
        0 -- the dictionary file

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
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one dictionary to check...")
    dictionary = args[0]

    output = kwargs.get("output", None)
    flip = kwargs.get("flip", False)
    semitic = kwargs.get("semitic", False)

    version = kwargs.get("version", "v2")
    if version not in ("v1", "v2"):
        raise UnitexException("Unknown dictionary version '%s'..." % version)

    command = ["UnitexTool", "Compress"]

    if output is not None:
        command.append("--output=%s" % output)
    if flip is True:
        command.append("--flip")
    if semitic is True:
        command.append("--semitic")

    if version == "v1":
        command.append("--v1")
    elif version == "v2":
        command.append("--v2")

    command.append(dictionary)

    command = " ".join(command)

    LOGGER.info("Compressing dic '%s'" % dictionary)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def concord(*args, **kwargs):
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

    Arguments (length: 1):
        0 -- index file

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
            sort [str] -- 'TO': order in which the occurrences appear in the text (default)
                          'LC': left context for primary sort, then occurrence for secondary sort
                          'LR': left context, then right context
                          'CL': occurrence, then left context
                          'CR': occurrence, then right context
                          'RL': right context, then left context
                          'RC': left context, then occurrence

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
            alphabet [str]  -- alphabet file used for sorting
            thai [bool]     -- option to use for Thai concordances (default: False)
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one concordance index...")
    index = args[0]

    font = kwargs.get("font", None)
    fontsize = kwargs.get("fontsize", None)
    only_ambiguous = kwargs.get("only_ambiguous", False)
    only_matches = kwargs.get("only_matches", False)
    left = kwargs.get("left", 0)
    right = kwargs.get("right", 0)

    sort = kwargs.get("sort", "TO")
    if sort not in ("TO", "LC", "LR", "CL", "CR", "RL", "RC"):
        raise UnitexException("Unknown sort order '%s'..." % sort)

    script = None
    offsets = None
    unxmlize = None
    output = None

    format = kwargs.get("format", "html")
    if format in ("glossanet", "script"):
        script = kwargs.get("script", None)
        if script is None:
            raise UnitexException("You must provide the 'script' argument for 'glossanet' and 'script' formats...")
    elif format == "uima":
        offsets = kwargs.get("offsets", None)
        if offsets is None:
            raise UnitexException("You must provide the 'offsets' argument for 'uima' and 'prlg' formats...")
    elif format == "prlg":
        offsets = kwargs.get("offsets", None)
        if offsets is None:
            raise UnitexException("You must provide the 'offsets' argument for 'uima' and 'prlg' formats...")
        unxmlize = kwargs.get("unxmlize", None)
        if unxmlize is None:
            raise UnitexException("You must provide the 'unxmlize' argument for 'prlg' format...")
    elif format == "merge":
        output = kwargs.get("output", None)
        if output is None:
            raise UnitexException("You must provide the 'output' argument for 'merge' format...")
    elif format not in ("html", "text", "index", "xml", "xml-with-header", "axis", "xalign"):
        raise UnitexException("Unknown output format '%s'..." % format)

    directory = kwargs.get("directory", None)
    thai = kwargs.get("thai", False)

    alphabet = kwargs.get("alphabet", None)
    if alphabet is None:
        raise UnitexException("You must provide the 'alphabet' argument...")

    command = ["UnitexTool", "Concord"]

    if font is not None:
        command.append("--font=%s" % font)
    if fontsize is not None:
        command.append("--fontsize=%s" % fontsize)
    if only_ambiguous is True:
        command.append("--only_ambiguous")
    if only_matches is True:
        command.append("--only_matches")

    command.append("--left=%s" % left)
    command.append("--right=%s" % right)

    if sort == "TO":
        command.append("--TO")
    elif sort == "LC":
        command.append("--LC")
    elif sort == "LR":
        command.append("--LR")
    elif sort == "CL":
        command.append("--CL")
    elif sort == "CR":
        command.append("--CR")
    elif sort == "RL":
        command.append("--RL")
    elif sort == "RC":
        command.append("--RC")

    if format == "html":
        command.append("--html")
    elif format == "text":
        command.append("--text")
    elif format == "glossanet":
        command.append("--glossanet=%s" % script)
    elif format == "script":
        command.append("--script=%s" % script)
    elif format == "index":
        command.append("--index")
    elif format == "uima":
        command.append("--uima=%s" % offsets)
    elif format == "prlg":
        command.append("--PRLG=%s,%s" % unxmlize, offsets)
    elif format == "xml":
        command.append("--xml")
    elif format == "xml-with-header":
        command.append("--xml-with-header")
    elif format == "axis":
        command.append("--axis")
    elif format == "xalign":
        command.append("--xalign")
    elif format == "merge":
        command.append("--merge=%s" % output)

    if directory is not None:
        command.append("--directory=%s" % directory)

    command.append("--alphabet=%s" % alphabet)

    if thai is not None:
        command.append("--thai")

    command.append(index)

    command = " ".join(command)

    LOGGER.info("Create concordance for '%s'" % index)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def dico(*args, **kwargs):
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

    Arguments (length: number of dictionaries):
        List of dictionaries ('bin' or 'fst2' formats)

    Keyword arguments:
        text [str]         -- text (snt format) file path
        alphabet [str]     -- the alphabet file path
        morpho [list(str)] -- this optional argument indicates which morphological mode
                              dictionaries are to be used, if needed by some .fst2
                              dictionaries. The argument is a list of dictionary path
                              (bin format)
        korean [bool]      -- specify the dictionary is in korean (default: False)
        semitic [bool]     -- specify the dictionary is in a semitic language (default: False)
        arabic_rules [str] -- specifies the Arabic typographic rule configuration file path
        raw [str]          -- alternative output file path containing both simple and compound
                              words, without requiring a text directory
    """

    if not args:
        raise UnitexException("You must provide the list of dictionaries to apply...")

    text = kwargs.get("text", None)
    if text is None:
        raise UnitexException("You must provide the text file path (snt format)...")

    alphabet = kwargs.get("alphabet", None)
    if alphabet is None:
        raise UnitexException("You must provide the alphabet file path...")

    morpho = kwargs.get("morpho", None)
    korean = kwargs.get("korean", False)
    semitic = kwargs.get("semitic", False)
    arabic_rules = kwargs.get("arabic_rules", None)
    raw = kwargs.get("raw", None)

    command = ["UnitexTool", "Dico"]

    command.append("--text=%s" % text)
    command.append("--alphabet=%s" % alphabet)

    if morpho is not None:
        command.append("--morpho=%s" % ",".join(morpho))
    if korean is True:
        command.append("--korean")
    if semitic is True:
        command.append("--semitic")
    if arabic_rules is not None:
        command.append("--arabic_rules=%s" % arabic_rules)
    if raw is not None:
        command.append("--raw=%s" % raw)

    command += args

    command = " ".join(command)

    LOGGER.info("Applying dictionaries")
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def fst2txt(*args, **kwargs):
    """This function applies a transducer to a text in longest match mode at the preprocessing
    stage, when the text has not been cut into lexical units yet. This function modifies the input
    text file.

    This function modifies the input text file.

    Arguments (length: 1):
        0 -- The fst2 to apply on the text

    Keyword arguments:
        text [str]            -- the text file to be modified, with extension .snt
        alphabet [str]        -- the alphabet file of the language of the text
        start_on_space [bool] -- this parameter indicates that the search will start at
                                 any position in the text, even before a space. This parameter
                                 should only be used to carry out morphological searches
                                 (default: False)
        char_by_char [bool]   -- works in character by character tokenization mode.
                                 This is useful for languages like Thai (default: False)
        merge [bool]          -- merge transducer outputs with text inputs (default: True)

    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one grammar to apply...")
    grammar = args[0]

    text = kwargs.get("text", None)
    if text is None:
        raise UnitexException("You must provide the text file path (snt format)...")

    alphabet = kwargs.get("alphabet", None)
    if alphabet is None:
        raise UnitexException("You must provide the alphabet file path...")

    start_on_space = kwargs.get("start_on_space", False)
    char_by_char = kwargs.get("char_by_char", False)
    merge = kwargs.get("merge", True)

    command = ["UnitexTool", "Fst2Txt"]

    command.append("--text=%s" % text)
    command.append("--alphabet=%s" % alphabet)

    if start_on_space is False:
        command.append("--dont_start_on_space")
    else:
        command.append("--start_on_space")

    if char_by_char is False:
        command.append("--word_by_word")
    else:
        command.append("--char_by_char")

    if merge is True:
        command.append("--merge")
    else:
        command.append("--replace")

    command.append(grammar)

    command = " ".join(command)

    LOGGER.info("Applying grammar '%s'..." % grammar)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def grf2fst2(*args, **kwargs):
    """This program compiles a grammar into a .fst2 file (for more details see section
    6.2). The parameter <grf> denotes the complete path of the main graph of the
    grammar, without omitting the extension .grf.

    The result is a file with the same name as the graph passed to the program as a
    parameter, but with extension .fst2. This file is saved in the same directory as
    <grf>.

    Arguments (length: 1):
        0 -- The grf to compile

    Keyword arguments:
        loop_check [bool]              -- enables error (loop) checking (default: False)
        alphabet [str]                 -- specifies the alphabet file to be used for
                                          tokenizing the content of the grammar boxes into
                                          lexical units
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
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one grammar to compile...")
    grammar = args[0]

    loop_check = kwargs.get("loop_check", False)

    alphabet = kwargs.get("alphabet", None)
    if alphabet is None:
        raise UnitexException("You must provide the alphabet file path...")

    char_by_char = kwargs.get("char_by_char", False)
    pkgdir = kwargs.get("pkgdir", None)
    no_empty_graph_warning = kwargs.get("no_empty_graph_warning", False)
    tfst_check = kwargs.get("tfst_check", False)
    silent_grf_name = kwargs.get("silent_grf_name", False)
    named_repositories = kwargs.get("named_repositories", None)
    debug = kwargs.get("debug", False)
    check_variables = kwargs.get("check_variables", False)

    command = ["UnitexTool", "Grf2Fst2"]

    if loop_check is False:
        command.append("--no_loop_check")
    else:
        command.append("--loop_check")

    command.append("--alphabet=%s" % alphabet)

    if char_by_char is True:
        command.append("--char_by_char")
    if pkgdir is not None:
        command.append("--pkgdir=%s" % pkgdir)
    if no_empty_graph_warning is True:
        command.append("--no_empty_graph_warning")
    if tfst_check is True:
        command.append("--tfst_check")
    if silent_grf_name is True:
        command.append("--silent_grf_name")
    if named_repositories is not None:
        command.append("--named_repositories=%s" % named_repositories)
    if debug is True:
        command.append("--debug")
    if check_variables is True:
        command.append("--check_variables")

    command.append(grammar)

    command = " ".join(command)

    LOGGER.info("Compiling grammar '%s'..." % grammar)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def locate(*args, **kwargs):
    """This function applies a grammar to a text and constructs an index of the occurrences
    found.

    This function saves the references to the found occurrences in a file called concord.ind.
    The number of occurrences, the number of units belonging to those occurrences, as
    well as the percentage of recognized units within the text are saved in a file called
    concord.n. These two files are stored in the directory of the text.

    Arguments (length: 1):
        0 -- The fst2 to apply on the text

    Keyword arguments:
      - Generic options:
            text [str]              -- the text file, with extension .snt
            alphabet [str]          -- the alphabet file of the language of the text
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
            stop_token_count [tuple(int_1, int_2)] --  emits a warning after 'int_1' iterations on a
                                                       token and stops after 'int_2' iterations.

      - Matching mode options:
            match_mode [str] -- 'shortest': shortest match mode
                                'longest': longest match mode (default)
                                'all': all match mode

      - Output options:
            output_mode [str]              -- 'ignore': ignore transducer outputs (default)
                                              'merge': merge transducer outputs with text inputs 
                                              'replace': replace texts inputs with corresponding transducer
                                                         outputs
            protect_dic_chars [bool]       -- when 'merge' or 'replace' mode is used, this option protects some
                                              input characters with a backslash. This is useful when Locate is
                                              called by Dico in order to avoid producing bad lines like: 3,14,.PI.NUM
                                              (default: True)
            variable [tuple(str_1, str_2)] -- sets an output variable named str_1 with content str_2. Note that str_2
                                              must be ASCII.

      - Ambiguous output options:
            ambiguous_outputs [bool] -- allows the production of several matches with same input but different
                                        outputs (default: True). If False, in case of ambiguous outputs, one will
                                        be arbitrarily chosen and kept, depending on the internal state of the
                                        function (default: True)
            variable_error [str]     -- 'exit': kills the function if variable has an empty content
                                        'ignore': ignore the errors (default)
                                        'backtrack': stop the current path exploration
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one grammar to apply...")
    grammar = args[0]

    text = kwargs.get("text", None)
    if text is None:
        raise UnitexException("You must provide the text file path (snt format)...")

    alphabet = kwargs.get("alphabet", None)
    if alphabet is None:
        raise UnitexException("You must provide the alphabet file path...")

    morpho = kwargs.get("morpho", None)
    start_on_space = kwargs.get("start_on_space", False)
    char_by_char = kwargs.get("char_by_char", False)
    sntdir = kwargs.get("sntdir", None)
    korean = kwargs.get("korean", False)
    arabic_rules = kwargs.get("arabic_rules", None)
    negation_operator = kwargs.get("negation_operator", None)

    number_of_matches = kwargs.get("number_of_matches", None)

    stop_token_count = kwargs.get("stop_token_count", None)

    match_mode = kwargs.get("match_mode", "longest")
    if match_mode not in ("shortest", "longest", "all"):
        raise UnitexException("Invalid match mode '%s'..." % match_mode)

    output_mode = kwargs.get("output_mode", "ignore")
    if output_mode not in ("ignore", "merge", "replace"):
        raise UnitexException("Invalid output mode '%s'..." % output_mode)

    protect_dic_chars = kwargs.get("protect_dic_chars", False)
    variable = kwargs.get("variable", None)

    ambiguous_outputs = kwargs.get("ambiguous_outputs", True)

    variable_error = kwargs.get("variable_error", "")
    if variable_error not in ("exit", "ignore", "backtrack"):
        raise UnitexException("Invalid variable error handling mode '%s'..." % variable_error)

    command = ["UnitexTool", "Locate"]

    command.append("--text=%s" % text)
    command.append("--alphabet=%s" % alphabet)

    if morpho is not None:
        command.append("--morpho=%s" % ",".join(morpho))

    if start_on_space is False:
        command.append("--dont_start_on_space")
    else:
        command.append("--start_on_space")

    if char_by_char is False:
        command.append("--word_by_word")
    else:
        command.append("--char_by_char")

    if sntdir is not None:
        command.append("--sntdir=%s" % sntdir)
    if korean is True:
        command.append("--korean")
    if arabic_rules is not None:
        command.append("--arabic_rules=%s" % arabic_rules)
    if negation_operator is not None:
        command.append("--negation_operator=%s" % negation_operator)

    if number_of_matches is None:
        command.append("--all")
    else:
        command.append("--number_of_matches=%s" % number_of_matches)

    if stop_token_count is not None:
        if stop_token_count[0] is None:
            command.append("--stop_token_count=%s" % stop_token_count[1])
        else:
            command.append("--stop_token_count=%s,%s" % (stop_token_count[0], stop_token_count[1]))

    if match_mode == "longest":
        command.append("--longest_matches")
    elif match_mode == "shortest":
        command.append("--shortest_matches")
    elif match_mode == "all":
        command.append("--all_matches")

    if output_mode == "ignore":
        command.append("--ignore")
    elif output_mode == "merge":
        command.append("--merge")
    elif output_mode == "replace":
        command.append("--replace")

    if protect_dic_chars is True:
        command.append("--protect_dic_chars")

    if variable is not None:
        command.append("--variable=%s=%s" % (variable[0], variable[1]))

    if ambiguous_outputs is True:
        command.append("--ambiguous_outputs")
    else:
        command.append("--no_ambiguous_outputs")

    if variable_error == "ignore":
        command.append("--ignore_variable_error")
    elif variable_error == "exit":
        command.append("--exit_on_variable_error")
    elif variable_error == "backtrack":
        command.append("--backtrack_on_variable_error")

    command.append(grammar)

    command = " ".join(command)

    LOGGER.info("Locating pattern '%s'..." % grammar)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def normalize(*args, **kwargs):
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

    Arguments (length: 1):
        0 -- The text file to normalize

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
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one text to normalize...")
    text = args[0]

    no_carriage_return = kwargs.get("no_carriage_return", False)

    input_offsets = kwargs.get("input_offsets", None)
    output_offsets = kwargs.get("output_offsets", None)
    if input_offsets is None and output_offsets is not None:
        raise UnitexException("You must provide both input and output offsets...")
    if input_offsets is not None and output_offsets is None:
        raise UnitexException("You must provide both input and output offsets...")

    replacement_rules = kwargs.get("replacement_rules", None)
    no_separator_normalization = kwargs.get("no_separator_normalization", False)

    command = ["UnitexTool", "Normalize"]

    if no_carriage_return is True:
        command.append("--no_carriage_return")

    if input_offsets is not None:
        command.append("--input_offsets=%s" % input_offsets)
    if output_offsets is not None:
        command.append("--output_offsets=%s" % output_offsets)

    if replacement_rules is not None:
        command.append("--replacement_rules=%s" % replacement_rules)

    if no_separator_normalization is True:
        command.append("--no_separator_normalization")

    command.append(text)

    command = " ".join(command)

    LOGGER.info("Normalizing text '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def sort_txt(*args, **kwargs):
    """This function carries out a lexicographical sorting of the lines of file <txt>. <txt>
    represents the complete path of the file to be sorted.

    The input text file is modified. By default, the sorting is performed in the order of
    Unicode characters, removing duplicate lines.

    Arguments (length: 1):
        0 -- The text file to sort

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
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one text to normalize...")
    text = args[0]

    duplicates = kwargs.get("duplicates", False)
    reverse = kwargs.get("reverse", False)

    sort_order = kwargs.get("sort_order", None)
    if sort_order is None:
        raise UnitexException("You must provide the sort_order argument...")

    line_info = kwargs.get("line_info", None)
    thai = kwargs.get("thai", False)
    factorize_inflectional_codes = kwargs.get("factorize_inflectional_codes", False)

    command = ["UnitexTool", "SortTxt"]

    if duplicates is False:
        command.append("--no_duplicates")
    else:
        command.append("--duplicates")

    if reverse is True:
        command.append("--reverse")
    if sort_order is None:
        command.append("--sort_order=%s" % sort_order)
    if line_info is None:
        command.append("--line_info=%s" % line_info)
    if thai is True:
        command.append("--thai")
    if factorize_inflectional_codes is True:
        command.append("--factorize_inflectional_codes")

    command.append(text)

    command = " ".join(command)

    LOGGER.info("Sorting file '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret



def tokenize(*args, **kwargs):
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

    Arguments (length: 1):
        0 -- The text file to tokenize (snt format)

    Keyword arguments:
      - Generic options:
            alphabet [str]      -- alphabet file
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
    """

    if len(args) != 1:
        raise UnitexException("You must specify one and only one text to normalize...")
    text = args[0]

    alphabet = kwargs.get("alphabet", None)
    if alphabet is None:
        raise UnitexException("You must specify the alphabet file path...")

    char_by_char = kwargs.get("char_by_char", False)
    tokens = kwargs.get("tokens", None)

    input_offsets = kwargs.get("input_offsets", None)
    output_offsets = kwargs.get("output_offsets", None)
    if input_offsets is None and output_offsets is not None:
        raise UnitexException("You must provide both input and output offsets...")
    if input_offsets is not None and output_offsets is None:
        raise UnitexException("You must provide both input and output offsets...")

    command = ["UnitexTool", "Tokenize"]

    command.append("--alphabet=%s" % alphabet)

    if char_by_char is True:
        command.append("--char_by_char")
    else:
        command.append("--word_by_word")

    if tokens is not None:
        command.append("--tokens=%s" % tokens)

    if input_offsets is not None:
        command.append("--input_offsets=%s" % input_offsets)
    if output_offsets is not None:
        command.append("--output_offsets=%s" % output_offsets)

    command.append(text)

    command = " ".join(command)

    LOGGER.info("Tokenizing file '%s'..." % text)
    LOGGER.debug("Command: %s", command)
    ret = LIBUNITEX.UnitexTool_public_run_string(bytes(str(command), "utf-8"))

    return ret
