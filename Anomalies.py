#import modules
import streamlit as st
import pandas as pd
import numpy as np


#page config
st.set_page_config(
    page_title="Dashboard Coach Buzz - PE",
    page_icon="image.png",
    layout="wide",
)
st.markdown("# Anomalies Analysis ⚠️")




#dados
data = pd.read_csv('https://raw.githubusercontent.com/igorszt/streamlit/main/base_morning_results_BR.csv',parse_dates=['day'])


#unique bdrs
total_bdrs = data['bdrId'].unique().shape[0]

#days analized
days_analyzed = data['day'].max() - data['day'].min()
days_analyzed = days_analyzed / np.timedelta64(1,'D')
days_analyzed = int(days_analyzed)

#gps
gps = round(data[data['kpi']=='gps'].groupby('bdrId').agg({'value':'mean'})['value'].mean(),1)/100
gps_pct = "{:.1%}".format(gps)

#task completion
net_completion = round(data[data['kpi']=='net_completion'].groupby('bdrId').agg({'value':'mean'})['value'].mean(),1)/100
net_pct = "{:.1%}".format(net_completion)

#prop_+2min
prop_2min = round(data[data['kpi']=='prop_+2min'].groupby('bdrId').agg({'value':'mean'})['value'].mean(),1)/100
prop_pct = "{:.1%}".format(prop_2min)

#kpis
col1,col2,col3,col4 = st.columns(4)
col1.metric(label='# BDRs',value=total_bdrs)
col1.metric(label='Days Analyzed',value=days_analyzed)
col2.metric(label='GPS',value=gps_pct)
col3.metric(label='Task Completion',value=net_pct)
col4.metric(label='Prop. Visits More 2 Minutes',value=prop_pct)

#table with anomalies by tipe
temp = data.groupby(['bdrId','kpi']).agg({'anomalie':'sum'}).reset_index()
temp2= temp.pivot(index='bdrId',columns='kpi',values='anomalie').reset_index()
temp2['Total Anomalies'] = temp2['gps']+temp2['net_completion']+temp2['prop_+2min']
temp2.rename(columns={'bdrId': 'BDR_ID','gps': 'Anomalie GPS', 'net_completion': 'Anomalie Net Completion','prop_+2min': 'Anomalie Low Quality'}, inplace=True)
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(temp2.sort_values('Total Anomalies').head(5))

#avg type anomalie by bdr by days analized
gps_anomalie = data[data['kpi']=='gps'].groupby('bdrId').agg({'anomalie':'sum'}).reset_index()
gps_anomalie = round(gps_anomalie['anomalie'].mean(),1)
col2.metric(label='Average Anomalies GPS per BDR',value=gps_anomalie)

net_anomalie = data[data['kpi']=='net_completion'].groupby('bdrId').agg({'anomalie':'sum'}).reset_index()
net_anomalie = round(net_anomalie['anomalie'].mean(),1)
col3.metric(label='Average Anomalies Task Completion per BR',value=net_anomalie)

low_anomalie = data[data['kpi']=='prop_+2min'].groupby('bdrId').agg({'anomalie':'sum'}).reset_index()
low_anomalie = round(low_anomalie['anomalie'].mean(),1)
col4.metric(label='Average Anomalies Low Quality per BDR',value=low_anomalie)

