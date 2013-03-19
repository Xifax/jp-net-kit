#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get, RequestException
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

    def get_reading(self, sentence, hiragana=True):
        """
        Get reading for provided sentence|word
        NB: for some rare words there may be no readings available!
        """
        info = self.include('pronounciation').parse(sentence)
        if info:
            katakana = u''.join([
                reading.get('pronounciation', '') for reading in info
                if reading.get('pronounciation')
            ])
            if hiragana:
                return kata2hira(katakana)
            return katakana

    def word_by_word(self, sentence, hiragana=True):
        """Get reading for every element in provided sentence"""
        words = []
        info = self.include('pronounciation', 'surface').parse(sentence)
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

    def part_of_speech(self, term):
        """Get term type"""
        info = self.include('pos', 'baseform').parse(term)
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
            return get(
                self.url % (sentence, ','.join(self.options))
            ).json()
        except RequestException:
            return None

    def include(self, *args):
        """
        Include specified option in response
        Options available:
            * 'surface',          : parts of the sentence
            * 'feature',          : inflection, baseform, pos
            * 'pos',              : part of speech
            * 'inflection',       : type and form of inflection
            * 'baseform',         : baseform of the word
            * 'pronounciation'    : word pronounciation
        """
        for option in args:
            if option not in self.options:
                self.options.append(option)
        return self
