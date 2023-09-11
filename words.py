import pandas as pd
import sqlite3
import ast
import unicodedata

translation_table = str.maketrans("0123456789", "０１２３４５６７８９")


# Function to create the words table
def create_words_table():
    connection = sqlite3.connect("words.db")  # Create a separate database for words
    cursor = connection.cursor()

    # Create a table for words if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS words (
        word TEXT PRIMARY KEY,
        definition TEXT,
        spelling TEXT
    )''')

    connection.commit()
    connection.close()


# Function to populate the words table from the DataFrame
def populate_words_table(dfw):
    connection = sqlite3.connect("words.db")  # Use the separate database for words
    cursor = connection.cursor()

    # Creating a dictionary to map words to their kanji and kanji to their radical
    japanese_words_dictionary = {}

    for entry in dfw["examples"]:
        entry = ast.literal_eval(entry)

        for word_info in entry:
            word_and_spelling = word_info[0].split("（")
            word = unicodedata.normalize("NFKC", word_and_spelling[0])
            word = word.translate(translation_table)

            if word in japanese_words_dictionary:
                continue  # Skip if word is already in the dictionary

            if word.startswith("*") or word.startswith("~"):
                word = word[1:]

            definition = word_info[1]
            spelling = word_and_spelling[1][:-1]

            # Insert data into the words table
            cursor.execute("INSERT OR REPLACE INTO words (word, definition, spelling) VALUES (?, ?, ?)",
                           (word, definition, spelling))

            japanese_words_dictionary[word] = True

    connection.commit()
    connection.close()


# Function to print the words table
def print_words_table():
    # Connect to the SQLite database
    connection = sqlite3.connect("words.db")
    cursor = connection.cursor()

    # Execute a SELECT query to fetch data from the words table
    cursor.execute("SELECT * FROM words")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Print the table header
    print("Word\tDefinition\tSpelling")

    # Print each row of the table
    for row in rows:
        word, definition, spelling = row
        print(f"{word}\t{definition}\t{spelling}")

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    create_words_table()
    dfw = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")
    populate_words_table(dfw)

    print_words_table()
