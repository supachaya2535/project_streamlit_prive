import streamlit as st
import pandas as pd
import numpy as np

import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils_prive import save_customer_used_record
import utils_prive

###  Main
st.set_page_config(layout="wide")
status = utils_prive.choos_status()

st.write(time.strftime('%X - %x'))

df = utils_prive.get_customer_used_record()
st.dataframe(df)
st.text('Hello')


df['next_date'] =  df['next_date'].str.replace(' 00:00','')
st.dataframe(df)

df['txn_date'] =  pd.to_datetime(df['txn_date'], format='mixed').dt.strftime('%Y-%m-%d')
df['next_date'] =  pd.to_datetime(df['next_date'], format='mixed').dt.strftime('%Y-%m-%d')

st.dataframe(df)
if st.button('บันทึกการเปลี่ยนแปลง'):
        st.balloons()
        save_customer_used_record(df)