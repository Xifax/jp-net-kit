# -*- coding: utf-8 -*-

from glob import glob
from tempfile import gettempdir

from jpnetkit.kradfile import Kradfile


class TestKradfile:
    """Test Kradfile"""

    def test_can_prepare_kradfile(self):
        """Test that we can prepare kradfile"""
        assert len(Kradfile().prepare_radikals()) >= 13108

    def test_can_get_radikal_decomposition(self):
        """Test that we can get radikal decomposition for kanji"""
        assert ([u'一', u'言', u'口', u'五'] ==
                Kradfile().get_radikals_for(u'語', use_cache=False))

    def test_can_cache_kradfile(self):
        """Test that we can cache kradfile"""
        krad = Kradfile()
        assert ([u'一', u'言', u'口', u'五'] ==
                krad.get_radikals_for(u'語', use_cache=True))
        assert len(glob(gettempdir() + '/*.krad')) == 1
        krad.clean_cache()
        assert len(glob(gettempdir() + '/*.krad')) == 0
