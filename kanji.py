import pandas as pd
import sqlite3
import unicodedata


# Function to create the kanji table
def create_kanji_table():
    connection = sqlite3.connect("kanji.db")  # Create a separate database for kanji
    cursor = connection.cursor()

    # Create a table for kanji if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS kanji (
        kanji TEXT PRIMARY KEY,
        meaning TEXT,
        radical TEXT
    )''')

    connection.commit()
    connection.close()


# Function to populate the kanji table from the DataFrame
def populate_kanji_table(dfw):
    connection = sqlite3.connect("kanji.db")  # Use the separate database for kanji
    cursor = connection.cursor()

    for index, row in dfw.iterrows():
        kanji = row["kanji"]
        meaning = row["kmeaning"]
        radical = unicodedata.normalize("NFKC", row["radical"])

        # Insert data into the kanji table
        cursor.execute("INSERT OR REPLACE INTO kanji (kanji, meaning, radical) VALUES (?, ?, ?)",
                       (kanji, meaning, radical))

    connection.commit()
    connection.close()


# Function to print the kanji table
def print_kanji_table():
    # Connect to the SQLite database
    connection = sqlite3.connect("kanji.db")
    cursor = connection.cursor()

    # Execute a SELECT query to fetch data from the kanji table
    cursor.execute("SELECT * FROM kanji")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Print the table header
    print("Kanji\t\tMeaning\t\tRadical")

    # Print each row of the table
    for row in rows:
        kanji, meaning, radical = row
        print(f"{kanji}\t\t{meaning}\t\t{radical}")

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    create_kanji_table()
    dfw = pd.read_csv("https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/ka_data.csv")
    populate_kanji_table(dfw)

    print_kanji_table()
