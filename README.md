Deployed at: http://leonardoblas.pythonanywhere.com

## Important
Accessing an image and seeing "n/a" doesn't mean the page is broken.
The Kanji Alive project doesn't have images for some, sometimes self-explanatory, radicals or their mnemonics. For example, the radical for the kanji representing "one" is just one horizontal stroke.

## Description
This creates a Japanese dictionary. It displays essential Japanese words (according to Kanji alive) next to their definition, spelling (in hiragana), and kanji composition. Next to each kanji, the dictionary provides an image of the kanji's radical and a mnemonic to see where in nature the radical could stem from.

This dictionary could have many uses but I created it to aid me in my quest to learn Japanese.

## How to use
```
flask run
```

## What's next
UI: It'd be best to display a limited amount of words, or one at a time, instead of showing the entire dictionary in a single page.

Pictures: Currently, the dictionary only provides links to the images of radicals and their mnemonics. This is because the whole dictionary is displayed in a single page (imagine displaying thousands of images on the same page). If we show one or a few entries at a time, displaying their related images would be doable.

## Credits
I developed this using the Kanji alive data, which is publicly available on https://github.com/kanjialive/kanji-data-media.
