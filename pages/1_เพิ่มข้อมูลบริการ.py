import streamlit as st
import pandas as pd
import os

import psycopg2
import psycopg2.extras as extras

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils_prive import load_product_category_data, creat_new_directory

def postgresql_connect():
    # specify user/password/where the database is
    sqluser = 'postgres'
    sqlpass = 'KAPOONman2535!'
    dbname = 'prive-datastore'
    
    try:
        host =  'localhost' 
        con = psycopg2.connect(dbname=dbname, user=sqluser, password=sqlpass, host=host)
    except:
        st.warning('172.20.10.13')
        host =  '172.20.10.13' 
        con = psycopg2.connect(dbname=dbname, user=sqluser, password=sqlpass, host=host)
        st.warning('172.20.10.13 complete')
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

def get_product_category():
    # Product
    try:
        product_category_df = pd.read_csv(f"./database/product_category/product_category_{date.today()}_data.csv")
        st.success('Load from lasted updated file')
    except:
        product_category_df = pd.read_csv(f"./database/product_category/product_category_data.csv")
        st.warning('No updated file today...')
    return product_category_df.drop_duplicates()


def hex_format(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)


###  Main
st.set_page_config(layout="wide")

st.title('รายการบริการ (แก้ไขได้)')

st.write(time.strftime('%X - %x'))
# customer_record_df = load_customer_profile_data()
# creat_new_directory("./database/customer_profile/")

product_category_df = get_product_category()

edited_df = st.experimental_data_editor(product_category_df.sort_values('start_dt',ascending=False), height=500, width=800)
if st.button('บันทึกการเปลี่ยนแปลง'):
    st.balloons()
    edited_df.to_csv(f"./database/product_category/product_category_{date.today()}_data.csv",header = True,index = False)
    edited_df.to_csv(f"./database/product_category/product_category_data.csv",header = True,index = False)

