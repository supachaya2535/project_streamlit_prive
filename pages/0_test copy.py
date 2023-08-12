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

df = utils_prive.get_customer_used_record()
st.dataframe(df)
st.text('Hello')


df['dob2'] =  df['dob'].str.replace(' 00:00','')
st.dataframe(df['dob'])

customer_profile_df['dob'] =  pd.to_datetime(customer_profile_df['dob2'], format='mixed').dt.strftime('%Y-%m-%d')
customer_profile_df['application_dt'] =  pd.to_datetime(customer_profile_df['application_dt'], format='mixed').dt.strftime('%Y-%m-%d')

st.dataframe(customer_profile_df.drop(columns='dob2'))
if st.button('บันทึกการเปลี่ยนแปลง'):
        st.balloons()
        save_customer_profile(customer_profile_df.drop(columns='dob2'))