import streamlit as st
import inspect
import textwrap
import os

import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import psycopg2
import psycopg2.extras as extras

PROJECT = 'project_streamlit_prive'

#SQL
def postgresql_connect():
    # specify user/password/where the database is
    sqluser = 'postgres'
    sqlpass = 'KAPOONman2535!'
    dbname = 'prive-datastore'
    schema_name = 'someschema'
    host = 'localhost'

    query_schema = 'SET search_path to ' + schema_name + ';'

    # connect to the database
    con = psycopg2.connect(dbname=dbname, user=sqluser, password=sqlpass, host=host)
    return con
  
def insert_df2postgresql(conn, df, table):
  
    tuples = [tuple(x) for x in df.to_numpy()]
  
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("the dataframe is inserted")
    cursor.close()

def create_table(sql,conn):
    cur = conn.cursor()
    cur.execute(sql)
    # try:
    #     cur.execute(sql)
    # except:
    #     print("I can't drop our test database!")

    conn.commit() # <--- makes sure the change is shown in the database
    conn.close()
    cur.close()
  
# Directory
def creat_new_directory(prefix_path):
    today = datetime.today()
    path = prefix_path
    
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print(f"The new directory {path} is created!")
    else:
        print(f"The {path} directory is already exist!")
    return path

# Data
def load_product_category_data():
    con = postgresql_connect()
    query = """select  * 
                from product_category
                """
    df = pd.read_sql_query(query,con)
    
    return df

def load_customer_profile_data():
    con = postgresql_connect()
    query = """select  * 
                from customer_profile
                """
    df = pd.read_sql_query(query,con)
    
    return df

def load_customer_used_record_data():
    con = postgresql_connect()
    query = """select  * 
                from customer_used_record
                """
    df = pd.read_sql_query(query,con)
    
    return df
    
def load_customer_product_record_data():
    con = postgresql_connect()
    query = """select  * 
                from customer_product_record
                """
    df = pd.read_sql_query(query,con)
    
    return df


    