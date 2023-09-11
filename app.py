import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

"""
Displays words along their spellings and definitions.
Displays kanji along their meanings.
Displays radicals along their meanings and mnemonics.

TODO: Vertically align kanji meanings and radical meanings in the template.
"""


@app.route("/")
def home():
    # Fetching the unique first characters from the database.
    connection = sqlite3.connect("japanese_words_dictionary.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT substr(word, 1, 1) FROM japanese_words_dictionary")
    first_characters = [row[0] for row in cursor.fetchall()]
    connection.close()

    # Displaying the list of unique first characters.
    return render_template("home_table.html", first_characters=first_characters)


@app.route("/<starting_character>")
def display_words_starting_with(starting_character):
    # Fetching the table's data for words starting with the specified character.
    connection = sqlite3.connect("japanese_words_dictionary.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM japanese_words_dictionary WHERE word LIKE ? || '%'", (starting_character,))
    word_rows = cursor.fetchall()
    connection.close()

    # Displaying the table's data.
    return render_template("table.html", rows=word_rows)


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