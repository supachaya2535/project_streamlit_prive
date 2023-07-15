import streamlit as st
import pandas as pd
import numpy as np

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils_prive
from utils_prive import save_new_used_record2db

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

def choose_service(df):
    active_df = df[df['active_status']]
    curc_list = list(active_df.groupby('item_name').count().index) 
    genre = st.selectbox('เลือกบริการ',curc_list)
    return genre

def display_cutomer(customer_df):
    st.markdown(f"หมายเลข HN : **:green[{customer_df['hn']}]**")
    st.markdown(f"ชื่อ :green[{customer_df['name']}]")
    st.markdown(f"นามสกุล  :green[{customer_df['last_name']}]")    
    st.markdown(f"เพศ :green[{customer_df['sex']}]")
    st.markdown(f"วันเกิด :green[{customer_df['dob']}]")
    st.markdown(f"เบอร์โทร : :green[{customer_df['tel']}]  ")
    st.markdown(f"email : :green[{customer_df['email']}]")

def display_service( item_name, used_couse_num):
    st.markdown(f"บริการที่ลูกค้าใช้ : :green[{item_name}]")
    st.markdown(f"จำนวนที่ใช้ : :green[{used_couse_num}]")

def add_used_record2db():
    customer_product_record_df = utils_prive.get_customer_product_record()
    product_category_df = utils_prive.get_product_category()
    customer_profile_df = utils_prive.get_customer_profile()
    customer_used_record_df = utils_prive.get_customer_used_record()

    col1,_, col2 = st.columns([0.5,0.1,0.5])
    hn_id = '1'
    found_customer = False
    found_item = False
    with st.container():
        with col1:
            hn_id = st.text_input('HN_number :', '1')
            col21,col22 = st.columns(2)
            with col21:
                hn_name = st.text_input('ชื่อ', '')
            with col22:
                hn_lastname = st.text_input('นามสกุล', '')
        
            #if st.button('ค้นหาข้อมูลลูกค้า'):
            customer_df = customer_profile_df[(customer_profile_df['hn'].astype('string').str.contains(hn_id)) & (customer_profile_df['name'].str.lower().str.contains(hn_name.lower()))]
            customer_df = customer_df[(customer_profile_df['last_name'].fillna('Not define').str.lower().str.contains(hn_lastname.lower()))]
            st.dataframe(customer_df.head(5))

            with col2:
                if customer_df.shape[0]>0 :
                    customer_df = customer_df.iloc[0,:]
                    hn_id = customer_df['hn']
                    found_customer = True
                    display_cutomer(customer_df)
                else:
                    found_customer = False
                    st.warning('ไม่มีลูกค้าในระบบ')
        
        item_name = None
        used_couse_num = None
        with col1:
            if (found_customer) & (hn_id!=None):
                customer_product_df = customer_product_record_df[customer_product_record_df['hn'] == int(hn_id)]
                item_name = choose_service(customer_product_df)
                
            if item_name != None:
                used_couse_num  = st.text_input('จำนวน Couse ทั้งหมดที่ลูกค้าใช้ครั้งนี้', '1')
            else:
                st.warning('ลูกค้ายังไม่มีบริการที่ซื้อในระบบ')
                used_couse_num = '0'

            item_df = product_category_df[product_category_df["item_name"] == item_name]

            if item_df.shape[0]>0:
                item_df = item_df.iloc[0,:]
                if (item_df['duration_unit'] == 'MONTH'):
                    next_dt = date.today() + relativedelta(months=+ int(item_df['duration']))
                elif  (item_df['duration_unit'] == 'WEEK'):
                    next_dt = date.today() + relativedelta(weeks=+int(item_df['duration']))
                elif (item_df['duration_unit'] == 'DAY'):
                    next_dt = date.today() + relativedelta(days=+int(item_df['duration']))
                else:
                    next_dt = None
                found_item = True
            else:
                st.warning('ไม่มีบริการนี้ในฐานข้อมูล')
                
        
    with st.container():    
        with col2:
            display_service(item_name, used_couse_num)

    used_row = {
        'hn' : hn_id,
        'item_name' : None,
        'status' : 'test',
        'duration': None,
        'duration_unit': None,
        'next_date': None,
        'num_course' : None,
        'txn_date': date.today().strftime('%Y-%m-%d')
    }
    if found_item:  
        used_row = {
            'hn' : int(hn_id),
            'item_name' : item_name,
            'status' : 'test',
            'duration': int(item_df['duration']),
            'duration_unit': item_df['duration_unit'],
            'next_date': next_dt.strftime('%Y-%m-%d'),
            'num_course' : used_couse_num,
            'txn_date': date.today().strftime('%Y-%m-%d')
        }
    else:
        used_row = {
            'hn' : int(hn_id),
            'item_name' : item_name,
            'status' : 'test',
            'duration': 0,
            'duration_unit': '-',
            'next_date': None,
            'num_course' : None,
            'txn_date': date.today().strftime('%Y-%m-%d')
        }
    
    if st.button('ยืนยันเพิ่มข้อมูล'):
        if item_name != None :
            st.dataframe(pd.DataFrame.from_dict(used_row,orient='index').T)
            customer_used_record_df = pd.concat([customer_used_record_df,pd.DataFrame.from_dict(used_row,orient='index').T],axis=0, ignore_index=True)
            utils_prive.save_customer_used_record(customer_used_record_df)
            st.balloons()
        else:
            st.write('ข้อมูลไม่ครบถ้วน')

    st.divider()
    with st.container():
        st.title('รายการใช้งานทั้งหมด (แก้ไขได้)')
        st.write(time.strftime('%X - %x'))

        customer_used_record_df = utils_prive.get_customer_used_record()
        customer_used_record_df = rename_to_display(customer_used_record_df)
        edited_df = st.data_editor(customer_used_record_df.sort_values('วันที่นัดครั้งถัดไป',ascending=False), height=1000,width=1100)
        if st.button('บันทึกการเปลี่ยนแปลง'):
            edited_df = rename_to_save(edited_df)
            utils_prive.save_customer_used_record(edited_df)

    return 1

    
###  Main
st.set_page_config(layout="wide")
st.title('เพิ่มข้อมูลการใช้บริการลูกค้า')

st.divider()
st.subheader(f'เพิ่มข้อมูลการใช้บริการลูกค้า ')

used_row = add_used_record2db()


