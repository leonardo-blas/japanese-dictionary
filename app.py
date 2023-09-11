import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Initialize a dictionary to store starting characters with radical meanings.
    radical_meaning_dict = {}

    # Fetching the unique first characters from the words database.
    connection = sqlite3.connect("words.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT substr(word, 1, 1) FROM words")
    first_characters = [row[0] for row in cursor.fetchall()]

    for character in first_characters:
        # Fetch the radicals associated with the character from kanji.db.
        kanji_connection = sqlite3.connect("kanji.db")
        kanji_cursor = kanji_connection.cursor()
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

    connection.close()

    # Sort the dictionary by radical meaning.
    sorted_radical_meaning_dict = dict(sorted(radical_meaning_dict.items()))

    # Display the table with radical meanings and associated starting characters.
    return render_template("index_table.html", radical_meaning_dict=sorted_radical_meaning_dict)


@app.route("/<starting_character>")
def display_words_starting_with(starting_character):
    """
    Displays words along their spellings and definitions.
    Displays kanji along their meanings.
    Displays radicals along their meanings and mnemonics.
    """
    word_conn = sqlite3.connect('words.db')
    words_cursor = word_conn.cursor()

    kanji_conn = sqlite3.connect('kanji.db')
    kanji_cursor = kanji_conn.cursor()

    radicals_conn = sqlite3.connect('radicals.db')
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

    # Displaying the table's data.
    return render_template("dictionary_table.html", data=data)


if __name__ == "__main__":
    app.run()


"""
Everytime you restart the application, you re-create the the table and append it
to the existing table, so the row duplicates will increase +1 for every time
you kill and restart via flask run.


３ vs 3


somehow sort the table: 
軒数
軒
軒下
"""