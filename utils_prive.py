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

def hex_format(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)

def choos_status():
    option = st.sidebar.selectbox(
    'Input type',
    ('staff', 'test'))
    return
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

# Get Data 
def get_product_category():
    product_category_df = pd.read_csv(f"./database/product_category/product_category_data.csv")
        
    return product_category_df.drop_duplicates()

def get_customer_profile():
    # Customer Profile Load
    customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_data.csv")
    return customer_profile_df.drop_duplicates()

def get_customer_used_record():
    customer_used_record_df = pd.read_csv(f"./database/customer_used_record/customer_used_record_data.csv")
    return customer_used_record_df.drop_duplicates()
    
def get_customer_product_record():
    customer_product_record_df = pd.read_csv(f"./database/customer_product_record/customer_product_record_data.csv")
    customer_product_record_df['active_status'] = True
    activ = customer_product_record_df['expired_dt'] < str(date.today())
    customer_product_record_df.loc[activ,'active_status'] = False
    return customer_product_record_df.drop_duplicates()


# Save Data

def save_new_used_record2db(used_row):
    customer_used_record_df = get_customer_used_record()
    customer_used_record_df = customer_used_record_df.append(used_row,ignore_index=True).sort_values('next_date',ascending=False)
    customer_used_record_df.to_csv(f"./database/customer_used_record/backup/customer_used_record_{date.today().strftime('%Y-%m-%d')}_data.csv",header = True,index = False,encoding="utf-8-sig")
    customer_used_record_df.to_csv(f"./database/customer_used_record/customer_used_record_data.csv",header = True,index = False,encoding="utf-8-sig")

def save_customer_used_record(customer_used_record_df):
    customer_used_record_df.to_csv(f"./database/customer_used_record/backup/customer_used_record_{date.today().strftime('%Y-%m-%d')}_data.csv",header = True,index = False,encoding="utf-8-sig")
    customer_used_record_df.to_csv(f"./database/customer_used_record/customer_used_record_data.csv",header = True,index = False,encoding="utf-8-sig")
     
def save_product_category(product_category_df):
    product_category_df.to_csv(f"./database/product_category/backup/product_category_{date.today().strftime('%Y-%d')}_data.csv",header = True,index = False, encoding="utf-8-sig")
    product_category_df.to_csv(f"./database/product_category/product_category_data.csv",header = True,index = False, encoding="utf-8-sig")
        
def save_customer_profile(customer_profile_df):
    customer_profile_df.to_csv(f"./database/customer_profile/backup/customer_profile_{date.today().strftime('%Y-%d')}_data.csv",header = True,index = False, encoding="utf-8-sig")
    customer_profile_df.to_csv(f"./database/customer_profile/customer_profile_data.csv",header = True,index = False, encoding="utf-8-sig")

def save_customer_product_record(customer_product_record_df):
    customer_product_record_df.to_csv(f"./database/customer_product_record/backup/customer_product_record_{date.today().strftime('%Y-%d')}_data.csv",header = True,index = False, encoding="utf-8-sig")
    customer_product_record_df.to_csv(f"./database/customer_product_record/customer_product_record_data.csv",header = True,index = False, encoding="utf-8-sig")
    