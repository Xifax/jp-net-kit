#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Jisho.org semi-api
"""

import re
from collections import OrderedDict
from itertools import islice

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Jisho:

    def __init__(self):
        self.url = u'http://jisho.org/words?jap=%s&eng=&dict=edict'

    def lookup(self, term):
        """Lookup term on jisho"""
        try:
            return requests.get(self.url % term).content
        except RequestException:
            return ''

    def complete(self, kanji):
        """Get words which include specified kanji"""
        results = []
        soup = BeautifulSoup(self.lookup(kanji), 'lxml')
        for word in soup.find_all('span', {'class': 'kanji'}):
            # get text from html element, strip spaces and tabs
            word = word.get_text().strip()
            # skip kanji itself
            if word != kanji:
                results.append(word)

        return results

    def define(self,
               kanji,
               limit=20,
               skip_same_reading=False,
               skip_same_meaning=False):
        """Get words with specified kanji + meaning + kana
        Returns iterator.
        """
        results = OrderedDict({})

        soup = BeautifulSoup(self.lookup(kanji), 'lxml')

        # Utility function to get specific row|column text
        get_row = lambda row, column: row.find('td', column).get_text().strip()
        columns = ['kanji_column', 'kana_column', 'meanings_column']

        # Find rows with classes 'odd' and 'even'
        for row in soup.find_all("tr", {"class": re.compile(r"^(odd|even)$")}):
            # Skip 'lower' classes
            if 'lower' in row['class']:
                continue

            # Get columns by names
            word, kana, meaning = [get_row(row, column) for column in columns]

            # Append to results if not the same kanji
            if word != kanji:
                results[word] = {'kana': kana, 'meaning': meaning}

        # todo: filter results based on flags
        # todo: may filter by the same meaning and kana

        return islice(results.iteritems(), limit)

    def decompose(self, word):
        """Get word decomposition by kanji"""
        pass
