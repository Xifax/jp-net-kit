#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jpnetkit.kit import Kit


class TestKit:
    """Test Kit"""

    def test_can_get_reading(self):
        """Test that we can get reading"""
        assert(
            Kit().get_reading(u'来週からテストが始まる。') ==
            u'らいしゅうからてすとがはじまる。'
        )

    def test_can_get_specified_items(self):
        """Test that we can get specified items"""
        results = Kit().get(u'テスト', 'reading', 'translation', 'examples')
        keys = ['translation', 'reading', 'examples']
        for key in results.keys():
            assert key in keys

    def test_can_get_only_one_result(self):
        """Test that we can get specified items"""
        assert Kit().get(u'テスト', 'reading') == u'てすと'
