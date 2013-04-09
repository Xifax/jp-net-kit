#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jpnetkit.jisho import Jisho


class TestJisho:
    """Test Jisho api consumer"""

    def test_can_complete_kanji(self):
        """Test that we can complete kanji"""
        kanji = u'琉'
        should_have_found = [
            u'琉璃',
            u'琉歌',
            u'琉球語',
            u'琉球藍',
            u'琉球芋',
            u'琉球音階',
            u'琉球諸島',
            u'琉球列島',
            u'琉球古武術'
        ]

        for word in Jisho().complete(kanji):
            assert word in should_have_found

    def test_can_get_words_and_definitions(self):
        """Test that we can complete kanji and get definitions for words"""
        kanji = u'琉'
        resulting_info = {
            u'琉歌':
            {'meaning': 'Okinawan fixed form poetry', 'kana': u'りゅうか'},
            u'琉球語':
            {'meaning': 'Ryukyuan languages', 'kana': u'りゅうきゅうご'},
        }

        for word, info in Jisho().define(kanji):
            if word in resulting_info:
                assert info['meaning'] == resulting_info[word]['meaning']
                assert info['kana'] == resulting_info[word]['kana']
