#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import remove
from pickle import loads, dumps
from tempfile import NamedTemporaryFile, gettempdir

from requests import get, RequestException


class Kradfile:
    """
    Kradfile-u consumer
    NB: Everything is stored as unicode.
    """

    def __init__(self):
        """Set Kradfile location"""
        self.url = 'http://www.kanjicafe.com/downloads/kradfile-u.gz'

    def get_kradfile(self):
        """Get Kradfile-u"""
        try:
            return get(self.url).content
        except RequestException:
            return ''

    def prepare_radikals(self):
        """Parse Kradfile into dictionary
        :return: dictionary of kanji and corresponding radikals
        """
        results = {}
        for line in self.get_kradfile().split('\n'):
            if not line or line.startswith('#'):
                continue

            kanji, radikals = line.split(':')
            results[unicode(kanji.strip(), 'utf-8')] = [
                unicode(rad, 'utf-8') for rad
                in radikals.split(' ')
                if rad != ''
            ]

        return results

    def get_radikals_for(self, kanji, use_cache=True):
        """Lookup radikal decomposition for specified kanji
        Will try to cache Kradfile in temp dir (as *.krad files) using pickle.
        :return: list of radikals
        """
        if use_cache:
            # 1st. Check if kradfile is already cached
            cache = False
            for krad in glob(gettempdir() + '/*.krad'):
                # If cached -- restore
                with open(krad, 'r') as cache:
                    radikals = loads(cache.read())
                cache = True
                break

            # 2nd. If not cached, then prepare and cache
            if not cache:
                with NamedTemporaryFile(suffix='.krad', delete=False) as cache:
                    radikals = self.prepare_radikals()
                    cache.write(dumps(radikals))
        else:
            radikals = self.prepare_radikals()

        # 3rd. Lookup kanji in restored kradfile
        return radikals.get(kanji, u'')

    def clean_cache(self):
        """Clean-up kradfile cache"""
        for krad in glob(gettempdir() + '/*.krad'):
            remove(krad)
