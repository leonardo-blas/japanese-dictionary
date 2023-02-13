import pandas as pd
import ast
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

table_created = False


def create_table():
    global table_created

    if not table_created:
        df = pd.read_csv(
            f"https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")

        words = []
        spellings = []
        definitions = []
        kanji = []
        kanji_meanings = []
        radical_image_urls = []
        radical_mnemonic_urls = []
        radical_meanings = []

        kanji_to_info_map = dict(zip(df["kanji"], zip(df["kmeaning"], df["rad_name"], df["rad_meaning"])))

        for row in df["examples"]:
            row = ast.literal_eval(row)

            for word_info in row:
                word_and_spelling = word_info[0].split("（")

                words.append(word_and_spelling[0])
                spellings.append(word_and_spelling[1][:-1])
                definitions.append(word_info[1])

                kanji_in_word = ""
                kanji_meaning = ""
                radical_image_url = ""
                radical_mnemonic_url = ""
                radical_meaning = ""

                for character in word_and_spelling[0]:
                    if character in kanji_to_info_map:
                        kanji_in_word += character + ";"

                        info = kanji_to_info_map.get(character)
                        kanji_meaning += str(info[0]) + ";"
                        radical_image_url += \
                            "https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/" \
                            + str(info[1]) + "2.svg;"
                        radical_mnemonic_url += \
                            "https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/" \
                            + str(info[1]) + "0.svg;"

                        radical_meaning += str(info[1:][1:][0]) + ";"

                kanji.append(kanji_in_word)
                kanji_meanings.append(kanji_meaning)
                radical_image_urls.append(radical_image_url[:-1])
                radical_mnemonic_urls.append(radical_mnemonic_url[:-1])
                radical_meanings.append(radical_meaning)

        connection = sqlite3.connect("dictionary.db")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE words")  # ADDRESS THIS
        cursor.execute("CREATE TABLE words (word text, spelling text, definition text, kanji text, kanji_meaning text,"
                       "radical_image_url text, radical_mnemonic_url text, radical_meaning text)")

        table_rows = len(words)
        for i in range(table_rows):
            cursor.execute("INSERT INTO words (word, spelling, definition, kanji, kanji_meaning, radical_image_url,"
                           "radical_mnemonic_url, radical_meaning) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (words[i], spellings[i], definitions[i], kanji[i], kanji_meanings[i], radical_image_urls[i],
                            radical_mnemonic_urls[i], radical_meanings[i]))

        connection.commit()
        connection.close()


@app.route("/")
def home():
    create_table()

    connection = sqlite3.connect("dictionary.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM words")
    word_rows = cursor.fetchall()
    connection.close()

    return render_template("table.html", rows=word_rows)


if __name__ == "__main__":
    app.run()
