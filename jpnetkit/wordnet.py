#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get, RequestException


class Wordnet:

    """
        Asian Wordnet API consumer
        http://ja.asianwordnet.org/services/provide_list
        NB: service has quota!
    """

    def __init__(self):
        """Setup request url and default request options"""
        # Base API url
        self.base = 'http://ja.asianwordnet.org/services/%s/json/'
        # Available services
        self.services = {
            'dictionary':       'ja2en/%s',         # word
            'autocomplete':     'ja/%s',            # incomplete term
            'browse':           'ja/%s',            # word
            'browse_related':   'ja/%s/%s/%s/%s',   # word, synset offset, relation
            'sense':            '%s/%s',            # pos, synset offset
        }
        # Semantic relations
        self.relations = [
            'ANTONYM',
            # denotes a more specific term, a subordinate grouping
            # "dog" is hyponym of "animal"
            'HYPONYM',
            # denotes superordinate term
            # "musical instrument" is a hypernym of "guitar"
            'HYPERNYM',
            # denotes a whole, whose part is denoted by another term
            # "word" is a holonym of "letter"
            'HOLONYM',
            # denotes a part of the whole, that is denoted by another term
            # "arm" is a meronym of "body"
            'MERONYM',
        ]
        # Parts of speech
        self.pos = {
            'noun':      'n',
            'verb':      'v',
            'adjective': 'a',
            'adverb':    'r',
            's':         's',  # what is this, I don't know
        }

    def query(self, service, params):
        """
        Query specified Wordnet service with provided params.
        """
        try:
            return get(
                self.base % service + self.services[service] % params
            ).json()
        except RequestException:
            return None

    def lookup(self, word):
        """
        Query Wordnet to lookup specific word.
        Resulting list will be sorted by provided priority ranks (row numbers).
        NB: may not find kanji by themselves!

        TODO: include specific fields to get (e.g., lookup gloss and so on)

        Each word contains following fields:
            'gloss'     : english translation
            'translate' : similar words in japanese
            'words'     : related words in english
            'ss_type'   : part of speech
        Additional fields are provided to use advanced wordnet features:
            'lex_filename'  : thematic category
            'synset_offset' : semantic key
        """
        # query dictionary service with provided word as an argument
        results = self.query('dictionary', word)
        # found something
        if self.valid(results):
            # return list of words, sorted by row number
            return list(zip(*sorted(
                (int(row), word) for row, word
                in results['data'].iteritems()
            )).pop())
        # otherwise return empty list
        else:
            return []

    def complete(self, term):
        """
        Get autocomplete suggestions list for partial word.
        Resulting list will be sorted by provided priority ranks (row numbers).
        NB: will find no more than 50 matching items, starting with term.
        """
        # query autocomplete service with provided term as an argument
        results = self.query('autocomplete', term)
        # if found anything
        if self.valid(results):
            # sort items in 'data' as list of int(row), lemma;
            # then unzip resulting list of tuples into list of lemmas
            # of length 2 and more
            return [item['lemma'] for item
                    in zip(*sorted(
                        (int(row), lemma) for row, lemma
                        in results['data'].iteritems()
                    )).pop()
                    if len(item['lemma']) > 1]
        # otherwise return empty list
        else:
            return []

    def browse(self, word):
        """
        List related words.
        """
        results = self.query('browse', word)
        if 'data' in results:
            return results

    def antonyms(self, word):
        """
        Get antonyms for word
        """
        # 1. find word, get its semantic key and pos
        # 2. query browse_related to with semantic relation of ANTONYM
        pass

    def valid(self, results):
        """
        Check if Wordnet response is valid.
        """
        if results:
            if 'data' in results and 'rows' in results:
                if results['rows'] > 0:
                    return True
