import streamlit as st
import pandas as pd
import numpy as np

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

import utils_prive 
from utils_prive import creat_new_directory


def choose_service(df):
    curc_list = list(df.groupby('item_name').count().index) 
    # genre = st.radio("", curc_list)
    genre = st.selectbox('เลือกบริการ',curc_list)
    return genre

def display_cutomer(customer_df, item_name, expired_dt, full_couse_num):
    st.divider()
    col11,col12 = st.columns(2)
    with col11:
        st.markdown(f"บริการที่ลูกค้าซื้อ : **:green[{item_name}]**")
        st.markdown(f"จำนวน : **:green[{full_couse_num}]**")
        st.markdown(f"วันหมดอายุ : **:green[{expired_dt}]**")
    with col12:
        st.markdown(f"หมายเลข HN : **:green[{hn_id}]**")
        st.markdown(f"ชื่อ :green[{customer_df['name']}]  \tนามสกุล  :green[{customer_df['last_name']}]")    
        st.markdown(f"เพศ :green[{customer_df['sex']}]  วันเกิด **:green[{customer_df['dob']}]**")
        st.markdown(f"เบอร์โทร : :green[{customer_df['tel']}]  email : :green[{customer_df['email']}]")
      
###  Main
st.set_page_config(layout="wide")
st.title('รายการซื้อบริการของลูกค้า')
today =  date.today()
st.write(time.strftime('%X - %x'))

creat_new_directory("./database/customer_product_record/")
# Customer Product Record
customer_product_record_df = utils_prive.get_customer_product_record()

# Customer Profile Load
customer_profile_df = utils_prive.get_customer_profile()

# Product
product_category_df = utils_prive.get_product_category()

st.divider()
status = utils_prive.choos_status()

hn_id = '57035'
product_list = 'ยังไม่ได้ระบุ'
customer_df = pd.DataFrame()
col1,_, col2 = st.columns([0.5,0.1,0.5])

with col1:
    st.subheader(f'เพิ่มข้อมูลการใช้บริการลูกค้า ')
    item_name = None
    item_name = choose_service(product_category_df)
    col11,col12 = st.columns(2)
    with col11:
        full_couse_num  = st.text_input('จำนวน Couse ทั้งหมดที่ลูกค้าได้รับ (ครั้ง)', 1)
    with col12:
        buy_dt = st.date_input("วันที่ซื้อบริการ (ค.ศ.)", date.today()).strftime('%Y-%m-%d')
        expired_dt = st.date_input("วันหมดอายุ (ค.ศ.)", buy_dt+relativedelta(months=36)).strftime('%Y-%m-%d')
st.divider()

with col2:
    st.subheader(f'ค้นหาข้อมูลลูกค้า')
    hn_id = st.text_input('HN_number : [xx,xxx]', )
    col21,col22 = st.columns(2)
    with col21:
        hn_name = st.text_input('ชื่อ', '')
    with col22:
        hn_lastname = st.text_input('นามสกุล', '')
    
    # if st.button('ค้นหาข้อมูลลูกค้า'):
    customer_df = customer_profile_df[(customer_profile_df['hn'].astype('string').str.contains(hn_id)) & (customer_profile_df['name'].str.lower().str.contains(hn_name.lower()))]
    customer_df = customer_df[(customer_profile_df['last_name'].fillna('Not define').str.lower().str.contains(hn_lastname.lower()))]
st.dataframe(customer_df)
     
with st.container():
    if customer_df.shape[0]>0:
        customer_df = customer_df.iloc[0,:]
        hn_id = customer_df['hn']
    else:
        st.warning('ไม่พบข้อมูลลูกค้า')
    
if customer_df.shape[0]>0:
    display_cutomer(customer_df,item_name,expired_dt,full_couse_num)
    
service_row = {
                'hn'    : int(hn_id),
                'item_name' : item_name,
                'status' : status,
                'num_fullcourse' : int(full_couse_num),
                'expired_dt': expired_dt.strftime('%Y-%m-%d'), 
                'buy_dt': buy_dt.strftime('%Y-%m-%d'),
                'active_status': True
            }


col = st.columns(3)[1]  # use an odd number and pick the middle element
if col.button('ยืนยันการเพิ่มข้อมูลลูกค้า'):
    customer_product_record_df = pd.concat([customer_product_record_df,pd.DataFrame.from_dict(service_row,orient='index').T], axis=0, ignore_index=True)
    customer_product_record_df.drop_duplicates(inplace = True)
    utils_prive.save_customer_product_record(customer_product_record_df)
    st.success('การเพิ่มข้อมูลเสร็จสมบูรณ์')
    st.balloons()

st.divider()
st.title('รายการการซื้อบริการทั้งหมด (แก้ไขได้)')
st.write(time.strftime('%X - %x'))
edited_df = st.data_editor(customer_product_record_df.sort_values('buy_dt',ascending=False), height=500,width=1100)
if st.button('บันทึกการเปลี่ยนแปลง'):
    utils_prive.save_customer_product_record(edited_df)
    st.success('บันทึกเสร็จสมบูรณ์')
    st.balloons()
   
