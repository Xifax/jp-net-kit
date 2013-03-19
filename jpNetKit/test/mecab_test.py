# -*- coding: utf-8 -*-

from src.api.jp.mecab import MeCab


class TestMeCab:
    """Detect language API test cases."""

    def test_can_get_sentence_reading_in_hiragana(self):
        """Test that we can get correct sentence reading"""
        assert (
            MeCab().reading(u'来週からテストが始まる。') ==
            u'らいしゅうからてすとがはじまる。'
        )

    def test_can_get_sentence_reading_in_katakana(self):
        """Test that we can get correct sentence reading without conversion"""
        assert (
            MeCab().reading(u'来週からテストが始まる。', hiragana=False) ==
            u'ライシュウカラテストガハジマル。'
        )

    def test_can_get_reading_word_by_word(self):
        """Test that we can get reading word by word"""
        for word, reading in MeCab().wordByWord(u'来週からテストが始まる。'):
            if word == u'来週':
                assert reading == u'らいしゅう'
            elif word == u'から':
                assert reading == u''
            elif word == u'始まる':
                assert reading == u'はじまる'
            elif word == u'テスト':
                assert reading == u''
            elif word == u'が':
                assert reading == u''

    def test_can_get_single_kanji_reading(self):
        """Test that we can get single kanji reading"""
        assert MeCab().reading(u'音') == u'おと'
