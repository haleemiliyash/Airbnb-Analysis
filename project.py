import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
pd.set_option('display.max_columns', None)



def data():
    df = pd.read_csv("D:/project/.venv/Airbnb_project/cleaned_airbnb.csv")
    return df
DF=data()

# streamlit part
st.set_page_config(page_title='Airbnb Analysis',page_icon=":1234:",layout="wide")
st.title('Airbnb Data analysis and visualization :chart_with_upwards_trend:')

with st.sidebar:
    select= option_menu('Main Menu',['Home','About','Visualization & Analysis'],icons=["house","list-task","pencil-square"],menu_icon="cast", default_index=0)

if select=='Home':
    col1,col2 = st.columns(2)
    with col1:
        st.image(Image.open(r"D:/project/.venv\Airbnb_project/airbnb_1.gif"),width=400)
    with col2:
        st.image(Image.open(r"D:/project/.venv\Airbnb_project/airbnb_2.gif"))
    col1,col2 = st.columns(2)
    
if select=='About':
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("About Airbnb")
        st.write("""Airbnb is an American company operating an online marketplace for short and long-term homestays and experiences.
                 The company acts as a broker and charges a commission from each booking. 
                 The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.
                  Airbnb is a shortened version of its original name, AirBedandBreakfast.com. 
                 Airbnb is the most well-known company for short-term housing rentals.""")
    col1,col2,col3=st.columns(3)
    with col1:
        st.image(Image.open(r"D:/project/.venv\Airbnb_project/airbnb_3.gif"),width=400)

if select=='Visualization & Analysis':
    tab1,tab2,tab3,tab4,tab5=st.tabs(['Price analysis','Avalability analysis','Location Based','Geographyical Visualization','Top charts'])
    with tab1: # price visulization
        country_price = st.selectbox("Select the Country", DF["address.country"].unique(), key="Select the country")
        df_country = DF[DF["address.country"] == country_price]
        room_type = st.selectbox("Select the Room Type", df_country["room_type"].unique())
        df_room_type = df_country[df_country["room_type"] == room_type]

        price_bar = px.bar(df_room_type, x='property_type', y='price', title='PRICE FOR PROPERTY_TYPES',
                                 hover_data=["number_of_reviews"], color='price',
                                 color_continuous_scale=px.colors.sequential.Redor_r)
        st.plotly_chart(price_bar)

    with tab2:# avalibility visulization
        df = pd.read_csv("D:/project/.venv/Airbnb_project/cleaned_airbnb.csv")
        country_available = st.selectbox("Select the Country", df["address.country"].unique(), key="Select country")
        df_country_1 = df[df["address.country"] == country_available]
        property_type=st.selectbox("Select the property type",df_country_1["property_type"].unique())
        df_property_type=df_country_1[df_country_1["property_type"]==property_type]

        avalibilty_sunburst = px.sunburst(df_property_type, path=["room_type", "bed_type", "address.location.is_location_exact"],
                                                title="Availability of 30 days",
                                               color='availability.availability_30')
        st.plotly_chart(avalibilty_sunburst)
    
    with tab3:#location visulization
        country_location = st.selectbox("Select the Country", DF["address.country"].unique())
        df_country_2 = DF[DF["address.country"] == country_location]
        property_type_1 = st.selectbox("Select the Property Type", df_country_2["property_type"].unique())
        df_property_type_1 = df_country_2[df_country_2["property_type"] == property_type_1]

        st.dataframe(df_property_type_1)

    with tab4:# geographical analysis
        map_plot = px.scatter_mapbox(df, lat='address.location.coordinates[1]', lon='address.location.coordinates[0]', color='price', size='accommodates',
                                            color_continuous_scale="rainbow", hover_name='host.host_name',
                                            mapbox_style="carto-positron", zoom=1)
        map_plot.update_layout(width=600, height=800, title='Geographical Distribution')
        st.plotly_chart(map_plot)

    with tab5:# top charts
        country_chart=st.selectbox("Select the Country", DF["address.country"].unique(), key="country select")
        df_country_3=DF[DF["address.country"] == country_chart]
        #property_type_2=st.selectbox("Select the Property Type", df_country_3["property_type"].unique())
        #df_property_type_2=df_country_3[df_country_3["property_type"] == property_type_2]

        df_sort_price=df_country_3.sort_values(by="price")
        df_price_sum_mean=pd.DataFrame(df_sort_price.groupby("property_type")["price"].agg(["sum","mean"]))
        df_price_sum_mean.reset_index(inplace=True)
        df_price_sum_mean.columns=["property_type","Total_price","Avg_price"]

        price_avg = px.bar(df_price_sum_mean, x="Total_price", y="property_type", orientation='h',
                                   title="Price based on country",hover_data=["Avg_price",'Total_price'],color='Total_price',width=600, height=800)
        st.plotly_chart(price_avg)