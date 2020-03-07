import requests
import time
from typing import Dict, List, Tuple, Any
import sqlite3
import feedparser
import pandas as pd
import plotly.graph_objects as pg
import geopy
from geotext import GeoText


# import ipywidgets


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


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS JobDatabase(
                id TEXT PRIMARY KEY ,
                types TEXT  ,
                url TEXT NOT NULL ,
                created_at TEXT ,
                company TEXT ,
                location TEXT ,
                title TEXT NOT NULL ,
                description TEXT NOT NULL
                );''')


def populate_db(cursor: sqlite3.Cursor, githubdata, stackjobsdata):
    for job in githubdata:
        cursor.execute('INSERT or IGNORE INTO JobDatabase VALUES (?,?,?,?,?,?,?,?)',
                       [job['id'], job['type'], job['url'], job['created_at'], job['company'], job['location'],
                        job['title'], job['description']])
    for job in stackjobsdata:
        cursor.execute('INSERT or IGNORE INTO JobDatabase (id, title, url, description) VALUES (?,?,?,?)',
                       [job['id'], job['title'], job['link'], job['description']])


'''def add_data_github_db(cursor: sqlite3.Cursor, data):
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
                       [i['id'], i['type'], i['url'], i['created_at'], i['company'], i['location'], i['title'], i['description']])""" '''


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
        cursor.execute(insert_statement, [job_info['id'], job_info['link'], job_info['title'], job_info['description']])


def hard_code_save_to_db_github(cursor: sqlite3.Cursor, all_github_jobs: List[Dict[str, Any]]):
    # in the insert statement below we need one '?' for each column, then we will use a second param with each of the
    # values when we execute it. SQLITE3 will do the data sanitization to avoid little bobby tables style problems
    insert_statement = f"""INSERT OR IGNORE INTO hardcode_github_jobs(
        id, type, url, created_at, company, company_url, location, title, description, how_to_apply, company_logo)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)"""
    for job_info in all_github_jobs:
        # first turn all the values from the jobs dict into a tuple
        data_to_enter = tuple(job_info.values())
        cursor.execute(insert_statement, data_to_enter)


def github_job_locations(cursor: sqlite3.Cursor, data):
    geolocator = geopy.Nominatim(user_agent="api_jobs.py")

    for item in data:
        location = geolocator.geocode(item["location"])
        if location == "remote" or location == "Remote" or location is None or location.longitude is None \
                or location.latitude is None:
            continue
        job_location = item["location"]
        job_title = item["title"]
        company_name = item["company"]
        latitude = location.latitude
        longitude = location.longitude
        cursor.execute(f'''INSERT INTO JobLocations(title, location, company, latitude, longitude) VALUES (?,?,?,?,?)
                        ''', (job_title, job_location, company_name, latitude, longitude))


def stackoverflow_job_locations(cursor: sqlite3.Cursor, stackjobsdata):
    geolocator = geopy.Nominatim(user_agent="api_jobs.py")
    debug_count = 0
    for job in stackjobsdata:
        cities = GeoText(job.title)
        debug_count = debug_count + 1
        print(debug_count)
        location = geolocator.geocode(cities.cities, timeout=15)
        if location == "remote" or location == "Remote" or location is None:
            continue
        else:
            word = location.address
            worddiv = word.split(', ')
            cursor.execute(
                f'''INSERT INTO JobLocations(title, location, company, latitude, longitude) VALUES (?,?,?,?,?)
                        ''', (job.title, worddiv[0], job.author, location.latitude, location.longitude))


def setup_locations_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS JobLocations(
                        company TEXT ,
                        location TEXT ,
                        title TEXT, 
                        latitude REAL NOT NULL ,
                        longitude REAL NOT NULL
                        );''')


def make_map(db_name):
    con = sqlite3.connect(db_name)
    df = pd.read_sql_query("SELECT * from JobLocations", con)
    df['text'] = df['title'] + ', ' + df['company'] + ', ' + df['location']

    fig = pg.Figure(data=pg.Scattergeo(
        lon=df['longitude'],
        lat=df['latitude'],
        text=df['text'],
        mode='markers',
    ))

    fig.update_layout(
        title='GitHub & StackOverflow Jobs Available Currently in the United States',
        geo_scope='usa',
    )
    fig.show()


def main():
    # Open the database
    db_name = 'reworked.sqlite'
    conn, cursor = open_db(db_name)

    # Create the two tables
    # GitHub Jobs
    github_data = get_github_jobs_data()
    # Save the Data
    save_data(github_data)
    # Stack Overflow Jobs
    stack_data = get_stack_overflow_jobs_data()
    # save the stack overflow data
    save_data(stack_data)
    setup_db(cursor)
    populate_db(cursor, github_data, stack_data)

    count = 0
    # setup_locations_db(cursor)
    # github_job_locations(cursor,github_data)
    # stackoverflow_job_locations(cursor,stack_data)
    conn.commit()
    close_db(conn)
    conn, cursor = open_db(db_name)
    setup_locations_db(cursor)
    github_job_locations(cursor, github_data)
    stackoverflow_job_locations(cursor, stack_data)
    conn.commit()
    close_db(conn)

    make_map(db_name)


if __name__ == '__main__':
    main()
