#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import yaml

from unitex import init_log_system
from unitex.config import UnitexConfig
from unitex.tools import *
from unitex.resources import *
from unitex.io import *



def load_resources(options):
    if options["resources"]["alphabet"] is not None:
        alphabet = load_persistent_alphabet(options["resources"]["alphabet"])
        options["resources"]["alphabet"] = alphabet
    
    if options["resources"]["alphabet-sorted"] is not None:
        alphabet_sorted = load_persistent_alphabet(options["resources"]["alphabet-sorted"])
        options["resources"]["alphabet-sorted"] = alphabet_sorted
    
    if options["resources"]["sentence"] is not None:
        sentence = load_persistent_fst2(options["resources"]["sentence"])
        options["resources"]["sentence"] = sentence
    
    if options["resources"]["replace"] is not None:
        replace = load_persistent_fst2(options["resources"]["replace"])
        options["resources"]["replace"] = replace
    
    if options["resources"]["dictionaries"] is not None:
        dictionaries = []
    
        for dictionary in options["resources"]["dictionaries"]:
            dictionary = load_persistent_dictionary(dictionary)
            dictionaries.append(dictionary)
    
        options["resources"]["dictionaries"] = dictionaries



def free_resources(options):
    if options["resources"]["alphabet"] is not None:
        free_persistent_alphabet(options["resources"]["alphabet"])
    
    if options["resources"]["alphabet-sorted"] is not None:
        free_persistent_alphabet(options["resources"]["alphabet-sorted"])
    
    if options["resources"]["sentence"] is not None:
        free_persistent_fst2(options["resources"]["sentence"])
    
    if options["resources"]["replace"] is not None:
        free_persistent_fst2(options["resources"]["replace"])
    
    if options["resources"]["dictionaries"] is not None:
        for dictionary in options["resources"]["dictionaries"]:
            free_persistent_dictionary(dictionary)



