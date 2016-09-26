#!/usr/bin/env python
# -*- coding: utf-8 -*-

import array
import logging
import re
import struct

from builtins import chr
from io import open

from unitex import UnitexException, UnitexConstants
from unitex.utils.fsa import FSAConstants, Automaton
from unitex.utils.types import BRACKETED_ENTRY, Tag, Entry

_LOGGER = logging.getLogger(__name__)



class CompressedEntry(Entry):

    SEPARATORS = (" ", "-")
    SPLITTER = re.compile("([-\s])")

    def __init__(self):
        super(CompressedEntry, self).__init__()

    def compute(self, lemma, form):
        n, i = "", 0

        while i < len(lemma) and lemma[i].isdigit():
            n = n + lemma[i]
            i = i + 1

        if i > 0:
            prefix = form[:len(form)-int(n)]
        else:
            prefix = form

        suffix = lemma[i:]

        return "%s%s" % (prefix, suffix)

    def uncompress(self, lemma):
        form = self.get_form()
        if not lemma:
            return form

        # If two words don't have de same number of elements
        # the compressed lemma is preceded by '_'
        if lemma[0] == '_':
            return self.compute(lemma[1:], form)

        wtab = self.SPLITTER.split(form)
        ltab = self.SPLITTER.split(lemma)

        l = []
        for i in range(len(ltab)):
            if not ltab[i]:
                continue
            elif ltab[i] in self.SEPARATORS:
                l.append(ltab[i])
            else:
                l.append(self.compute(ltab[i], wtab[i]))

        return "".join(l)

    def load(self, form, data, lemmatize=True):
        data = data.rstrip()

        self.set_form(form)
        lemma = ""

        i = 0

        lemma, escaped = "", False
        try:
            while True:
                if data[i] == "." and escaped is False:
                    break
                elif data[i] == "\\":
                    if escaped is True:
                        lemma += data[i]
                        escaped = False
                    else:
                        lemma += data[i]
                        escaped = True
                else:
                    lemma += data[i]
                    escaped = False
                i += 1
        except IndexError:
            raise UnitexException("Wrong lemma for entry '%s' ..." % data)

        if lemmatize is True:
            self.set_lemma(self.uncompress(lemma))

        Tag.load(self, data[i+1:])



