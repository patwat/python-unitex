#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import re

from unitex import UnitexException, UnitexConstants

_LOGGER = logging.getLogger(__name__)

BRACKETED_ENTRY = re.compile(r"{([^}]*)}")



class Tag(object):

    def __init__(self):
        self.__pos = ""

        self.__features = []
        self.__flexions = []

    def __str__(self):
        tag = self.get()
        tag = tag.encode(UnitexConstants.DEFAULT_ENCODING)
        return tag

    def __unicode__(self):
        return u"%s" % self.get()

    def load(self, tag):
        self.__pos = ""

        self.__features = []
        self.__flexions = []

        i = 0

        pos = ""
        while i < len(tag) and tag[i] != '+' and tag[i] != ':':
            pos = pos + tag[i]
            i += 1

        self.set_pos(pos)

        while i < len(tag) and tag[i] == '+':
            sign = tag[i]

            i += 1

            tmp = ""
            while i < len(tag) and tag[i] != '+' and tag[i] != ':':
                tmp = tmp + tag[i]
                i += 1

            if tmp:
                self.add_feature(tmp)

        while i < len(tag) and tag[i] == ':':
            sign = tag[i]

            i += 1

            tmp = ""
            while i < len(tag) and tag[i] != ':':
                tmp = tmp + tag[i]
                i += 1

            if tmp:
                self.add_flexion(tmp)

    def get(self):
        tag = self.get_pos()

        features = "+".join(self.get_features())
        if features:
            tag += "+%s" % features

        flexions = "".join(self.get_flexions())
        if flexions:
            tag += ":%s" % flexions

        return tag

    def set_pos(self, pos):
        self.__pos = pos

    def get_pos(self):
        return self.__pos

    def set_features(self, features):
        self.__features = features

    def get_features(self):
        return self.__features

    def add_feature(self, feature):
        self.__features.append(feature)

    def set_flexions(self, flexions):
        self.__flexions = flexions

    def get_flexions(self):
        return self.__flexions

    def add_flexion(self, flexion):
        self.__flexions.append(flexion)



class Entry(Tag):

    def __init__(self):
        super(Entry, self).__init__()

        self.__form = ""
        self.__lemma = ""

    def __str__(self):
        entry = self.get()
        entry = entry.encode(UnitexConstants.DEFAULT_ENCODING)
        return entry

    def __unicode(self):
        return u"%s" % self.get()

    def load(self, entry, bracketed=False):
        if bracketed is True:
            entry = BRACKETED_ENTRY.sub(r"\1", entry)
        i = 0

        escaped = False

        form = ""
        try:
            while True:

                if entry[i] == "," and escaped is False:
                    i += 1
                    break

                elif entry[i] == "\\":
                    if escaped is True:
                        form += entry[i]
                        escaped = False
                    else:
                        escaped = True

                else:
                    form += entry[i]
                    escaped = False

                i += 1
        except IndexError:
            raise UnitexException("Invalid entry format '%s'. No comma found." % entry)

        self.set_form(form)

        escaped = False

        lemma = ""
        try:
            while True:

                if entry[i] == "." and escaped is False:
                    i += 1
                    break

                elif entry[i] == "\\":
                    if escaped is True:
                        lemma += entry[i]
                        escaped = False
                    else:
                        escaped = True

                else:
                    lemma += entry[i]
                    escaped = False

                i += 1
        except IndexError:
            raise UnitexException("Invalid entry format '%s'. No dot found." % entry)

        self.set_lemma(lemma)

        Tag.load(self, entry[i:])

    def get(self, bracketed=False):
        form = self.get_form(escape=True)

        lemma = self.get_lemma(escape=True)
        if not lemma:
            lemma = form

        tag = Tag.get(self)

        if bracketed is True:
            return "{%s,%s.%s}" % (form, lemma, tag)
        else:
            return "%s,%s.%s" % (form, lemma, tag)

    def set_form(self, form):
        self.__form = form

    def get_form(self, escape=False):
        if escape is False:
            return self.__form
        return self.__form.replace(",", "\,")

    def set_lemma(self, lemma):
        self.__lemma = lemma

    def get_lemma(self, escape=False):
        if escape is False:
            return self.__lemma
        return self.__lemma.replace(",", "\,")
