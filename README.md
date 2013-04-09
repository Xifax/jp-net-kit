jp-net-kit
==========

Collection of utilities, dedictated for consuming JDict, MeCab, Wordnet and other jp2en-translation-oriented services (even those without official API).

Example usage:

```Python
from jpnetkit.kit import Kit

for section, result in Kit().get(
    u'テスト', 'reading', 'examples', 'translation'
).items():
    print '~', section, '~'
    if isinstance(result, dict):
        for item, translation in result.items():
            print item, '->', translation
    else:
        print result
    print '------------------'
```

Will output reading, translation and found examples:

```
~ translation ~
テスト ->  テスト   (n,vs) test; (P); ED
------------------
~ reading ~
てすと
------------------
~ examples ~
成果のテスト -> Testing Your Work
テスト実行 -> Test Run
テスト初期化。 -> Test Initializer.
SynchronousSampleApplication のテスト -> Testing the SynchronousSampleApplication
------------------
```

`Kit` is just a wrapper for the following services:

* MeCab;
* JDic;
* Kradfile
* Weblio;
* Jisho;
* Wordnet.

Peruse available tests to grok api for each of the consumer.
