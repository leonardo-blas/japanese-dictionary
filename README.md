Deployed at: http://leonardoblas.pythonanywhere.com

## Notes
As a data visualization project, the page may take some seconds to load. Note that it displays a table of 5812 essential Japanese words and their information.
<br>
The page could be broken down into several pages but I prefer seeing all the information in a single page, as it facilitates using Cmd + F.
<br>
The table's rows are not lazy loaded because that would interfere with using Cmd + F.
<br>
Seeing "n/a" means there is no image associated with a radical or its mnemonic.

## Description
This creates a Japanese dictionary. It displays essential Japanese words (according to Kanji alive) next to their definition, spelling (in hiragana), and kanji composition. 
<br>
Next to each kanji, the dictionary provides an image of the kanji's radical and a mnemonic to see where in nature the radical could stem from.
<br>
This dictionary could have many uses but I created it to aid me in my quest to learn Japanese.

## How to use
Install all dependencies.
<br>
On the terminal, navigate to the folder containing the files and:
<br>
```
flask run
```

## What's next
Vertically align kanji meanings and radical meanings in the template.

## Credits
I developed this using the Kanji alive data, which is publicly available on https://github.com/kanjialive/kanji-data-media.