class OldCompressedDictionary:

    INITIAL_STATE_OFFSET=4
    INF_SEPARATOR=re.compile(r"(?<![\\]),")

    def __init__(self):
        self.__bin = None
        self.__inf = None

        self.__buffer = None

    def lookup(self, token, i=None, pos=None):
        if i is None:
            i = 0

        if pos is None:
            pos = self.INITIAL_STATE_OFFSET
        tnbr = self.__bin[pos] * 256 + self.__bin[pos+1]
        pos = pos + 2

        _LOGGER.debug("Lookup Start: token[%s|%s] -- pos(%s) -- tnbr(%s)\n" % (token[:i], token[i:], pos, tnbr))

        if i == len(token):
            data = []

            _LOGGER.debug("   Check Final State: pos(%s) -- tnbr(%s)\n" % (pos, tnbr))
            if not (tnbr & 32768):
                _LOGGER.debug("      -> Final\n")
                index = self.__bin[pos] * 256 * 256 + self.__bin[pos+1] * 256 + self.__bin[pos+2]

                for inf in self.INF_SEPARATOR.split(self.__inf[index]):
                    E = CompressedEntry()
                    E.load(token, inf)

                    data.append(E)
            else:
                _LOGGER.debug("      -> Not final\n")

            return data, pos-2
        elif tnbr & 32768:
            tnbr = tnbr - 32768
        else:
            pos = pos + 3

        for j in range(tnbr):
            char = chr(self.__bin[pos] * 256 + self.__bin[pos+1])
            _LOGGER.debug("   Matching char[%s] -- pos(%s) -> current[%s]\n" % (token[i], pos, char))

            pos = pos + 2

            offset = self.__bin[pos] * 256 * 256 + self.__bin[pos+1] * 256 + self.__bin[pos+2]
            pos = pos + 3

            if char == token[i]:
                _LOGGER.debug("      -> Char found\n")
                return self.lookup(token, i+1, offset)

            # WEIRD... Objective: handle whitespaces in MWU dictionaries for the match function
            #               -> ["Conseil", "d'", "administration"] == "Conseil d'administration"
            elif char == u" " and i == 0:
                _LOGGER.debug("   -> Char is whitespace [pass]\n")
                return self.lookup(token, i, offset)

        return None, pos

    def find(self, token):
        entries, pos = self.lookup(token)
        return entries

    def match(self, sequence, i=None, mode=None, separator=None):
        if i is None:
            i = 0

        if mode is None:
            mode = UnitexConstants.MATCH_MODE_LONGEST
        elif mode not in [UnitexConstants.MATCH_MODE_LONGEST,\
                          UnitexConstants.MATCH_MODE_SHORTEST,\
                          UnitexConstants.MATCH_MODE_ALL]:
            raise UnitexException("Wrong match mode: %s ..." % mode)

        matches = []

        buffer, pos, tnbr = [], None, None
        for j in range(i, len(sequence)):
            _LOGGER.debug("Match Token: '%s'\n" % sequence[j])

            entries, pos = self.lookup(sequence[j], pos=pos)
            if entries is None:
                _LOGGER.debug("   -> No entry found ...\n")
                break
            _LOGGER.debug("   -> Entries found: pos[%s] -- tnbr[%s]\n" % (pos, tnbr))

            buffer.append(j)

            if entries:
                matches.append((entries, buffer[:]))
                if mode == UnitexConstants.MATCH_MODE_SHORTEST:
                    return matches

            if separator is not None:
                _LOGGER.debug("Match Separator: '%s'\n" % separator)
                entries, pos = self.lookup(separator, pos=pos)
                if entries is None:
                    _LOGGER.debug("   -> No separator found ...\n")
                    break
                _LOGGER.debug("   -> Separator found\n")

        if not matches:
            return None
        elif mode == UnitexConstants.MATCH_MODE_LONGEST:
            return [matches[-1]]
        elif mode == UnitexConstants.MATCH_MODE_ALL:
            return matches

    def dump(self, pos=None):
        if pos is None:
            pos = self.INITIAL_STATE_OFFSET
            self.__buffer = []

        tnbr = self.__bin[pos] * 256 + self.__bin[pos+1]
        pos = pos + 2

        if not (tnbr & 32768):
            index = self.__bin[pos] * 256 * 256 + self.__bin[pos+1] * 256 + self.__bin[pos+2]

            form = "".join(self.__buffer)

            for inf in self.INF_SEPARATOR.split(self.__inf[index]):
                E = CompressedEntry()
                E.load(form, inf)
                yield E

            pos = pos + 3

        else:
            tnbr = tnbr - 32768

        for j in range(tnbr):
            self.__buffer.append(chr(self.__bin[pos] * 256 + self.__bin[pos+1]))
            pos = pos + 2

            offset = self.__bin[pos] * 256 * 256 + self.__bin[pos+1] * 256 + self.__bin[pos+2]
            pos = pos + 3

            for E in self.dump(offset):
                yield E

        if self.__buffer:
            self.__buffer.pop()

    def load(self, bin, inf, encoding=None):
        if encoding is None:
            encoding = UnitexConstants.DEFAULT_ENCODING
        INF = open(inf, "r", encoding=encoding)

        self.__inf = INF.readlines()
        self.__inf.pop(0) # Remove number information

        INF.close()

        BIN = open(bin, "r+b")

        a = struct.unpack('B', BIN.read(1))[0]
        b = struct.unpack('B', BIN.read(1))[0]
        c = struct.unpack('B', BIN.read(1))[0]
        d = struct.unpack('B', BIN.read(1))[0]
        size = d + (256*c) + (256*256*b) + (256*256*256*a)

        BIN.close()

        BIN = open(bin, "rb")

        self.__bin = array.array('B')

        byte = BIN.read(1)
        while byte:
            tmp = struct.unpack('B', byte)[0]

            self.__bin.append(tmp)

            byte = BIN.read(1)

        BIN.close()



