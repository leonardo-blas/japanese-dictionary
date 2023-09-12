import pandas as pd
import sqlite3
import unicodedata


def create_kanji_table():
    kanji_connection = sqlite3.connect("kanji.db")
    kanji_cursor = kanji_connection.cursor()
    kanji_cursor.execute('''CREATE TABLE IF NOT EXISTS kanji (
        kanji TEXT PRIMARY KEY,
        meaning TEXT,
        radical TEXT
    )''')
    kanji_connection.commit()
    kanji_connection.close()


def populate_kanji_table():
    dfw = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")

    kanji_connection = sqlite3.connect("kanji.db")
    kanji_cursor = kanji_connection.cursor()

    for index, row in dfw.iterrows():
        kanji = row["kanji"]
        meaning = row["kmeaning"]
        radical = unicodedata.normalize("NFKC", row["radical"])
        kanji_cursor.execute("INSERT OR REPLACE INTO kanji (kanji, meaning, radical) VALUES (?, ?, ?)", (kanji, meaning, radical))

    kanji_connection.commit()
    kanji_connection.close()


if __name__ == "__main__":
    create_kanji_table()
    populate_kanji_table()
