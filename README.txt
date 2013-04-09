==========
jp-net-kit
==========

Collection of utilities, dedictated for consuming following services:

* MeCab;
* JDic;
* Kradfile
* Weblio;
* Jisho;
* Wordnet.


Example usage:

    #!/usr/bin/env python
    # encoding: utf-8

    from jpnetkit.kradfile import Kradfile
    from jpnetkit.jisho import Jisho
    from jpnetkit.weblio import Weblio
    from jpnetkit.mecab import MeCab

    # our kanji
    amusing_kanji = u'称'

    # get radical decomposition
    radicals = Kradfile().get_radikals_for(amusing_kanji)

    # compile examples list with readings and translation
    # for each of the word, that contains our kanji
    examples = {}
    weblio = Weblio()
    mecab = MeCab()
    jisho = Jisho()

    for word in jisho.complete(amusing_kanji):
        for sentence, translation in weblio.examples(word).iteritems():
            examples[word] = {
                'example': sentence,
                'translation': translation,
                'reading': mecab.get_reading(sentence),
            }
