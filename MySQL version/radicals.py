import pandas as pd
import unicodedata
import math
import pymysql

RADICALS_DB_CONFIG = {
    'host': 'japanesedictionary.mysql.pythonanywhere-services.com',
    'user': 'japanesedictiona',
    'password': 'capybara',
    'database': 'japanesedictiona$radicals',
}


def create_radicals_table():
    radicals_connection = pymysql.connect(**RADICALS_DB_CONFIG)
    radicals_cursor = radicals_connection.cursor()
    radicals_cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS radicals (
            radical VARCHAR(255) PRIMARY KEY,
            meaning VARCHAR(255),
            radical_image_url VARCHAR(255),
            radical_mnemonic_url VARCHAR(255)
        )
        '''
    )
    radicals_connection.commit()
    radicals_connection.close()


def populate_radicals_table():
    dfr = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/japanese-radicals.csv")

    radicals_connection = pymysql.connect(**RADICALS_DB_CONFIG)
    radicals_cursor = radicals_connection.cursor()

    for index, row in dfr.iterrows():
        radical = unicodedata.normalize("NFKC", row["Radical"])
        meaning = row["Meaning"]

        if isinstance(meaning, float) and math.isnan(meaning):
            meaning = ""
            radical_image_url = ""
            radical_mnemonic_url = ""

        else:
            romanji_reading = row["Reading-R"]
            radical_image_url = f"https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/{romanji_reading}2.svg"
            radical_mnemonic_url = f"https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/{romanji_reading}0.svg"

        radicals_cursor.execute(
            '''
            INSERT IGNORE INTO radicals (
                radical,
                meaning,
                radical_image_url,
                radical_mnemonic_url
            )
            VALUES (%s, %s, %s, %s)
            ''',
            (radical, meaning, radical_image_url, radical_mnemonic_url)
        )

    radicals_connection.commit()
    radicals_connection.close()


if __name__ == "__main__":
    create_radicals_table()
    populate_radicals_table()