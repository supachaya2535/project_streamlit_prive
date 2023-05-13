import streamlit as st
import pandas as pd
import os

import psycopg2
import psycopg2.extras as extras

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

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


#@st.cache_data 
def load_customer_record_data():
    today = date.today() # date(2023,5,12) #
    path = f"data_cach/product_category_{str(today)}.csv"
    try:
        con = postgresql_connect()
        query = """select  * 
                    from product_category
                    """
        df = pd.read_sql_query(query,con)
        
        isExist = os.path.exists(path)
        if not isExist:
            df.to_csv(path,header = True,index = False)
        
    except:
        st.write('Load data from cach ....')
        df = pd.read_csv(path)
    return df


def hex_format(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)


###  Main
st.set_page_config(layout="wide")

st.title('รายการบริการ')
customer_record_df = load_customer_record_data()

st.dataframe(customer_record_df,height=1000)
