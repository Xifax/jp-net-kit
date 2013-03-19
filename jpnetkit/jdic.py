#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import get, RequestException
from bs4 import BeautifulSoup


class JDic:
    """
    Queries JDic Web API (at csse.monash.edu.au) and returns parsed data
    """

    def __init__(self):
        """Setup request url and default request options"""
        self.url = ('http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?'
                    '9MIG%s')

    def lookup(self, sentence):
        """Lookup translations and reading of sentence|word"""
        return self.parse(self.query(sentence))

    def query(self, request):
        """Query JDic to analyze sentence|word"""
        try:
            return BeautifulSoup(get(self.url % request).text, 'lxml')
        except RequestException:
            return None

    def parse(self, response):
        """Parse JDic response as html"""
        try:
            return dict(zip(
                # keys: Items (colorized)
                [item.getText()
                    for item in response.find(id='inp').find_all('font')
                    if 'color' in item.attrs],
                # values: Translations (as list elements)
                [li.getText()
                    for li in response.find(id='inp').find_all('li')]
            ))
        except Exception:
            return None
