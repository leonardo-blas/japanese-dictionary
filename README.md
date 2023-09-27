# Japanese dictionary
Deployed at: http://3.141.39.12/
<br>
Using the [japanesedictionary.pythonanywhere.com](www.japanesedictionary.pythonanywhere.com) link will redirect you to the address above. This is a temprary placeholder until I get a prettier domain name.
<br>
Seeing "n/a" means there is no image associated with a mnemonic.

## Description
This creates and displays a dictionary of essential Japanese words. It displays words next to their definition, hiragana spelling, and kanji composition. Next to each kanji, it displays possible kanji meanings and the kanji's radical. Next to each radical, it displays possible radical meanings and a visual mnemonic to see where in nature the radical could stem from.
<br>
This dictionary could have many uses but I created it to aid me in my quest to learn Japanese.
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

## Architecture
The architecture depends on 3 databases:
  * One for 8474 words, their spelling, and their definitions.
  * A second for 1234 kanji, their meanings and their radicals.
  * And a third for 319 radical characters, their meanings, and their mnemonics.

Note that there are only 214 unique radicals, but a radical may have more than one character associated with it (different versions of the same radical).
<br>
The backend is managed using Flask.
<br>
The application is hosted using Gunicorn and it's made available online using NGINX.
<br>
All components are deployed on an EC2 Ubuntu T2 instance.

![Architecture](https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/f4205a29-047e-4b52-aed2-98a13093c413)

<img width="1728" alt="SQL tables" src="https://github.com/leonardo-blas/japanese-dictionary/assets/125172895/6317e757-c979-4005-8219-22911721483e">

## What's next
### Styling
Change （ characters for ( in the radical meaning column.
<br>
Styling the tables.

### Features
Adding a search bar.
<br>
Add a romanji spelling column for words. Use the romkan library to render the column.
<br>
Think about a computer vision algorithm to identify the non-radical "building blocks" of kanji.

### Deployment
Get a custom domain name.
<br>
Make Gunicorn and NGINX bootup routines, so if the instance restarts for any reason, the app will go back online.

## Credits
I developed this using the Kanji alive data, which is publicly available on https://github.com/kanjialive/kanji-data-media.
