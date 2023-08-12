import streamlit as st
import pandas as pd
import numpy as np

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils_prive import  get_customer_profile, save_customer_profile
import utils_prive

###  Main
st.set_page_config(layout="wide")
status = utils_prive.choos_status()
st.title('เพิ่มข้อมูลส่วนตัวลูกค้า')
today =  date(2023,5,22)#date.today()
st.write(time.strftime('%X - %x'))

customer_profile_df = get_customer_profile()
st.dataframe(customer_profile_df)

max_hn = int(customer_profile_df['hn'].max())
with st.container():
    st.subheader(f'กรอกข้อมูลสำหรับลูกค้าใหม่')
    col1 ,col2 = st.columns(2)
    with col1:
        st.text(f'หมายเลข HN สูงสุดในฐานข้อมูลปัจจุบัน : {max_hn}')
    
        hn_id = st.text_input('หมายเลข HN สำหรับลูกค้าใหม่', '')
    
    col11,col12,col13 = st.columns([0.4,0.4,0.2])
    with col11:
        hn_name = st.text_input('ชื่อลูกค้า (*)', '')
    with col12:
        hn_last_name = st.text_input('นามสกุล (*)', '')
    with col13:
        hn_sex = st.selectbox('เพศ',('ชาย', 'หญิง', 'ไม่ระบุ'))

    col21, col22 ,col23 = st.columns([0.3,0.4,0.6])  
    with col21:
        hn_dob = st.date_input("วันเกิด (ค.ศ.)", date(999, 9, 9) )
    with col22: 
        hn_tel = st.text_input('เบอร์โทร', '')
    with col23:
        hn_email = st.text_input("e-mail", "")

st.divider()
with st.container():
    st.subheader(f'ที่อยู่ลูกค้าใหม่ :{str(hn_id)}')
    col1, col2  = st.columns([0.2,0.5])  
    with col1:
        hn_housenum = st.text_input('บ้านเลขที่', '-')
    with col2: 
        hn_building = st.text_input('ตึก/หมู่บ้าน', '-')
    

    col1, col2 ,col3 = st.columns([0.6,0.5,0.5])  
    with col1:
        hn_road = st.text_input('ถนน', '-')
    with col2: 
        hn_sub_district = st.text_input('ตำบล/เขต', '-')
    with col3:
        hn_district = st.text_input('อำเภอ/แขวง', '-')
    
    col1, col2,_ = st.columns([0.2,0.2,0.5])  
    with col1:
        hn_province = st.text_input('จังหวัด', '-')
    with col2:
        hn_zip = st.text_input('รหัสไปรษณีย์', '-')

done_flag = False 
summa_flag = False
hn_row = {}
if st.button('ยืนยันเพิ่มข้อมูลลูกค้า'):
    st.balloons()
    if(hn_name == '')|(hn_last_name == ''):
        st.warning('Please fill in required feild [ ชื่อ, นามสกุล, เบอร์โทร]')
    else:
        hn_row = {
            'hn'    : int(hn_id),
            'name' : hn_name,
            'last_name' : hn_last_name,
            'sex': hn_sex,
            'tel' : hn_tel,
            'dob' : hn_dob.strftime('%Y-%m-%d'),
            'status' : status,
            'email': hn_email, 
            'house_num' : hn_housenum,
            'building': hn_building, 
            'road' : hn_road, 
            'sub_district' : hn_sub_district, 
            'district' :hn_district, 
            'province': hn_province, 
            'zip_code' : hn_zip,
            'application_dt': date.today().strftime('%Y-%m-%d')
        }
        
        st.markdown(f"หมายเลข HN : **:green[{hn_id}]**")
        st.markdown(f'ชื่อ :green[{hn_name}]  \tนามสกุล  :green[{hn_last_name}]')    
        st.markdown(f'เพศ :green[{hn_sex}]  วันเกิด **:green[{hn_dob}]**')
        st.markdown(f'เบอร์โทร : :green[{hn_tel}]  email : :green[{hn_email}]')
        st.markdown(f'**:green[{hn_housenum}]**   **:green[{hn_building}]** \
                    \n**:green[{hn_road}]**\
                    \n**:green[{hn_sub_district}]**  **:green[{hn_district}]**  \
                    \n**:green[{hn_province}]**\
                    \n**:green[{hn_zip}]**')
        

        done_flag = True
        
        hn_df = pd.DataFrame.from_dict(hn_row,orient='index').T
        customer_profile_df = pd.concat([customer_profile_df,hn_df],axis=0, ignore_index=True)
        st.dataframe(customer_profile_df.sort_values('hn',ascending=False))
        save_customer_profile(customer_profile_df)
        st.success("เพิ่มข้อมูลสำเร็จ")
        st.balloons()
        done_flag = False
                        
st.divider()
st.header('ลูกค้าทั้งหมด (แก้ไขได้) : วันที่ yyyy-mm-dd')
st.write(time.strftime('%X - %x'))
with st.container():
    customer_profile_df = get_customer_profile()
    edited_df = st.data_editor(customer_profile_df.sort_values('hn',ascending=False), height=1000)
    if st.button('บันทึกการเปลี่ยนแปลง'):
        save_customer_profile(edited_df)
        st.balloons()