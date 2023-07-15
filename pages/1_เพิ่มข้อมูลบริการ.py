import streamlit as st
import pandas as pd
import os

import psycopg2
import psycopg2.extras as extras

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils_prive import get_product_category , save_product_category


###  Main
st.set_page_config(layout="wide")
st.header(f'เพิ่มข้อมูลบริการ')
product_category_df = get_product_category()
with st.container():
    col11,col12,col13 = st.columns([0.6,0.3,0.2])
    with col11:
        item_name = st.text_input('ชื่อบริการ', '')
    with col12:
        duration_unit = st.selectbox('หน่วย',('DAY', 'WEEK', 'MONTH'))
    with col13:
        duration = st.text_input(f'ระยะเวลา({duration_unit})', '')
    
    item = {}
    if st.button('เพิ่มข้อมูล'):
        item = {
            'item_name'    : item_name,
            'duration' : duration,
            'duration_unit' : duration_unit,
            'start_dt': str(date.today()),
            'active_status': True
        }
        item_df = pd.DataFrame.from_dict(item,orient='index').T
        product_category_df  = pd.concat([product_category_df,item_df],axis=0, ignore_index=True)
        save_product_category(product_category_df)
        st.balloons()

with st.container():
    st.subheader(f'รายการบริการ (แก้ไขได้)')
    st.write(time.strftime('%X - %x'))
    product_category_df  = get_product_category()
    edited_df = st.data_editor(product_category_df.sort_values('start_dt',ascending=False), height=500, width=800)
    if st.button('บันทึกการเปลี่ยนแปลง'):
        st.balloons()
        save_product_category(edited_df)
