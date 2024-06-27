import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
import os
import random
import numpy as np
import re
import csv
from dotenv import load_dotenv

#global variable

loc_data = "../data"
load_dotenv()

password = os.getenv("password")

def creating_database(db_name:str) -> None:

    """
    Function to create a database in PostgreSQL.

    This function demonstrates how to create a new database in PostgreSQL using psycopg2.
    """
    try:
        conn = psycopg2.connect(f"dbname= 'postgres' user= 'postgres' host = 'localhost' password= '{password}'")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        try:
            cur.execute(f"CREATE DATABASE {db_name};")
            print("Database created successfully.")

            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()  
            
        except psycopg2.Error as e:
            raise e 

    except psycopg2.Error as e:
        raise e


def create_schema(db_name:str) -> None:
    try:
        conn = psycopg2.connect(f"dbname= '{db_name}' user= 'postgres' host = 'localhost' password= '{password}'")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        try:
            # Read SQL file
            with open('./Schema.sql', 'r') as file:
                sql_statements = file.read()
                # Execute SQL statements
                print(sql_statements)
                cur.execute(sql_statements)
                # Commit the transaction
                conn.commit()

                # Close the cursor and connection
                cur.close()
                conn.close()

        except psycopg2.Error as e:
            raise e

    except psycopg2.Error as e:
        raise e


def count_rows(file_name):
    print(file_name)
    with open(file_name, 'r', newline='', ) as file:
        reader = csv.reader(file)
        row_count = sum(1 for row in reader)
    return row_count


def choose_csv_files(file_name:str = None) -> list[str]:
    """
    select all csv filer or single csv file in data file
    return list of file name(s)
    """

    csv_list = os.listdir(loc_data)
    # assume that all files are csv

    row_counts = {the_file: count_rows(os.path.join(loc_data, the_file)) for the_file in csv_list}

    sorted_files = sorted(csv_list, key=lambda the_file: row_counts[the_file])

    if file_name is None:
        return sorted_files

    else:
        if file_name in sorted_files:
            return [file_name]
        else:
            raise Exception("file name not found")

def extract_csvs(db_name: str, file_name:str = None) -> list:
    """
    Function to extract value of csv into list 

    """
    csv_to_extract = choose_csv_files(file_name)

    try:
        conn = psycopg2.connect(f"dbname= '{db_name}' user= 'postgres' host = 'localhost' password= '{password}'")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cur = conn.cursor()

        for single_file in csv_to_extract:

            df = pd.read_csv(f"{loc_data}/{single_file}")

            table_columns =list(df.columns)

            table_name = single_file[:-4]

            for index,row in df.iterrows():

                insert_value = np.array2string((row.values), separator = ',')[1:-1].replace("nan", "NULL").replace('"',"'")
                
            

                pattern = r"(?<!,|\s)'(?!,|$)"

                modi_insert_value = re.sub(pattern, "''", insert_value)

                sql_insert_statement = f"INSERT INTO {table_name} ({', '.join(table_columns)}) VALUES({modi_insert_value})"

                print(sql_insert_statement)
                cur.execute(sql_insert_statement)

        conn.commit()
        # Close the cursor and connection
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        raise e

if __name__ == '__main__':

    # storing the directory of a module in 
    dir = os.path.dirname(__file__)
    os.chdir(dir)

    # creating_database()
    database_name = "bike_store_db"
    # creating_database(database_name)
    create_schema(database_name)
    extract_csvs(database_name)
