import streamlit as st
import pandas as pd
import numpy as np

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils_prive import load_customer_used_record_data

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

def get_customer_used_record():
    # Customer used Record
    try:
        customer_used_record_df = pd.read_csv(f"./database/customer_used_record/customer_used_record_{date.today()}_data.csv")
    except:
        customer_used_record_df = pd.read_csv(f"./database/customer_used_record/customer_used_record_data.csv")
        customer_used_record_df['status'] = 'excel'
    return customer_used_record_df.drop_duplicates()

def get_customer_product_record():
    # Customer Product Record
    try:
        customer_product_record_df = pd.read_csv(f"./database/customer_product_record/customer_product_record_{date.today()}_data.csv")
    except:
        customer_product_record_df = pd.read_csv(f"./database/customer_product_record/customer_product_record_data.csv")
    customer_product_record_df['active_status'] = True
    activ = customer_product_record_df['expired_dt'] < str(date.today())
    customer_product_record_df.loc[activ,'active_status'] = False
    return customer_product_record_df.drop_duplicates()

def get_customer_profile():
    # Customer Profile Load
    try:
        customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_{date.today()}_data.csv")
        # st.success('Load from lasted updated file')
    except:
        customer_profile_df = pd.read_csv(f"./database/customer_profile/customer_profile_data.csv")
        # st.warning('No updated file today...')
    return customer_profile_df.drop_duplicates()

def get_product_category():
    # Product
    try:
        product_category_df = pd.read_csv(f"./database/product_category/product_category_{date.today()}_data.csv")
    except:
        product_category_df = pd.read_csv(f"./database/product_category/product_category_data.csv")
    return product_category_df.drop_duplicates()

def hex_format(r,g,b):
    return '#{:02X}{:02X}{:02X}'.format(r,g,b)

def choose_service(df):
    active_df = df[df['active_status']]
    curc_list = list(active_df.groupby('item_name').count().index) 
    genre = st.selectbox('เลือกบริการ',curc_list)
    return genre

def display_cutomer(customer_df):
    st.markdown(f"หมายเลข HN : **:green[{customer_df['hn']}]**")
    st.markdown(f"ชื่อ :green[{customer_df['name']}]  \tนามสกุล  :green[{customer_df['last_name']}]")    
    st.markdown(f"เพศ :green[{customer_df['sex']}]  วันเกิด **:green[{customer_df['dob']}]**")
    st.markdown(f"เบอร์โทร : :green[{customer_df['tel']}]  email : :green[{customer_df['email']}]")

def display_service( item_name, used_couse_num):
    st.markdown(f"บริการที่ลูกค้าใช้ : **:green[{item_name}]**")
    st.markdown(f"จำนวนที่ใช้ : **:green[{used_couse_num}]**")

def save_new_used_record2db(used_row):
    customer_used_record_df = get_customer_used_record()
    customer_used_record_df = customer_used_record_df.append(used_row,ignore_index=True).sort_values('next_date',ascending=False)
    customer_used_record_df.to_csv(f"./database/customer_used_record/customer_used_record_{date.today()}_data.csv",header = True,index = False)
    customer_used_record_df.to_csv(f"./database/customer_used_record/customer_used_record_data.csv",header = True,index = False)
        
def add_used_record2db():
    customer_product_record_df = get_customer_product_record()
    product_category_df = get_product_category()

    col1,_, col2 = st.columns([0.5,0.1,0.5])
    with col1:
        hn_id = st.text_input('ค้นหาข้อมูลลูกค้าด้วย HN_number : [xx,xxx]', 57035)
        customer_profile_df = get_customer_profile()
        customer_df = customer_profile_df[customer_profile_df['hn'] == int(hn_id)]
        if customer_df.shape[0]>0 :
            customer_df = customer_df.iloc[0,:]
            with col2:
                display_cutomer(customer_df)
        else:
            st.warning('ไม่มีลูกค้าในระบบ')
    
    
    item_name = '-'
    used_couse_num = '-'

    used_row = {
        'hn' : hn_id,
        'item_name' : item_name,
        'status' : 'test',
        'duration': None,
        'duration_unit': None,
        'next_date': None,
        'num_course' : used_couse_num,
        'txn_date': date.today().strftime('%Y-%m-%d')
    }
    item_name = None
    if customer_df.shape[0]>0:
        customer_product_df = customer_product_record_df[customer_product_record_df['hn'] == int(hn_id)]
        with col1:
            item_name = choose_service(customer_product_df)
            
            if item_name != None:
                used_couse_num  = st.text_input('จำนวน Couse ทั้งหมดที่ลูกค้าใช้ครั้งนี้', '2')
            else:
                used_couse_num = '-'

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
        else:
            st.warning('No service for this customer')
        with col2:
            display_service(item_name, used_couse_num)

        

        customer_used_record_df = get_customer_used_record()
        
    if item_name != None:
        used_row = {
            'hn' : int(hn_id),
            'item_name' : item_name,
            'status' : 'test',
            'duration': float(item_df['duration']),
            'duration_unit': item_df['duration_unit'],
            'next_date': next_dt.strftime('%Y-%m-%d'),
            'num_course' : used_couse_num,
            'txn_date': date.today().strftime('%Y-%m-%d')
        }
    else:
        used_row = {
            'hn' : [int(hn_id)],
            'item_name' : item_name,
            'status' : 'test',
            'duration': '-',
            'duration_unit': '-',
            'next_date': None,
            'num_course' : None,
            'txn_date': date.today().strftime('%Y-%m-%d')
        }

    if st.button('ยืนยันเพิ่มข้อมูล'):
        if item_name != None :
            st.dataframe(customer_used_record_df.append(used_row,ignore_index=True).sort_values('next_date',ascending=False))
            customer_used_record_df = customer_used_record_df.append(used_row,ignore_index=True)
            customer_used_record_df.to_csv(f"./database/customer_used_record/customer_used_record_{date.today()}_data.csv",header = True,index = False)
            customer_used_record_df.to_csv(f"./database/customer_used_record/customer_used_record_data.csv",header = True,index = False)
            st.balloons()

            
        else:
            st.write('ข้อมูลไม่ครบถ้วน')
    st.divider()
    with st.container():
        st.title('รายการใช้งานทั้งหมด (แก้ไขได้)')
        st.write(time.strftime('%X - %x'))

        customer_used_record_df = rename_to_display(customer_used_record_df)
        edited_df = st.experimental_data_editor(customer_used_record_df.sort_values('วันที่นัดครั้งถัดไป',ascending=False), height=1000,width=1100)
        if st.button('บันทึกการเปลี่ยนแปลง'):
            edited_df = rename_to_save(edited_df)
            edited_df.to_csv(f"./database/customer_used_record/customer_used_record_{date.today()}_data.csv",header = True,index = False)
            edited_df.to_csv(f"./database/customer_used_record/customer_used_record_data.csv",header = True,index = False)

    return 1

    
###  Main
st.set_page_config(layout="wide")
st.title('เพิ่มข้อมูลการใช้บริการลูกค้า')

st.divider()
st.subheader(f'เพิ่มข้อมูลการใช้บริการลูกค้า ')

used_row = add_used_record2db()


