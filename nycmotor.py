##Tushar Aggarwal

#Importing the required liabraries
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px 
import gdown
import streamlit_embedcode
url = "https://drive.google.com/uc?id=1Q7_Seerl4Da2k3pDw9bOXH91vLe44wrc"
output = "motor.csv" # replace with the name you want for your CSV file
gdown.download(url, output, quiet=False)





st.set_page_config(layout="wide",page_title="Motor Vehicle Collision Reports(NYC🗽) by Tushar Aggarwal")
#image_url = "https://drive.google.com/file/d/1fOIQqwMzZowohCg5rjDv4AnSjHWWwE2P/uc?usp=sharing"
#st.image(image_url, width=100)
st.title("Motor Vehicle Collision Reports(NYC🗽)by Tushar Aggarwal")
#st.set_page_config(
    #page_title="Motor Vehicle Collision Reports(NYC🗽)",
    #page_icon="🗽",
    #layout="wide",
    #initial_sidebar_state="expanded"
#)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)



# Using st.cache to store df in cache
@st.cache_data(persist=True)
def load_data(nrows):
    data = pd.read_csv(output, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase =lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time':'date/time'}, inplace=True)
    return data

data=load_data(100000)
original_data =data
##################


#Query1
st.header("Where are the most people injured in NYC?")
injured_people = st.sidebar.slider("Choose number of injured person  in vehicle collision", 1, 19)
st.map(data.query("injured_persons>=@injured_people")[["latitude","longitude"]].dropna(how="any"))

#Query2
st.header("How many collisions occur during a given time of the day?")
hour=st.sidebar.slider("Hour range ", 0,23)
data=data[data['date/time'].dt.hour==hour]

st.markdown("Vehicle collision between %i:00 and %i:00" %(hour,(hour+1)%24))
midpoint =(np.average(data['latitude'])),(np.average(data['longitude']))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
    "latitude":midpoint[0],
    "longitude":midpoint[1],
    "zoom":11,
    "pitch":50,
    },
    layers=[
    pdk.Layer(
    "HexagonLayer",
    data=data[['date/time','latitude','longitude']],
    get_position=['longitude','latitude'],
    radius=100,
    extruded=True,
    pickable=True,
    elevation_scale=4,
    elevation_range=[0, 1000],
    ),
    ],
))

#######Visuals

st.subheader("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered =data[
    (data['date/time'].dt.hour >=hour) & (data['date/time'].dt.hour<(hour+1))]
hist=np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data =pd.DataFrame({'minute':range(60),
                          'crashes':hist})

fig=px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)


st.subheader("Top 5 dangerous streets by affected type")
select =st.sidebar.radio("Affected Category", ['Pedestrians','Cyclists','Motorists'])

if select =='Pedestrians':
    st.write(original_data.query("injured_pedestrians>=1")[['on_street_name','injured_pedestrians']].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])
elif select =="Cyclists":
    st.write(original_data.query("injured_cyclists>=1")[['on_street_name','injured_cyclists']].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])
else:
    st.write(original_data.query("injured_motorists>=1")[['on_street_name','injured_motorists']].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])





#Raw Date view for debugging if any:

if st.checkbox("Show me Raw data", False):
    st.subheader('Here is your raw data, enjoy!')
    st.write(data)

########

embed_code = streamlit_embedcode.get_embed_code(hash_func=None, width=800, height=600)
st.markdown(embed_code, unsafe_allow_html=True)
##########################################END######################################################################

