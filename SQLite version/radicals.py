import pandas as pd
import sqlite3
import unicodedata
import math


def create_radicals_table():
    radicals_connection = sqlite3.connect("radicals.db")
    radicals_cursor = radicals_connection.cursor()
    radicals_cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS radicals (
            radical TEXT PRIMARY KEY,
            meaning TEXT,
            radical_image_url TEXT,
            radical_mnemonic_url TEXT
        )
        '''
    )
    radicals_connection.commit()
    radicals_connection.close()


def populate_radicals_table():
    rdf = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/japanese-radicals.csv")

    radicals_connection = sqlite3.connect("radicals.db")
    radicals_cursor = radicals_connection.cursor()

    for index, row in rdf.iterrows():
        radical = unicodedata.normalize("NFKC", row["Radical"])
        meaning = row["Meaning"]

        if isinstance(meaning, float) and math.isnan(meaning):
            meaning = ""
            radical_image_url = ""
            radical_mnemonic_url = ""

        else:
            romanji_reading = row["Reading-R"]
            radical_image_url = f"https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-characters/{romanji_reading}.svg"
            radical_mnemonic_url = f"https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/{romanji_reading}0.svg"

        radicals_cursor.execute(
            '''
            INSERT OR REPLACE INTO radicals (
                radical,
                meaning,
                radical_image_url,
                radical_mnemonic_url
            )
            VALUES (?, ?, ?, ?)
            ''',
            (radical, meaning, radical_image_url, radical_mnemonic_url)
        )

    radicals_connection.commit()
    radicals_connection.close()


if __name__ == "__main__":
    create_radicals_table()
    populate_radicals_table()
