import pandas as pd
import unicodedata
import ast
import pymysql

WORDS_DB_CONFIG = {
    'host': 'japanesedictionary.mysql.pythonanywhere-services.com',
    'user': 'japanesedictiona',
    'password': 'capybara',
    'database': 'japanesedictiona$words',
}


def create_words_table():
    words_connection = pymysql.connect(**WORDS_DB_CONFIG)
    words_cursor = words_connection.cursor()
    words_cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS words (
            word VARCHAR(255) PRIMARY KEY,
            definition VARCHAR(255),
            spelling VARCHAR(255)
        )'''
    )
    words_connection.commit()
    words_connection.close()


def populate_words_table():
    dfw = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")

    # Used to translate Arabic numeric characters to Japanese full-width numeric characters.
    translation_table = str.maketrans("0123456789", "０１２３４５６７８９")

    words_connection = pymysql.connect(**WORDS_DB_CONFIG)
    words_cursor = words_connection.cursor()

    for entry in dfw["examples"]:
        # Parsing an entry, a string formatted as a list, into a Python list.
        entry = ast.literal_eval(entry)

        for word_info in entry:
            word_and_spelling = word_info[0].split("（")
            word = unicodedata.normalize("NFKC", word_and_spelling[0])
            # Translating numeric characters.
            word = word.translate(translation_table)

            # Check if the word already is in the database.
            words_cursor.execute("SELECT 1 FROM words WHERE word = %s", (word,))

            # Skip if the word is already in the database.
            if words_cursor.fetchone() is not None:
                continue

            if word.startswith("*") or word.startswith("~"):
                word = word[1:]

            definition = word_info[1]
            spelling = word_and_spelling[1][:-1]

            words_cursor.execute(
                '''
                INSERT IGNORE INTO words (
                    word,
                    definition,
                    spelling
                )
                VALUES (%s, %s, %s)
                ''',
                (word, definition, spelling)
            )

    words_connection.commit()
    words_connection.close()


if __name__ == "__main__":
    create_words_table()
    populate_words_table()
