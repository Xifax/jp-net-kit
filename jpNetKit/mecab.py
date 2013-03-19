#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    MeCab Web API consumer
"""

import requests
from requests import RequestException
from jcconv import kata2hira


class MeCab:
    """
    Queries MeCab Web API (at chasen.org) and returns sentence|word readings
    """

    def __init__(self):
        """Setup request url and default request options"""
        self.url = ('http://chasen.org/~taku/software/mecapi/mecapi.cgi?'
                    'sentence=%s&response=%s&format=json')
        # NB: nothing is included, by default
        self.options = []
        self.stats = {}

    def reading(self, sentence, hiragana=True):
        """
        Get reading for provided sentence|word
        NB: for some rare words there may be no readings available!
        """
        self.include('pronounciation')
        info = self.parse(sentence)
        if info:
            kana = u''.join([
                reading.get('pronounciation', '') for reading in info
                if reading.get('pronounciation')
            ])
            if hiragana:
                return kata2hira(kana)
            return kana

    def wordByWord(self, sentence, hiragana=True):
        """Get reading for every element in provided sentence"""
        self.includeSurface().includeReading()
        info = self.parse(sentence)
        words = []
        if info:
            # Compile list of {word: reading} excluding okurigana and and so on
            for word in info:
                # No reading
                if not word.get('pronounciation'):
                    reading = u''
                # Word is already in kana
                elif (
                    word.get('pronounciation') == word.get('surface') or
                    kata2hira(word.get('pronounciation')) == word.get('surface')
                ):
                    reading = u''
                # Need to convert to hiragana
                elif hiragana:
                    reading = kata2hira(word.get('pronounciation'))
                # Otherwise, let it be
                else:
                    reading = word.get('pronounciation')
                # Append tuple to word list
                words.append((word.get('surface'), reading))

        return words

    def partOfSpeech(self, term):
        """Get term type"""
        self.includePartOfSpeech()
        self.includeBaseForm()
        info = self.parse(term)
        if info:
            if len(info) == 1:
                # TODO: should really PARSE this stuff, as it gets ugly
                # with all that subitems for all the okurigana
                #reply = info.pop()
                #return reply.get('pos'), reply.get('baseform')
                return info.pop().get('pos')
            else:
                # TODO: should return all the POSes?
                return ''
                #return 'compound'

    def parse(self, sentence):
        """Query MeCab to parse sentence|word"""
        try:
            return requests.get(
                self.url % (sentence, ','.join(self.options))
            ).json
        except RequestException:
            return None

    def include(self, options):
        """Specify, which responce elements should be included"""
        self.options = options

    def includeReading(self):
        """Include reading in response"""
        if 'pronounciation' not in self.options:
            self.options.append('pronounciation')
        return self

    def includeSurface(self):
        """Include surface in response"""
        if 'surface' not in self.options:
            self.options.append('surface')
        return self

    def includeFeature(self):
        """Include feature in response"""
        if 'feature' not in self.options:
            self.options.append('feature')
        return self

    def includePartOfSpeech(self):
        """Include pronounciation in response"""
        if 'pos' not in self.options:
            self.options.append('pos')
        return self

    def includeBaseForm(self):
        """Include baseform in response"""
        if 'baseform' not in self.options:
            self.options.append('baseform')
        return self

    def include(self, option):
        """
        Include specified option in response
        Options available:
            * 'surface',          : parts of the sentence
            * 'feature',          : inflection, baseform, pos
            * 'pos',              : part of speech
            * 'inflection',       : type and form of inflection
            * 'baseform',         : baseform of the word
            * 'pronounciation'    : word pronounciation
        TODO: use kwargs of arguments
        """
        if option not in self.options:
            self.options.append(option)
        return self
