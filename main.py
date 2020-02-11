import requests
import time
from typing import Dict, List, Tuple
import sqlite3


def get_data() -> List[Dict]:
    """retrieve github jobs data and turns it into a dict"""
    data = []
    more_data = True
    json_url = "https://jobs.github.com/positions.json?page="
    current_page = 0
    max_entries = 50
    while more_data:
        current_page += 1
        pageurl = json_url + str(current_page)
        pgres = requests.get(pageurl)
        # check if you can receive data from
        if pgres.status_code == 200:
            page_json = pgres.json()
            data.extend(page_json)
            if len(page_json) < 50:
                more_data = False
            time.sleep(.1)  # short sleep between requests so I dont wear out my welcome.
        return data


def save_data(data, filename='jsonderulo.txt',):
    """Saves Data to a file"""
    with open(filename, 'a', encoding='utf-8') as file:
        for item in data:
            print(item, file=file)


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    # Create the Table of GitHub Jobs
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS GitHub_Jobs (
    "id" TEXT NOT NULL PRIMARY KEY ,
    "type"	TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "created_at" TEXT NOT NULL,
    "company" TEXT NOT NULL,
    "company_url" TEXT NOT NULL,
    "title"	TEXT NOT NULL,
    "description" TEXT NOT NULL,
    PRIMARY KEY("id")
    );''')


def add_to_db(conn, cursor:sqlite3.Cursor, entry):

    sql = '''INSERT INTO GitHub_Jobs (id, type , url, created_at, company, company_url, title, description)
    VALUES (?,?,?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, entry)
    return cur.lastrowid


def main():
    # Open the database
    conn, cursor = open_db("jobs_db.db")
    # Create the GitHub Jobs Table in the database
    setup_db(cursor)
    data = get_data()
    print(data)
    save_data(data)
    print(type(conn))

    count = 0
    """I used this line beneath to test getting a parameter from an entry. 
    This was helpful when putting the data into the db"""
    for i in range(len(data)):
        entry = data[i]
        count += 1
        add_to_db(conn, cursor, entry)
        print("successfully added ", count, " entries.")

    conn.commit()
    close_db(conn)


if __name__ == '__main__':
    main()
