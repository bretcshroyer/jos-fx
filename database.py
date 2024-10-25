import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

def create_database(df):
    # Create a connection to a new SQLite database
    engine = create_engine('sqlite:///tickdata.db')

    # Create the table with the correct schema and primary key
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS price_data (
        time TEXT,
        instrument TEXT,
        granularity TEXT,
        volume REAL,
        o TEXT,
        h TEXT,
        l TEXT,
        c TEXT,
        PRIMARY KEY (time, instrument, granularity)
    )
    '''

    # Execute the create table query
    with engine.connect() as conn:
        conn.execute(text(create_table_query))

    # Insert the data from the DataFrame
    df.to_sql('price_data', engine, if_exists='append', index=False)

    print("Database created and data successfully stored.")

