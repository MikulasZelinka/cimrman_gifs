# [Gify z Divadla Járy Cimrmana](https://cimrman.zelinka.dev)

- https://cimrman.zelinka.dev

Toto je pouze nástroj, který umožňuje snadněji vyhledávat, prohlížet a sdílet Cimrmanovské pohyblivé obrázky.

Na Giphy je [oficiálně nahrála Česká televize](https://www.facebook.com/ceskatelevize/posts/10157786507422686), požadavky na přidání chybějících gifů tedy směřujte tam.
Pokud k přidání dojde (dejte mi vědět), objeví se časem i [zde](https://cimrman.zelinka.dev).

## Jak vygenerovat data pro web

Původně:
```shell
python get get_gifs_with_keywords.py
```


Nyní (jelikož Giphy search nefunguje jak by měl a část výsledků nenajde):
```shell
python get_gifs_from_historical_gif_ids.py
```


## TODO
- [x] obtain static list of (cimrman) gifs, keywords and image urls
- [x] search in keywords
- [x] reasonable display of gif previews
- [x] copy to clipboard
- [x] random shuffle on load
- [x] display webm instead of gifs (better quality/size ratio)
- [x] display mp4 instead of webm (better quality/size ratio)
- [x] vanishing tooltip alert after clipboard copy
- [x] cleanup json (remove redundant image urls)
- [ ] option to select gif quality to be shared
- [x] smart/dynamic image load (only when displayed) (it _might_ work)
- [x] search for multiple keywords (separate query by whitespaces)
- [x] ignore list for gifs that have nothing to do with mr. Jarunka
- [x] support regex search (without that we can't search for "jak" only as it is contained in "smoljak")
- [ ] lazyload vue video elements to avoid the initial stutter
  - https://adrienhobbs.github.io/vue-lazyload-video/
