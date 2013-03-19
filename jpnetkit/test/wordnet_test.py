# -*- coding: utf-8 -*-

from jpnetkit.wordnet import Wordnet


class TestWordnet:
    """Test Wordnet"""

    def test_can_complete_kanji(self):
        """Test that we can complete kanji"""
        words = Wordnet().complete(u'始')
        assert len(words) >= 10
        example_words = [u'始まり', u'始める', u'始動']
        for word in example_words:
            assert word in words

    def test_can_get_gloss_for_word(self):
        """Test that we can lookup word in glossary"""
        fields_present = [
            'gloss',
            'translate',
            'words',
            'ss_type',
            'lex_filename',
            'synset_offset',
        ]
        for definition in Wordnet().lookup(u'始まり'):
            for field in fields_present:
                assert field in definition