class CompressedDictionary(OldCompressedDictionary):

    def __init__(self):
        super(CompressedDictionary, self).__init__()
        raise NotImplementedError



class GRF(Automaton):

    def __init__(self, name="GRF"):
        super(GRF, self).__init__(name)

    def load(self, file, encoding=None):
        if encoding is None:
            encoding = UnitexConstants.DEFAULT_ENCODING
        raise NotImplementedError

    def save(self, file, encoding=None):
        if encoding is None:
            encoding = UnitexConstants.DEFAULT_ENCODING

        X = 1000
        Y = 1000
        GAP = 20

        transitions = []
        transitions.append({"label": FSAConstants.EPSILON, "targets": set([])})
        transitions.append({"label": "", "targets": set([])})

        nmap = {}
        root = []

        for edge, sid, tid in self.iter("dfs"):
            source = self[sid]
            target = self[tid]

            index = 0

            key = (str(edge), tid)
            if key in nmap:
                index = nmap[key]
            else:
                index = len(transitions)
                nmap[key] = index
                transitions.append({"label": str(edge), "targets": set([])})

            if sid == self.get_initial():
                transitions[0]["targets"].add(str(index))
            if target.is_final() is True:
                transitions[index]["targets"].add("1")

            for _edge in target:
                for _target in target[_edge]:
                    _index = 0

                    _key = (str(_edge), _target.get_id())
                    if _key in nmap:
                        _index = nmap[_key]
                    else:
                        _index = len(transitions)
                        nmap[_key] = _index
                        transitions.append({"label": str(_edge), "targets": set([])})

                    transitions[index]["targets"].add(str(_index))

        with open(file, "w", encoding=encoding) as output:
            output.write("#Unigraph\r\n")
            output.write("SIZE %s %s\r\n" % (X+GAP, Y+GAP))
            output.write("FONT Times New Roman:B 10\r\n")
            output.write("OFONT Monospaced:B 8\r\n")
            output.write("BCOLOR 16777215\r\n")
            output.write("FCOLOR 0\r\n")
            output.write("ACOLOR 13487565\r\n")
            output.write("SCOLOR 16711680\r\n")
            output.write("CCOLOR 255\r\n")
            output.write("DBOXES y\r\n")
            output.write("DFRAME y\r\n")
            output.write("DDATE y\r\n")
            output.write("DFILE y\r\n")
            output.write("DDIR n\r\n")
            output.write("DRIG n\r\n")
            output.write("DRST n\r\n")
            output.write("FITS 100\r\n")
            output.write("PORIENT L\r\n")
            output.write("#\r\n")
            output.write("%s\r\n" % len(transitions))

            for transition in transitions:
                label = transition["label"]
                size = len(transition["targets"])
                targets = " ".join(list(transition["targets"]))

                if size == 0:
                    output.write('"%s" %s %s %s \r\n' % (label, GAP, GAP, size))
                else:
                    output.write('"%s" %s %s %s %s \r\n' % (label, GAP, GAP, size, targets))



class SentenceFST(Automaton):

    def __init__(self, name="SentenceFST"):
        super(SentenceFST, self).__init__(name)

        self.__sentence = None

        self.__tokens = None
        self.__labels = None

    def get_sentence(self):
        return self.__sentence

    def get_tokens(self):
        return self.__tokens

    def get_token(self, i):
        return self.__tokens[i]

    def get_label(self, i):
        return self.__labels[i]

    def load(self, sentence, tokens, states, labels):
        self.__sentence = sentence

        self.__tokens = []
        self.__labels = {}

        start = 0
        for index, length in tokens:
            end = start + length

            self.__tokens.append(self.__sentence[start:end])
            start = end

        transitions = []

        for i in range(len(states)):
            initial = False
            if i == 0:
                initial = True

            final = False
            if states[i] == "t":
                final = True

            sid = self.add_node(initial=initial, final=final)
            if final is True:
                break

            for lid, tid in states[i]:
                entry = labels[lid][0]

                p1 = labels[lid][1][0][0]
                p2 = labels[lid][1][1][0]

                if p1 not in self.__labels:
                    self.__labels[p1] = []
                self.__labels[p1].append((entry, p2))

                transitions.append((sid, lid, tid))

        for sid, lid, tid in transitions:
            self.add_edge(lid, sid, tid)



