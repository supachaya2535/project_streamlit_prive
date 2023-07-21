import streamlit as st
import pandas as pd
import numpy as np

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import utils_prive

def get_customer_used_record():
    # Customer used Record
    try:
        customer_used_record_df = pd.read_csv(f"./database/customer_used_record/customer_used_record_{date.today().strftime('%Y-%m')}_data.csv")
    except:
        customer_used_record_df = pd.read_csv(f"./database/customer_used_record/customer_used_record_data.csv")
        customer_used_record_df['status'] = 'excel'
    return customer_used_record_df.drop_duplicates()

def get_customer_profile():
    # Customer Profile Load
    try:
        customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_{date.today()}_data.csv")
        # st.success('Load from lasted updated file')
    except:
        customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_data.csv")
        # st.warning('No updated file today...')
    return customer_profile_df.drop_duplicates()

def rename_to_display(df):
    df.rename(columns={ 'hn': 'หมายเลข HN',
                        'name': 'ชื่อ',
                        'last_name': 'นามสกุล',
                        'item_name': 'บริการ',
                        'tel':'เบอร์โทร',
                        'txn_date': 'วันที่มาใช้บริการล่าสุด',
                        'next_date': 'วันที่นัดครั้งถัดไป',
                        'dob':'วันเกิด'
                    },inplace=True)
    return df

def rename_to_save(df):
    df.rename(columns={ 'หมายเลข HN':'hn' ,
                        'ชื่อ':'name' ,
                        'นามสกุล':'last_name' ,
                        'บริการ':'item_name' ,
                        'เบอร์โทร':'tel',
                        'วันที่มาใช้บริการล่าสุด':'txn_date' ,
                        'วันที่นัดครั้งถัดไป':'next_date' ,
                        'วันเกิด':'dob'
                    },inplace=True)
    return df

###  Main
st.set_page_config(layout="wide")

st.title('รายชื่อลูกค้าที่ต้องทำนัดตั้งแต่')
c1,c2 = st.columns(2)
with c1: strt_dt = st.date_input("วันที่เริ่มต้น", date.today())
with c2: end_dt = st.date_input("วันที่สิ้นสุด", date.today()+relativedelta(months=1))

st.text(f"{strt_dt}:{end_dt}")

next_df = utils_prive.get_customer_used_record()

next_df.sort_values('next_date',ascending=False,inplace=True)

next_df.drop_duplicates(ignore_index=True, subset = ['hn','item_name'], keep = 'first',inplace=True)

range_df = next_df[(next_df['next_date'].astype(str) >= strt_dt.strftime('%Y-%m-%d')) & (next_df['next_date'].astype(str) <= end_dt.strftime('%Y-%m-%d'))]

st.dataframe(rename_to_display(range_df), width=1100)

next_df = rename_to_display(next_df)

st.divider()
st.title('รายชื่อลูกค้าที่ต้องทำนัดทั้งหมด')

edited_df = st.data_editor(next_df.sort_values('วันที่นัดครั้งถัดไป',ascending=False), height=500,width=1100)
if st.button('บันทึกการเปลี่ยนแปลง'):
    edited_df = rename_to_save(edited_df)
    utils_prive.save_customer_used_record(edited_df)
