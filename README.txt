jp-net-kit
==========

Collection of utilities, dedictated for consuming JDict, MeCab, Wordnet and other jp2en-translation-oriented services (even thouse without official API).

Example usage:

```Python
    from jpnetkit.kit import Kit

    for item, value in Kit().get(
        u'テスト', 'reading', 'examples', 'translation'
    ).items():
        print item, '\n', value
```

---

Rough TODOism:

1. MeCab API consumer (simplest one, actually provides API) [done];
2. JDict (requires some html parsing, partial implementation for jp2en should be enough) [done];
3. Kradfile-u (also very simple and quite useful) [done];
4. Wordnet (autocomplete, glossary, related terms) [done];
5. Weblio (examples with jp2en translation) [somewhat done]
6. Kotobank?

---

Possible dependencies:

1. Requests [yes]
2. Kata2hira [yes]
3. BeautifulSoup [yes]
4. MessagePack?

---

Additional notes:
http://guide.python-distribute.org/quickstart.html
