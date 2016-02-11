#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

from unitex import UnitexException, LOGGER



class UnitexSettings:

    def __init__(self):
        raise NotImplementedError

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def load(self, f):
        raise NotImplementedError