class TextFST:

    def __init__(self):
        self.__tfst = None
        self.__tind = None

    def __del__(self):
        self.__tfst.close()

    def __len__(self):
        return len(self.__tind)

    def __getitem__(self, i):
        if i >= len(self):
            raise UnitexException("TextFST index out of range (size: %s)." % len(self))
        position = self.__tind[i]

        self.__tfst.seek(position)

        line = self.__tfst.readline()
        while line:
            line = line.rstrip()

            if line[0] != "$":
                raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

            # The sentence number (format '$n')
            number = int(line[1:])

            line = self.__tfst.readline()
            line = line.rstrip()

            # The text of the sentence
            text = line

            line = self.__tfst.readline()
            line = line.rstrip()

            # The tokens of the text
            #   -> [(x1, y), (x2, y2), ..., (xi, yi)]
            #      where,
            #        - x: token index in file 'tokens.txt'
            #        - y: length of the token (in characters)
            tokens = [tuple(int(t) for t in token.split("/")) for token in line.split(" ")]

            line = self.__tfst.readline()
            line = line.rstrip()

            # The offset of the sentence (from the begining of the text)
            #   -> X_Y
            #      where,
            #        - X: the offset in tokens
            #        - Y: the offset in characters
            offset = tuple(int(o) for o in line.split("_"))

            line = self.__tfst.readline()
            line = line.rstrip()

            states = []
            while line != "t":
                if line[0] != ":":
                    raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

                line = line[1:].strip()
                line = line.split()

                state = []
                for i in range(0, len(line), 2):
                    state.append((int(line[i]), int(line[i+1])))
                states.append(state)

                line = self.__tfst.readline()
                line = line.rstrip()

                if not line:
                    raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

            states.append(line)

            line = self.__tfst.readline()
            line = line.rstrip()

            if line[0] != "f":
                raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

            line = self.__tfst.readline()
            line = line.rstrip()

            tags = []
            while line != "f":
                if line == "@<E>":
                    tags.append(("<E>", None))

                elif line == "@STD":
                    line = self.__tfst.readline()
                    line = line.rstrip()

                    content = line[1:]

                    entry = Entry()

                    if BRACKETED_ENTRY.match(content):
                        content = BRACKETED_ENTRY.sub(r"\1", content)
                        entry.load(content)
                    else:
                        entry.set_form(content)

                    line = self.__tfst.readline()
                    line = line.rstrip()

                    if line[0] != "@":
                        raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

                    position = [tuple(int(i) for i in p.split(".")) for p in line[1:].split("-")]

                    tags.append((entry, position))

                else:
                    raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

                line = self.__tfst.readline()
                line = line.rstrip()

                if line[0] != ".":
                    raise UnitexException("File '%s' is corrupted ..." % self.__tfst.name)

                line = self.__tfst.readline()
                line = line.rstrip()

            _LOGGER.debug("SENTENCE[%s]\n" % number)
            _LOGGER.debug(" - offset: (%s)\n" % ", ".join([str(i) for i in offset]))
            _LOGGER.debug(" - text: %s\n" % text)
            _LOGGER.debug(" - tokens: [%s]\n" % ", ".join([str(t) for t in tokens]))
            _LOGGER.debug(" - states:\n")
            for state in states:
                _LOGGER.debug("   - s: %s\n" % state)
            _LOGGER.debug(" - tags:\n")
            for tag in tags:
                _LOGGER.debug("   - t: (%s)\n" % ", ".join([str(t) for t in tag]))

            S = SentenceFST("SENTENCE[%d]" % number)
            S.load(text, tokens, states, tags)

            return S

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

    def load(self, fst, index, encoding=None):
        if encoding is None:
            encoding = UnitexConstants.DEFAULT_ENCODING

        self.__tfst = open(fst, "r", encoding=encoding)
        self.__tind = []

        with open(index, "rb") as fin:
            i = fin.read(4)
            while i:
                position = struct.unpack("<L", i)
                self.__tind.append(position[0])

                i = fin.read(4)
