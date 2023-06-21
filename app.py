import pandas as pd
import ast
import sqlite3
from flask import Flask, render_template, redirect
import unicodedata

app = Flask(__name__)

table_created = False


def create_table():
    """
    Creates a SQLite table only if it doesn't already exist.
    Loads Kanji alive data into the table.
    Words are composed of kanji, and each kanji has exactly one radical.
    Radicals are mapped to their romanji reading and their mnemonic (if provided).
    Kanji are mapped to their meaning and radical.
    Words are related to their kanji from Kanji alive's dataset.
    Displays words along their spellings and definitions.
    Displays kanji along their meanings.
    Displays radicals along their meanings and mnemonics.

    TODO: Vertically align kanji meanings and radical meanings in the template.
    """
    global table_created

    if not table_created:
        # Radicals data frame.
        dfr = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/japanese-radicals.csv")

        # Encoding radicals to prevent access problems.
        dfr["Radical"] = dfr["Radical"].apply(lambda x: unicodedata.normalize("NFKC", x))

        # Mapping radicals to their romanji reading and meaning.
        # Used for O(1) access to radical information for each kanji.
        radicals_map =\
            dfr.groupby("Radical").apply(lambda group: group[["Reading-R", "Meaning"]].values[0].tolist()).to_dict()

        # Appending radical image URLs to the map.
        for radical, radical_info in radicals_map.items():
            romanji_reading = str(radical_info[0])
            radical_image_url = "https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/" \
                                + romanji_reading + "2.svg"
            r_mnemonic_url = "https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/" \
                             + romanji_reading + "0.svg"

            radical_info.append(radical_image_url)
            radical_info.append(r_mnemonic_url)

        # Words data frame.
        dfw = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")

        # Mapping kanji to their meaning and radical.
        # Used for O(1) queries to verify kanji, as words may have other characters, like hiragana.
        kanji_map = dict(zip(dfw["kanji"], zip(dfw["kmeaning"], dfw["radical"])))

        # Creating a dictionary to map words to their kanji and kanji to their radical.
        # Used for O(1) queries to verify if a word is already in the dictionary.
        # Used to construct the SQLite table.
        japanese_words_dictionary = {}

        # Filling all word-related lists.
        for row in dfw["examples"]:
            # Preparing a row for iteration.
            row = ast.literal_eval(row)

            # Selecting and curating a word's information.
            for word_info in row:
                word_and_spelling = word_info[0].split("（")
                word = word_and_spelling[0]

                # If the word is already in the dictionary, select the next word.
                if word in japanese_words_dictionary:
                    break

                # If the word starts with an unnecessary asterisk, remove it.
                if word[0] == "*":
                    word = word[1:]

                spelling = word_and_spelling[1][:-1]
                definition = word_info[1]

                # Using strings to store word information, as SQLite doesn't take lists as arguments.
                kanji_in_word = ""
                kanji_meanings = ""
                radical_image_url = ""
                radical_mnemonic_url = ""
                radical_meanings = ""

                # Selecting and curating data related to each kanji in a word.
                for kanji in word:
                    # Words may have non-kanji characters, like hiragana.
                    if kanji in kanji_map:
                        kanji_info = kanji_map.get(kanji)
                        # Encoding radicals to prevent access problems.
                        radical = unicodedata.normalize("NFKC", kanji_info[1])

                        # Using semicolons as separators.
                        # The table.html template separates by semicolon.
                        kanji_in_word += kanji + ";"
                        kanji_meanings += str(kanji_info[0]) + ";"
                        radical_image_url += radicals_map[radical][2] + ";"
                        radical_mnemonic_url += radicals_map[radical][3] + ";"
                        radical_meanings += str(radicals_map[radical][1]) + ";"

                # Mapping a word to an empty list. We will append word data to it.
                japanese_words_dictionary[word] = []

                # Filling the Japanese words dictionary with word data.
                japanese_words_dictionary[word].extend([spelling,
                                                        definition,
                                                        kanji_in_word,
                                                        kanji_meanings,
                                                        radical_image_url[:-1],
                                                        radical_mnemonic_url[:-1],
                                                        radical_meanings])

        # Creating a SQLite table.
        connection = sqlite3.connect("japanese_words_dictionary.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS japanese_words_dictionary ("
                       "word text,"
                       "spelling text,"
                       "definition text,"
                       "kanji text,"
                       "kanji_meanings text,"
                       "radical_image_url text,"
                       "radical_mnemonic_url text,"
                       "radical_meanings text)")

        # Filling the SQLite table.
        for word, word_data in japanese_words_dictionary.items():
            cursor.execute("INSERT INTO japanese_words_dictionary (word, spelling, definition, kanji, kanji_meanings,"
                           "radical_image_url, radical_mnemonic_url, radical_meanings)"
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (word,
                            word_data[0],
                            word_data[1],
                            word_data[2],
                            word_data[3],
                            word_data[4],
                            word_data[5],
                            word_data[6]))

        connection.commit()
        connection.close()

        table_created = True

        print(len(japanese_words_dictionary))


@app.route("/")
def home():
    # Creating a SQLite table only if it doesn't already exist.
    create_table()

    # Fetching the table's data.
    connection = sqlite3.connect("japanese_words_dictionary.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM japanese_words_dictionary")
    word_rows = cursor.fetchall()
    connection.close()

    # Displaying the table's data.
    return render_template("table.html", rows=word_rows)


if __name__ == "__main__":
    app.run()
