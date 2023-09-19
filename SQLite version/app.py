import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders a table in the format radical meaning, symbol.
    Displays all unique first characters for all words in the words database, next to its radical meaning.
    Each unique character is a hyperlink to the page of words that start with that character.
    Some characters are not kanji, like hiragana or numbers, and some are kanji which Kanji alive has no data on.
    The characters without radical meaning are displayed next to "n/a" for radical meaning.
    Personal choice to organize the dictionary entries.
    """
    # Dictionary to store starting characters with radical meanings.
    radical_meaning_dict = {}

    words_connection = sqlite3.connect("words.db")
    words_cursor = words_connection.cursor()
    # Fetching unique first characters from the words database.
    words_cursor.execute("SELECT DISTINCT SUBSTR(word, 1, 1) FROM words")
    first_characters = [row[0] for row in words_cursor.fetchall()]

    for character in first_characters:
        kanji_connection = sqlite3.connect("kanji.db")
        kanji_cursor = kanji_connection.cursor()
        # Fetch the radicals associated with the character.
        kanji_cursor.execute("SELECT radical FROM kanji WHERE kanji = ?", (character,))
        radicals = [row[0] for row in kanji_cursor.fetchall()]
        kanji_connection.close()

        # If no radicals found, add the character to the list with "n/a" radical meaning.
        if not radicals:
            radical_meaning = "n/a"
        else:
            # Group the character by its associated radical meanings in the dictionary.
            radical_connection = sqlite3.connect("radicals.db")
            radical_cursor = radical_connection.cursor()
            radical_cursor.execute("SELECT meaning FROM radicals WHERE radical = ?", (radicals[0],))
            radical_meaning = radical_cursor.fetchone()[0]
            radical_connection.close()

        if radical_meaning not in radical_meaning_dict:
            radical_meaning_dict[radical_meaning] = []
        radical_meaning_dict[radical_meaning].append(character)

    words_connection.close()

    # Sort the dictionary by radical meaning.
    sorted_radical_meaning_dict = dict(sorted(radical_meaning_dict.items()))
    return render_template("index_table.html", radical_meaning_dict=sorted_radical_meaning_dict)


@app.route("/<starting_character>")
def display_words_starting_with(starting_character):
    """
    Displays words along their spellings and definitions.
    Displays kanji along their meanings.
    Displays radicals along their meanings and mnemonics.
    """
    word_conn = sqlite3.connect("words.db")
    words_cursor = word_conn.cursor()

    kanji_conn = sqlite3.connect("kanji.db")
    kanji_cursor = kanji_conn.cursor()

    radicals_conn = sqlite3.connect("radicals.db")
    radicals_cursor = radicals_conn.cursor()

    words_cursor.execute("SELECT * FROM words WHERE word LIKE ? || '%'", (starting_character,))
    words = words_cursor.fetchall()

    data = []

    for word in words:
        word = word[0]
        words_cursor.execute("SELECT * FROM words WHERE word = ?", (word,))
        word_row = words_cursor.fetchall()
        word_spelling = word_row[0][1]
        word_definition = word_row[0][2]

        word_data = []

        for character in word:
            kanji_cursor.execute("SELECT * FROM kanji WHERE kanji = ?", (character,))
            kanji_row = kanji_cursor.fetchall()
            kanji_row = kanji_row

            if kanji_row:
                kanji_row = kanji_row[0]
                kanji_meaning = kanji_row[1]
                radical = kanji_row[2]

                radicals_cursor.execute("SELECT * FROM radicals WHERE radical = ?", (radical,))
                radical_row = radicals_cursor.fetchall()
                radical_row = radical_row[0]
                radical_meaning = radical_row[1]
                radical_image_url = radical_row[2]
                radical_mnemonic_url = radical_row[3]

                word_data.append([character, kanji_meaning, radical_image_url, radical_meaning, radical_mnemonic_url])

            else:
                word_data.append([character, "", "", "", ""])

        data.append([word_spelling, word_definition, word_data])

    word_conn.close()
    kanji_conn.close()
    radicals_conn.close()

    return render_template("dictionary_table.html", data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
