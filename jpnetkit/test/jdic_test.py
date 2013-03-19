#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jpnetkit.jdic import JDic


class TestJDic:
    """Test JDic"""

    def test_can_translate_words_in_sentence(self):
        """Test that we can translate sentence word by word"""
        sentence = u'体を癒すために。'
        translations = JDic().lookup(sentence)
        assert len(translations) == 3
        for key in translations.keys():
            assert key in sentence
