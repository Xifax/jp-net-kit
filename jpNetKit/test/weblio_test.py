# -*- coding: utf-8 -*-

from src.api.jp.weblio import Weblio


class TestWeblio:
    """Test Weblio"""

    def test_can_get_definitions(self):
        """Test that we can get definitions from Weblio"""
        #for usage, translation in Weblio().examples(u'唆す'):
        for usage, translation in Weblio().examples(u'妖精'):
            print usage, translation
