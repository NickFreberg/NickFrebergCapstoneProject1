import requests
import time
from typing import Dict, List, Tuple, Any
import sqlite3
import feedparser


def get_github_jobs_data() -> List[Dict]:
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


def get_stack_overflow_jobs_data() -> List[Dict]:
    """retrieve jobs from Stack Overflow data and turns it into a dict"""
    stack_overflow_data = feedparser.parse("https://stackoverflow.com/jobs/feed").entries
    # stackjobdata['title']['link']['description']['location']['category']
    # checks to make sure feedparser is getting correct information
    # for post in stack_job_data.entries:
    # print("post location: " + post.location)
    # print("post link: " + post.link)
    # print("post title: " + post.title)

    return stack_overflow_data


def save_data(data, filename='jsonderulo.txt'):
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


def setup_db_GitHub(cursor: sqlite3.Cursor):
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


def setup_db_Stack_Overflow(cursor: sqlite3.Cursor):
    # Create the Table of Stack Overflow Jobs
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS Stack_Overflow_Jobs (
    id TEXT PRIMARY KEY ,
    types TEXT NOT NULL,
    url TEXT NOT NULL ,
    created_at TEXT NOT NULL ,
    company TEXT NOT NULL ,
    location TEXT NOT NULL ,
    title TEXT NOT NULL ,
    description TEXT NOT NULL
    );''')


"""def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS JobDatabase(
                id TEXT PRIMARY KEY ,
                types TEXT NOT NULL  ,
                url TEXT NOT NULL ,
                created_at TEXT NOT NULL ,
                company TEXT NOT NULL ,
                location TEXT NOT NULL ,
                title TEXT NOT NULL ,
                description TEXT NOT NULL
                );''')"""



def add_data_github_db(cursor: sqlite3.Cursor, data):
    """conn,cursor = open_db("jobs_db.db")

    sql = ('INSERT INTO GitHub_Jobs (id, type , url, created_at, company, company_url, title, description)\n'
           '    VALUES (?,?,?,?,?,?,?,?), ')

    cur = conn.cursor()
    cur.execute(sql, entry)
    return cur.lastrowid"""

    for i in data:
        cursor.execute('INSERT or IGNORE INTO hardcode_github_jobs VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                       [i['id'], i['type'], i['url'], i['created_at'], i['company'], i['company_url'], i['location'], i['title'], i['description'], i['how_to_apply'], i['company_logo']])


def add_data_stack_db(cursor: sqlite3.Cursor, data):
    for i in data:
        print(i)
        """cursor.execute('INSERT or IGNORE INTO hardcode_stack_overflow_jobs VALUES (?,?,?,?,?,?,?,?)',
                       [i['id'], i['type'], i['url'], i['created_at'], i['company'], i['location'], i['title'], i['description']])"""


def hard_code_create_github_jobs_table(cursor: sqlite3.Cursor):
    create_statement = f"""CREATE TABLE IF NOT EXISTS hardcode_github_jobs(
    'id' TEXT,
    'type' TEXT,
    'url' TEXT,
    'created_at' TEXT,
    'company' TEXT NOT NULL,
    company_url TEXT,
    location TEXT,
    title TEXT NOT NULL,
    description TEXT,
    how_to_apply TEXT,
    company_logo TEXT
    );
        """
    cursor.execute(create_statement)


def hard_code_create_stack_jobs_table(cursor: sqlite3.Cursor):
    create_statement = f"""CREATE TABLE IF NOT EXISTS Stack_Overflow_Jobs(
    id TEXT NOT NULL PRIMARY KEY,
    link TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL
    
    
    ); """
    cursor.execute(create_statement)


def hard_code_save_to_stack_jobs_db(cursor: sqlite3.Cursor, all_stack_jobs: List[Dict[str, Any]]):
    insert_statement = f"""INSERT INTO Stack_Overflow_Jobs VALUES (?,?,?,?)"""
    for job_info in all_stack_jobs:
        cursor.execute(insert_statement,[job_info['id'], job_info['link'], job_info['title'], job_info['description']])

def hard_code_save_to_db_github(cursor: sqlite3.Cursor, all_github_jobs: List[Dict[str, Any]]):
    # in the insert statement below we need one '?' for each column, then we will use a second param with each of the values
    # when we execute it. SQLITE3 will do the data sanitization to avoid little bobby tables style problems
    insert_statement = f"""INSERT OR IGNORE INTO hardcode_github_jobs(
        id, type, url, created_at, company, company_url, location, title, description, how_to_apply, company_logo)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
    for job_info in all_github_jobs:
        # first turn all the values from the jobs dict into a tuple
        data_to_enter = tuple(job_info.values())
        cursor.execute(insert_statement, data_to_enter)


def main():
    # Open the database
    db_name = 'momentoftruth_electric_boogaloo.sqlite'
    conn, cursor = open_db(db_name)
    # Create the two tables
    #GitHub Jobs
    #github_data = get_github_jobs_data()
    # Save the Data
    #save_data(github_data)
    # Stack Overflow Jobs
    stack_data = get_stack_overflow_jobs_data()
    # save the stack overflow data
    save_data(stack_data)
    # Hard Code the Tables
    #hard_code_create_github_jobs_table(cursor)
    # add the data to the tables
    #add_data_github_db(cursor, github_data)
    # hard code save
    #hard_code_save_to_db_github(cursor, github_data)
    # create stack jobs
    hard_code_create_stack_jobs_table(cursor)
    add_data_stack_db(cursor, stack_data)
    hard_code_save_to_stack_jobs_db(cursor, stack_data)
    count = 0
    conn.commit()
    close_db(conn)


if __name__ == '__main__':
    main()
