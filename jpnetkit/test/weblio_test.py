# -*- coding: utf-8 -*-

from jpnetkit.weblio import Weblio


class TestWeblio:
    """Test Weblio"""

    def test_can_get_definitions(self):
        """Test that we can get definitions from Weblio"""
        word = u'妖精'
        examples = Weblio().examples(word)
        assert len(examples) == 4
        for example, translation in examples.items():
            assert word in example
