import pandas as pd
import sqlite3
import unicodedata
import math


# Function to create the radicals table
def create_radicals_table():
    connection = sqlite3.connect("radicals.db")  # Create a separate database for radicals
    cursor = connection.cursor()

    # Create a table for radicals if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS radicals (
        radical TEXT PRIMARY KEY,
        meaning TEXT,
        radical_image_url TEXT,
        radical_mnemonic_url TEXT
    )''')

    connection.commit()
    connection.close()


# Function to populate the radicals table from the DataFrame
def populate_radicals_table(dfr):
    connection = sqlite3.connect("radicals.db")  # Use the separate database for radicals
    cursor = connection.cursor()

    for index, row in dfr.iterrows():
        radical = unicodedata.normalize("NFKC", row["Radical"])
        meaning = row["Meaning"]

        print(meaning, type(meaning))

        if isinstance(meaning, float) and math.isnan(meaning):
            meaning = ""
            radical_image_url = ""
            radical_mnemonic_url = ""

        else:
            romanji_reading = row["Reading-R"]
            # Generate radical image URLs
            radical_image_url = f"https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/{romanji_reading}2.svg"
            radical_mnemonic_url = f"https://raw.githubusercontent.com/leonardo-blas/kanji-alive-data-media/master/radical-animations/{romanji_reading}0.svg"


        # Insert data into the radicals table
        cursor.execute(
            "INSERT OR REPLACE INTO radicals (radical, meaning, radical_image_url, radical_mnemonic_url) VALUES (?, ?, ?, ?)",
            (radical, meaning, radical_image_url, radical_mnemonic_url))

    connection.commit()
    connection.close()


# Function to print the radicals table
def print_radicals_table():
    # Connect to the SQLite database
    connection = sqlite3.connect("radicals.db")
    cursor = connection.cursor()

    # Execute a SELECT query to fetch data from the radicals table
    cursor.execute("SELECT * FROM radicals")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Print the table header
    print("Radical\tMeaning\tRadical Image URL\tRadical Mnemonic URL")

    # Print each row of the table
    for row in rows:
        radical, meaning, radical_image_url, radical_mnemonic_url = row
        print(f"{radical}\t{meaning}\t{radical_image_url}\t{radical_mnemonic_url}")

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    create_radicals_table()
    dfr = pd.read_csv(
        "https://raw.githubusercontent.com/kanjialive/kanji-data-media/master/language-data/japanese-radicals.csv")
    populate_radicals_table(dfr)

    print_radicals_table()
