import sqlite3
import pandas as pd
import sys
import os
import importlib

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('..'))

import src.data_collection
importlib.reload(src.data_collection)
from src.data_collection import *

def store(df: pd.DataFrame, db: str, table: str):
    """
    Load data from a DataFrame into an SQLite database table.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be stored.
        db (str): The SQLite database file name.
        table (str): The name of the table to store the data.

    Returns:
        None
    """
    try:
        # Establish connection to the SQLite database
        con = sqlite3.connect(db)
        print(f"Connected to database: {db}")

        # Load data into the specified table
        df.to_sql(table, con, if_exists='replace', index=False)
        print(f"Data successfully stored in table '{table}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the database connection is closed
        if con:
            con.close()
            print("Database connection closed.")