def execute(path, grammar, options):
    directory, filename = os.path.split(path)
    name, extension = os.path.splitext(filename)

    txt = path
    snt = os.path.join(directory, "%s.snt" % name)
    dir = os.path.join(directory, "%s_snt" % name)

    # Set up the virtual filesystem
    if options["virtualization"] is True:
        _txt = "%s%s" % (UnitexConstants.VFS_PREFIX, txt)
        cp(txt, _txt)
        
        txt = _txt
        snt = "%s%s" % (UnitexConstants.VFS_PREFIX, snt)
    else:
        if os.path.exists(dir) is False:
            mkdir(dir)

    # Some ad-hoc check
    alphabet = options["resources"]["alphabet"]
    if alphabet is None:
        sys.stderr.write("[ERROR] You must provide the alphabet. Fix the configuration file.\n")
        sys.exit(1)

    alphabet_sorted = options["resources"]["alphabet-sorted"]
    if alphabet_sorted is None:
        sys.stderr.write("[ERROR] You must provide the sorted alphabet. Fix the configuration file.\n")
        sys.exit(1)

    # Normalize the text
    kwargs = options["tools"]["normalize"]
    
    ret = normalize(txt, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Text normalization failed!\n")
        sys.exit(1)

    # Apply Sentence.fst2
    sentence = options["resources"]["sentence"]
    if sentence is not None:
        kwargs = {}
        kwargs["start_on_space"] = options["tools"]["fst2txt"]["start_on_space"]
        kwargs["char_by_char"] = options["tools"]["fst2txt"]["char_by_char"]
        kwargs["merge"] = True
        
        ret = fst2txt(sentence, snt, alphabet, **kwargs)
        if ret is False:
            sys.stderr.write("Text segmentation failed!\n")
            sys.exit(1)

    # Apply Replace.fst2
    replace = options["resources"]["replace"]
    if replace is not None:
        kwargs = {}
        kwargs["start_on_space"] = options["tools"]["fst2txt"]["start_on_space"]
        kwargs["char_by_char"] = options["tools"]["fst2txt"]["char_by_char"]
        kwargs["merge"] = False
        
        ret = fst2txt(replace, snt, alphabet, **kwargs)
        if ret is False:
            sys.stderr.write("Replace grammar application failed!\n")
            sys.exit(1)

    # Tokenize the text
    kwargs = options["tools"]["tokenize"]
    
    ret = tokenize(snt, alphabet, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Text tokenization failed!\n")
        sys.exit(1)

    # Apply dictionaries
    if options["resources"]["dictionaries"] is not None:
        dictionaries = options["resources"]["dictionaries"]
        kwargs = options["tools"]["dico"]

        ret = dico(dictionaries, snt, alphabet, **kwargs)
        if ret is False:
            sys.stderr.write("[ERROR] Dictionaries application failed!\n")
            sys.exit(1)

    # Locate pattern
    kwargs = options["tools"]["locate"]
    
    ret = locate(grammar, snt, alphabet, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Locate failed!\n")
        sys.exit(1)

    index = os.path.join(dir, "concord.ind")
    if options["virtualization"] is True:
        index = "%s%s" % (UnitexConstants.VFS_PREFIX, index)

    if exists(index) is False:
        sys.stderr.write("[ERROR] Locate failed! No index produced.\n")
        sys.exit(1)

    # Build concordance
    kwargs = options["tools"]["concord"]

    format = kwargs["format"]
    if format not in (UnitexConstants.FORMAT_HTML,
                      UnitexConstants.FORMAT_TEXT,
                      UnitexConstants.FORMAT_GLOSSANET,
                      UnitexConstants.FORMAT_SCRIPT,
                      UnitexConstants.FORMAT_XML,
                      UnitexConstants.FORMAT_XML_WITH_HEADERS):
        sys.stderr.write("[ERROR] This little script supports a limited list of concordance format:\n")
        sys.stderr.write("[ERROR]    - TEXT ('text' option)\n")
        sys.stderr.write("[ERROR]    - HTML ('html', 'glossanet' and 'script' options)\n")
        sys.stderr.write("[ERROR]    - XML ('xml' and 'wml-with-headers' options)\n")
        sys.exit(1)
    
    ret = concord(index, alphabet_sorted, **kwargs)
    if ret is False:
        sys.stderr.write("[ERROR] Concord failed!\n")
        sys.exit(1)

    concordances = None
    output = None

    if format == UnitexConstants.FORMAT_TEXT:
        concordances = os.path.join(dir, "concord.txt")
        output = os.path.join(directory, "%s-concordances.txt" % name)
    elif format in (UnitexConstants.FORMAT_HTML, UnitexConstants.FORMAT_GLOSSANET, UnitexConstants.FORMAT_SCRIPT):
        concordances = os.path.join(dir, "concord.html")
        output = os.path.join(directory, "%s-concordances.html" % name)
    elif format in (UnitexConstants.FORMAT_XML, UnitexConstants.FORMAT_XML_WITH_HEADERS):
        concordances = os.path.join(dir, "concord.xml")
        output = os.path.join(directory, "%s-concordances.xml" % name)

    if options["virtualization"] is True:
        concordances = "%s%s" % (UnitexConstants.VFS_PREFIX, concordances)
    mv(concordances, output)

    # Clean the Unitex files
    if options["debug"] is False:
        if options["virtualization"] is True:
            for vf in ls("%s%s" % (UnitexConstants.VFS_PREFIX, directory)):
                rm(vf)
            rm(snt)
            rm(txt)
        else:
            rmdir(dir)
            rm(snt)

    return output



if __name__ == "__main__":
    def usage():
        sys.stderr.write("Do Concord -- A simple script to illustrate the Unitex Python bindings\n\n")
        sys.stderr.write("  $ do-concord [OPTIONS] <file1(, file2, ...)>\n\n")
        sys.stderr.write("Options:\n")
        sys.stderr.write("  [ -h, --help    = this help message       ]\n")
        sys.stderr.write("    -c, --config  = the Unitex config file\n")
        sys.stderr.write("    -g, --grammar = the fst2 grammar to use\n\n")
        sys.stderr.write("Example:\n")
        sys.stderr.write("  $ do-concord -c unitex.yaml -g grammar.fst2 *.txt\n")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:g:", ["help", "config=", "grammar="])
    except getopt.GetoptError:
        usage()

    if len(opts) == 0 and len(args) == 0:
        usage()

    config_file = None
    grammar = None

    for o, a in opts :
        if o == "-h" or o == "--help":
            usage()
        elif o == "-c" or o == "--config":
            config_file = a
        elif o == "-g" or o == "--grammar":
            grammar = a
        else:
            sys.stderr.write("Wrong option '%s'.\n" % o)
            usage()

    if config_file is None:
        sys.stderr.write("You must provide the config file.\n")
        usage()

    if grammar is None:
        sys.stderr.write("You must provide the grammar.\n")
        usage()

    if not args:
        sys.stderr.write("You must provide at least one file to process.\n")
        usage()

    # 'glob' is bad! Do not use 'glob'.
    files = []
    for arg in args:
        if os.path.isdir(arg) is True:
            for root, dir, _files in os.walk(arg):
                files += [os.path.join(root, f) for f in _files]
        elif os.path.isfile(arg) is True:
            files.append(arg)
        else:
            sys.stderr.write("The arguments must be files or directories.\n")
            usage()

    # Configuration file loading
    config = None
    with open(config_file, "r") as f:
        config = yaml.load(f)
    options = UnitexConfig(config)

    # Intialization of the basic logging system
    init_log_system(options["verbose"], options["debug"], options["log"])

    # Load resources in the persistent space
    if options["persistence"] is True:
        grammar = load_persistent_fst2(grammar)
        load_resources(options)

    results = []

    for f in files:
        sys.stdout.write("Processing '%s'...\n" % f)

        # This function illustrate the whole Unitex process used in order
        # to produce a concordance file.
        result = execute(f, grammar, options)
        sys.stdout.write("   -> %s\n" % result)

        results.append(result)

    # Free resources from the persistent space
    if options["persistence"] is True:
        free_persistent_fst2(grammar)
        free_resources(options)
