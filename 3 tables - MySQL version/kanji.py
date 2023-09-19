import pandas as pd
import unicodedata
import pymysql

KANJI_DB_CONFIG = {
    'host': 'japanesedictionary.mysql.pythonanywhere-services.com',
    'user': 'japanesedictiona',
    'password': 'capybara',
    'database': 'japanesedictiona$kanji',
}


def create_kanji_table():
    kanji_connection = pymysql.connect(**KANJI_DB_CONFIG)
    kanji_cursor = kanji_connection.cursor()
    kanji_cursor.execute('''CREATE TABLE IF NOT EXISTS kanji (
        kanji VARCHAR(255) PRIMARY KEY,
        meaning TEXT,
        radical TEXT
    )''')
    kanji_connection.commit()
    kanji_connection.close()


def populate_kanji_table():
    dfw = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")

    kanji_connection = pymysql.connect(**KANJI_DB_CONFIG)
    kanji_cursor = kanji_connection.cursor()

    for index, row in dfw.iterrows():
        kanji = row["kanji"]
        meaning = row["kmeaning"]
        radical = unicodedata.normalize("NFKC", row["radical"])
        kanji_cursor.execute("INSERT IGNORE INTO kanji (kanji, meaning, radical) VALUES (%s, %s, %s)", (kanji, meaning, radical))

    kanji_connection.commit()
    kanji_connection.close()


if __name__ == "__main__":
    create_kanji_table()
    populate_kanji_table()
