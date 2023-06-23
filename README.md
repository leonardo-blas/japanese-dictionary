Deployed at: [japanesedictionary.pythonanywhere.com](https://japanesedictionary.pythonanywhere.com)

## Notes
As a data visualization project, the page may take some seconds to load.
<br>
The data could be displayed on several pages but I prefer seeing all the information on a single page, as it facilitates using Cmd + F.
<br>
The table's rows are not lazy loaded because that would interfere with using Cmd + F.
<br>
Seeing "n/a" means there is no image associated with a radical or its mnemonic.

## Description
This creates and displays a dictionary of 5812 essential Japanese words. It displays words next to their definition, hiragana spelling, and kanji composition. Next to each kanji, it displays possible kanji meanings and the kanji's radical. Next to each radical, it displays possible radical meanings and a visual mnemonic to see where in nature the radical could stem from.
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
