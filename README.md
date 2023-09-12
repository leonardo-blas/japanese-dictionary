# Japanese dictionary
Deployed at: [japanesedictionary.pythonanywhere.com](https://japanesedictionary.pythonanywhere.com)
<br>
The page may take some seconds to load.
<br>
Seeing "n/a" means there is no image associated with a radical or its mnemonic.

## Description
This creates and displays a dictionary of essential Japanese words. It displays words next to their definition, hiragana spelling, and kanji composition. Next to each kanji, it displays possible kanji meanings and the kanji's radical. Next to each radical, it displays possible radical meanings and a visual mnemonic to see where in nature the radical could stem from.
<br>
This dictionary could have many uses but I created it to aid me in my quest to learn Japanese.
<br>
<br>
<img width="1715" alt="image" src="https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/4f07d22b-1d7f-4171-9d54-03d861339a46">

<img width="1461" alt="image" src="https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/6fe7c292-b243-488d-a086-84f83cdc3290">

## Demo
https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/ad6d4e27-5bd4-4955-b98a-27d9f0cc6cef

## Running it locally
**These instructions are only for the SQLite version.**
<br>
Install all dependencies:
```
pip3 install -r requirements.txt
```
Create the databases:
```
python3 words.py
python3 kanji.py
python3 radicals.py
```
Run the application:
```
flask run
```

## What's next
Styling the tables, UI development.

## Credits
I developed this using the Kanji alive data, which is publicly available on https://github.com/kanjialive/kanji-data-media.
