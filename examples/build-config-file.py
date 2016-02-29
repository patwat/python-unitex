#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import yaml

from io import open



def load_dictionaries(directory):
    dictionaries = []

    dela_directory = os.path.join(directory, "Dela")
    if os.path.exists(dela_directory) is False:
        sys.stdout.write("'Dela' directory '%s' doesn't exist.\n")
        return dictionaries

    system_dic_file = os.path.join(directory, "system_dic.def")
    if os.path.exists(system_dic_file) is False:
        sys.stdout.write("'system_dic.def' file not found. Load the entire 'Dela' directory.\n")

        for root, dir, files in os.walk(dela_directory):
            for f in files:
                f = os.path.join(dela_directory, f)
                filename, extension = os.path.splitext(f)

                if extension != ".bin":
                    continue
                elif os.path.exists("%s.inf" % filename) is False:
                    sys.stdout.write("'inf' file doesn't exist for '%s'. Skipping...\n")
                    continue

                dictionaries.append(f)

    else:
        with open(system_dic_file, "r") as f:
            line = f.readline()
            while line:
                line = line.rstrip()
                if not line:
                    line = f.readline()
                    continue

                dictionary = os.path.join(dela_directory, line)
                if os.path.exists(dictionary) is False:
                    sys.stdout.write("Dictionary '%s' doesn't exist. Skipping...\n" % dictionary)

                    line = f.readline()
                    continue
                dictionaries.append(dictionary)

                line = f.readline()

    return dictionaries



def load_preprocessing_fsts(directory):
    sentence = None
    replace = None

    preprocessing_directory = os.path.join(directory, "Graphs/Preprocessing")

    sentence = os.path.join(preprocessing_directory, "Sentence/Sentence.fst2")
    if os.path.exists(sentence) is False:
        sys.stdout.write("'Sentence.fst2' doesn't exist.\n")
        sentence = None

    replace = os.path.join(preprocessing_directory, "Replace/Replace.fst2")
    if os.path.exists(replace) is False:
        sys.stdout.write("'Replace.fst2' doesn't exist.\n")
        replace = None

    return sentence, replace



def load_alphabets(directory):
    alphabet = None
    alphabet_sorted = None

    alphabet = os.path.join(directory, "Alphabet.txt")
    if os.path.exists(alphabet) is False:
        sys.stdout.write("'Alphabet.txt' doesn't exist.\n")
        alphabet = None

    alphabet_sorted = os.path.join(directory, "Alphabet_sort.txt")
    if os.path.exists(alphabet_sorted) is False:
        sys.stdout.write("'Alphabet_sort.txt' doesn't exist.\n")
        alphabet_sorted = None

    return alphabet, alphabet_sorted



if __name__ == "__main__":
    def usage():
        sys.stderr.write("Build Config File -- build the (default) config file for a given language\n\n")
        sys.stderr.write("  $ build-config-file [OPTIONS] <Unitex YAML config template>\n\n")
        sys.stderr.write("Options:\n")
        sys.stderr.write("  [ -h, --help      = this help message                                      ]\n")
        sys.stderr.write("    -o, --output    = the resulting config filename\n")
        sys.stderr.write("    -l, --language  = the language name\n")
        sys.stderr.write("    -d, --directory = the original resources directory for the language\n")
        sys.stderr.write("                      (i.e. the language directory from Unitex distribution)\n\n")
        sys.stderr.write("Example:\n")
        sys.stderr.write("  $ build-config-file -l fr -d /path/to/French -o unitex-fr.yaml unitex.yaml\n")
        sys.exit(1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:l:d:", ["help", "output=", "language=", "directory="])
    except getopt.GetoptError:
        usage()

    if len(opts) == 0 and len(args) == 0:
        usage()

    output = None
    language = None
    directory = None

    for o, a in opts :
        if o == "-h" or o == "--help":
            usage()
        elif o == "-o" or o == "--output":
            output = a
        elif o == "-l" or o == "--language":
            language = a
        elif o == "-d" or o == "--directory":
            directory = a
        else:
            sys.stderr.write("Wrong option '%s'.\n" % o)
            usage()

    if output is None:
        sys.stderr.write("You must provide the resulting config filename.\n")
        usage()

    if language is None:
        sys.stderr.write("You must provide the language name.\n")
        usage()

    if directory is None:
        sys.stderr.write("You must provide the language directory.\n")
        usage()
    directory = os.path.abspath(directory)

    if len(args) != 1:
        sys.stderr.write("You must provide one and only one config template.\n")
        usage()
    [template] = args

    options = None
    with open(template, "r") as f:
        options = yaml.load(f)

    dictionaries = load_dictionaries(directory)
    sentence, replace = load_preprocessing_fsts(directory)
    alphabet, alphabet_sorted = load_alphabets(directory)

    options["resources"]["language"] = language
    options["resources"]["dictionaries"] = dictionaries
    options["resources"]["sentence"] = sentence
    options["resources"]["replace"] = replace
    options["resources"]["alphabet"] = alphabet
    options["resources"]["alphabet-sorted"] = alphabet_sorted

    with open(output, 'w') as f:
        f.write(yaml.dump(options, encoding="utf-8" default_flow_style=False))
