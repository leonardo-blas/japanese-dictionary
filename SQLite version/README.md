# Japanese dictionary
Deployed at: [japanesedictionary.pythonanywhere.com](https://japanesedictionary.pythonanywhere.com)
<br>
The page may take some seconds to load.
<br>
The table's rows are not lazy loaded because that would interfere with using Cmd + F.
<br>
Seeing "n/a" means there is no image associated with a radical or its mnemonic.

## Description
This creates and displays a dictionary of essential Japanese words. It displays words next to their definition, hiragana spelling, and kanji composition. Next to each kanji, it displays possible kanji meanings and the kanji's radical. Next to each radical, it displays possible radical meanings and a visual mnemonic to see where in nature the radical could stem from.
<br>
This dictionary could have many uses but I created it to aid me in my quest to learn Japanese.
<br>
<br>
<img width="1715" alt="image" src="https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/4f07d22b-1d7f-4171-9d54-03d861339a46">

<img width="1506" alt="image" src="https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/c33216a5-c448-4308-80c7-1a677e58578c">

<img width="878" alt="Architecture" src="https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/4c2621bb-3c2c-4175-94b6-67f6c2d3f7f0">

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
