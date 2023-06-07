import streamlit as st
import pandas as pd
import numpy as np

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils_prive import load_customer_used_record_data
from utils_prive import creat_new_directory

def hex_format(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)

def choose_service(df):
    curc_list = list(df.groupby('item_name').count().index) 
    # genre = st.radio("", curc_list)
    genre = st.selectbox('เลือกบริการ',curc_list)
    return genre

def display_cutomer(customer_df, item_name, expired_dt, full_couse_num):
    st.markdown(f"บริการที่ลูกค้าซื้อ : **:green[{item_name}]**")
    st.markdown(f"จำนวน : **:green[{full_couse_num}]**")
    st.markdown(f"วันหมดอายุ : **:green[{expired_dt}]**")
    st.divider()
    st.markdown(f"หมายเลข HN : **:green[{hn_id}]**")
    st.markdown(f"ชื่อ :green[{customer_df['name']}]  \tนามสกุล  :green[{customer_df['last_name']}]")    
    st.markdown(f"เพศ :green[{customer_df['sex']}]  วันเกิด **:green[{customer_df['dob']}]**")
    st.markdown(f"เบอร์โทร : :green[{customer_df['tel']}]  email : :green[{customer_df['email']}]")
    
        
###  Main
st.set_page_config(layout="wide")

st.title('รายการซื้อบริการของลูกค้า')
today =  date(2023,3,10)#date.today()
st.write(time.strftime('%X - %x'))
# customer_record_df = load_customer_profile_data()
creat_new_directory("./database/customer_product_record/")

# Customer Product Record
try:
    customer_product_record_df = pd.read_csv(f"./database/customer_product_record/customer_product_record_{date.today()}_data.csv")
except:
    customer_product_record_df = pd.read_csv(f"./database/customer_product_record/customer_product_record_data.csv")
    customer_product_record_df['active_status'] = True
    activ = customer_product_record_df['expired_dt'] < str(date.today())
    customer_product_record_df.loc[activ,'active_status'] = False
    # customer_product_record_df['status'] = 'excel'
    # customer_product_record_df['expired_dt'] = None

# Customer Profile Load
try:
    customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_{date.today()}_data.csv")
    st.success('Load from lasted updated file')
except:
    customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_data.csv")
    st.warning('No updated file today...')

# Product
try:
    product_category_df = pd.read_csv(f"./database/product_category/product_category_{date.today()}_data.csv")
except:
    product_category_df = pd.read_csv(f"./database/product_category/product_category_data.csv")

st.divider()
st.subheader(f'เพิ่มข้อมูลการใช้บริการลูกค้า ')

show_flag = False
hn_id = '57035'
product_list = 'ยังไม่ได้ระบุ'
customer_df = pd.DataFrame()
col1,_, col2 = st.columns([0.5,0.1,0.5])

with col1:
    item_name = None
    item_name = choose_service(product_category_df)
    full_couse_num  = st.text_input('จำนวน Couse ทั้งหมดที่ลูกค้าได้รับ (ครั้ง)', 1)
    expired_dt = st.date_input("วันหมดอายุ (ค.ศ.)", date.today())
    st.divider()

    hn_id = st.text_input('ค้นหาข้อมูลลูกค้าด้วย HN_number : [xx,xxx]', 57035)
    if st.button('ค้นหาข้อมูลลูกค้า'):
        customer_df = customer_profile_df[customer_profile_df['hn'] == int(hn_id)]
        if customer_df.shape[0]>0:
            show_flag = True
            customer_df = customer_df.iloc[0,:]
        else:
            st.warning('ไม่พบข้อมูลลูกค้า')
    
with col2:
    if show_flag:
        display_cutomer(customer_df,item_name,expired_dt,full_couse_num)
    
service_row = {
                'hn'    : hn_id,
                'item_name' : item_name,
                'status' : 'test',
                'num_fullcourse' : int(full_couse_num),
                'expired_dt': expired_dt.strftime('%Y-%m-%d'), 
                'buy_dt': date.today().strftime('%Y-%m-%d'),
                'active_status': True
            }

col = st.columns(3)[1]  # use an odd number and pick the middle element
if col.button('ยืนยันการเพิ่มข้อมูลลูกค้า'):
    
    customer_product_record_df = customer_product_record_df.append(service_row,ignore_index=True)
    st.dataframe(customer_product_record_df.sort_values('buy_dt',ascending=False))
    customer_product_record_df.to_csv(f"./database/customer_product_record/customer_product_record_{date.today()}_data.csv",header = True,index = False)
    customer_product_record_df.to_csv(f"./database/customer_product_record/customer_product_record_data.csv",header = True,index = False)
        
    st.success('การเพิ่มข้อมูลเสร็จสมบูรณ์')
    st.balloons()

st.divider()
st.write(time.strftime('%X - %x'))
st.dataframe(customer_product_record_df.sort_values('buy_dt',ascending=False),height=300, width=1000)

