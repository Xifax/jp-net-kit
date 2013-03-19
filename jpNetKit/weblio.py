#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Weblio API(as if) consumer
"""

import requests
from requests import RequestException
from bs4 import BeautifulSoup


class Weblio:

    def __init__(self):
        #self.definition_url = 'http://www.weblio.jp/content/%s'
        # Cannot find some rare words
        self.definition_url = 'http://ejje.weblio.jp/english-thesaurus/%s'
        self.lookup_url = 'http://ejje.weblio.jp/content/%s'
        self.examples_url = 'http://ejje.weblio.jp/sentence/content/%s'
        # TODO: stats (and corresponding DB entity)
        self.stats = {}

    def definition(self, term):
        """Fetches definitions and similar words, synonyms"""
        data = self.process(self.definition_url, term)
        # TODO: implement!
        if data:
            # Check for different possible divs:
            # NetDicBody
            # Wiktionary
            gloss = data.find('div', 'NetDicBody')
            #print gloss.getText()
            definitions = gloss.getText().split('(')
            print definitions

    def lookup(self, term):
        """Fetches translations (jp-en) for different use-cases"""
        pass

    def examples(self, term, number=4, portion=4, tuples=False):
        """
        Fetches examples from Weblio
        :param term:    word or phrase to lookup
        :param number:  number of examples to fetch
        :param portion: portion of examples to use (e.g., 1/2 -> from the middle)
        :returns:       list of touples (example, translation)
        """
        data = self.process(self.examples_url, term)
        examples = []
        if data:
            #for example in data.find_all('div', 'qotC')[-number:]:
            total = data.find_all('div', 'qotC')
            print len(total)
            n = len(total) / portion
            # Let's take examples from the middle (TODO: golden ratio?)
            for example in total[n: n + number]:
                # TODO: remove identical examples or similar to term
                # TODO: if no examples found -> log it (and mark term)
                # TODO: check (term:example) when there's english example [0] instead
                sentence = example.contents[0].getText()
                source = example.contents[1].span.getText()
                translation = example.contents[1].getText().replace(source, '')
                translation = self.remove_comments(translation, '<!--')
                if tuples:
                    examples.append((sentence, translation))
                else:
                    examples.append({sentence: translation})

        return examples

    def process(self, url, term):
        try:
            # Use lxml instead of HTMLParser (2.7.2 is bad with malformed tags)
            return BeautifulSoup(requests.get(url % term).text, 'lxml')
        except RequestException:
            return None

    def remove_comments(self, line, sep):
        """Trims comments from string"""
        for s in sep:
            line = line.split(s)[0]
        return line.strip()


def local_run():
    """Cosole utility stub"""
    output = open('/home/yadavito/Desktop/test2_export.txt', 'w')
    export = []
    for line in open('/home/yadavito/Desktop/test2.txt'):
        fields = line.split('\t')
        term = fields[0]
        weblio = Weblio()
        examples = weblio.examples(term)
        if examples:
            example = weblio.examples(term).pop()
        else:
            example = u''
        #print example
        fields[0] = unicode(fields[0], 'utf-8')
        fields[1] = unicode(fields[1], 'utf-8')
        fields[2] = unicode(fields[2], 'utf-8')
        fields[3] = example
        export.append(fields)

    print export
    for line in export:
        output.write(u'\t'.join(line).encode('utf-8'))
        # OMG
        output.write('\n')

if __name__ == '__main__':
    """Run as test script"""
    Weblio().definition(u'唆す')
    #local_run()
