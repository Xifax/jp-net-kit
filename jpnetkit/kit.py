#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jpnetkit.jdic import JDic
from jpnetkit.kradfile import Kradfile
from jpnetkit.mecab import MeCab
from jpnetkit.weblio import Weblio
from jpnetkit.wordnet import Wordnet


class Kit:

    """Wrapper for included services"""

    def __init__(self):
        """Initialize all services"""
        self.jdic, self.krad, self.mecab, self.weblio, self.wordnet =\
            JDic(), Kradfile(), MeCab(), Weblio(), Wordnet()

    def get_reading(self, term):
        """Get reading for kanji|word|sentence"""
        return self.mecab.get_reading(term)

    def get_radikals(self, kanji):
        """Get radikal decomposition for kanji"""
        return self.kradfile.get_radikals_for(kanji)

    def translate(self, term):
        """Translate sentence word by word to english"""
        return self.jdic.lookup(term)

    def compelete(self, term):
        """Autocomplete kanji|word"""
        return self.wordnet.complete(term)

    def get_examples(self, word):
        """Get example usages with english translation for word"""
        return self.weblio.examples(word)

    def get(self, term, *args):
        """Get multiple or one item for term:
            * reading
            * radikals
            * translation
            * completion
            * examples

        e.g.:
            >> get(u'テスト', 'reading', 'translation', 'examples')

        Will return dictionary with reading, translation and examples.
        If only one result is specified, will return it without dictionary.

        NB: If many items are specified may take a while!
        """
        results = {}
        for arg in args:
            if 'reading' == arg:
                results[arg] = self.get_reading(term)
            if 'radikals' == arg:
                results[arg] = self.get_radikals(term)
            if 'translation' == arg:
                results[arg] = self.translate(term)
            if 'completion' == arg:
                results[arg] = self.compelete(term)
            if 'examples' == arg:
                results[arg] = self.get_examples(term)

        if len(results) == 1:
            return results.itervalues().next()

        return results
