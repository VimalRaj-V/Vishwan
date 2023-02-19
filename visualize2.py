# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 09:00:49 2023

@author: Vimal Raj
"""


import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

 
# Title
st.title("PSG - PRAYATNA'23 !!!")

# Selection box
city = st.sidebar.selectbox("City: ",
					        ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai'])


data = pd.read_csv("processed_data_" + city + ".csv")
data_csv = data.copy()


parameters = list(data_csv.columns)
Locations = list(data_csv['location'])
data_csv = data_csv.set_index(['location'])

st.subheader(city)
loc_name = st.sidebar.selectbox('Select location:', Locations)
st.success(f"The no. of houses surveyed : {data_csv['no_of_houses_surveyed'][loc_name]}")


pie_col, gauge_col = st.columns((1, 0.8))


room_splitup = [["1 BHK",data_csv['1bhk'][loc_name]], ["2 BHK", data_csv['2bhk'][loc_name]], ["3 BHK", data_csv['3bhk'][loc_name]], ["3+ BHK", data_csv['3+bhk'][loc_name]]]
piedata = pd.DataFrame(room_splitup, columns = ['name','count']) # Create the pandas DataFrame

# Creating a Pie Chart
fig = go.Figure()
colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
fig = px.pie(piedata, values='count', names = 'name', hover_name='name')
fig.update_layout(showlegend = True, width=350, height=350,
                  margin=dict(l=0.5,r=1,b=1,t=1))
fig.update_traces(textposition='inside', textinfo='label+percent',
                  marker=dict(colors=colors, line=dict(color='#ffffff', width=2)))
pie_col.write(fig)

# Creating a Gauge meter for area spread
min_selling_area = data_csv['min_selling_area'][loc_name]


gauge_col.info("Information about Selling Area")
gauge_col.markdown(f"Minimum Selling Area is {data_csv['min_selling_area'][loc_name]} Sq. m")
gauge_col.markdown(f"Average Selling Area is {round(data_csv['avg_selling_area'][loc_name], 2)} Sq. m")
gauge_col.markdown(f"Maximum Selling Area is {data_csv['max_selling_area'][loc_name]} Sq. m")
gauge_col.info("Information about Selling Price per Sq m")
gauge_col.markdown(f"Minimum Selling Price is {data_csv['min_selling_cost'][loc_name]} INR")
gauge_col.markdown(f"Average Selling Price is {round(data_csv['avg_selling_cost'][loc_name], 2)} INR")
gauge_col.markdown(f"Maximum Selling Price is {data_csv['max_selling_cost'][loc_name]} INR")


features = []
for parameter in parameters[13:]:
    if data_csv[parameter][loc_name] > 0:
        features.append(parameter)

st.sidebar.markdown("## Features")
for feature in features:
    st.sidebar.write(f"      * {feature}")
