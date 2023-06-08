import numpy as np 
import pandas as pd
import geopandas as gpd
import streamlit as st
import plotly.express as px
import folium 
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import joblib
import json
from PIL import Image
from streamlit.components.v1 import html

st.set_page_config(page_title='Fibre Roll-out in South African Townships', page_icon=':globe_with_meridians:', layout='wide')

@st.cache_data
def prov_geo():
     data = "https://2207-17-fibre-competitive-intensity-model-b.s3.eu-west-1.amazonaws.com/Streamlit+Data/prov.geojson"

     gdf = gpd.read_file(data)

     return gdf


@st.cache_data
def mun_geo():
     data = "https://2207-17-fibre-competitive-intensity-model-b.s3.eu-west-1.amazonaws.com/Streamlit+Data/muni.geojson"

     gdf = gpd.read_file(data)

     return gdf

@st.cache_data
def ward_geo():
     data = "https://2207-17-fibre-competitive-intensity-model-b.s3.eu-west-1.amazonaws.com/Streamlit+Data/ward.geojson"

     gdf = gpd.read_file(data)

     return gdf

# Get the list of province and place them in a select box
def filter_province(df, column):
       
       granularity = list(df[column].unique())
       
       province = st.sidebar.selectbox('**Select Province**', granularity)

       return province

# Create a function to filter for municipalities in a province and place them in a select box
def filter_municipality(df, mun_column, prov_column, province):
      
       granularity = list(df[mun_column][df[prov_column] == province].unique())
      
       municipal = st.sidebar.selectbox('**Select Municipality**', granularity)

       return municipal

# Create a function to display the province map
def filter_province_map(df):
      # Load the municipality geojson file     
      gdf = prov_geo()
      # Get the center cordinates for South Africa
      map = folium.Map(location=[-30.559482,22.937505999999985], zoom_start = 5, tiles='CartoDB positron')
      # Connect the geo data to the predicted uptake rates
      choropleth = folium.Choropleth(
            geo_data=gdf,
            data = df,
            columns = ('PROVINCE', 'predicted_uptake_rate'),
            key_on = 'feature.properties.PROVINCE',
            line_opacity=0.8,
            highlight=True
            )
      # Add the chloropleth to the map
      choropleth.geojson.add_to(map)
      # Set the province name as the index
      data_indexed = df.set_index('PROVINCE')
      # Add the predicted uptake rates to the geo data for access from the geo data
      for feature in choropleth.geojson.data['features']:
            municname = feature['properties']['PROVINCE']
            feature['properties']['predicted_uptake_rate'] = 'uptake_rate: ' + str(data_indexed.loc[municname, 'predicted_uptake_rate']) if municname in list(data_indexed.index) else ''
        # Label each municipality with their IDs and predicted uptake rates           
      choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['PROVINCE', 'predicted_uptake_rate'], labels=False))

      return map

# Create a function to display the municipality map
def filter_muni_map(data,prov_column,province):
      # Load the municipality geojson file
      df = mun_geo()
      # Get the center cordinates for the province
      pro_cord = pd.read_csv("data/province-cord.csv")
      # Filter the geojson files for the municipalities in the province     
      gdf = df[df[prov_column] == province]
      
      # Add the province to the map using its center cordinates
      map = folium.Map(location=[pro_cord['lat'][pro_cord['PROVINCE'] == province],pro_cord['long'][pro_cord['PROVINCE'] == province]], zoom_start = 6, tiles='CartoDB positron')
      # Connect the geo data with the predicted uptake rates
      choropleth = folium.Choropleth(
            geo_data=gdf,
            data = data,
            columns = ('MUNICNAME', 'predicted_uptake_rate'),
            key_on = 'feature.properties.MUNICNAME',
            line_opacity=0.7,
            highlight=True
            )
      # Add the chloropleth to the map
      choropleth.geojson.add_to(map)
      # Set the municipality name as the index
      data_indexed = data.set_index('MUNICNAME')
      # Add the predicted uptake rates to the geo data for access from the geo data
      for feature in choropleth.geojson.data['features']:
            municname = feature['properties']['MUNICNAME']
            feature['properties']['predicted_uptake_rate'] = 'uptake_rate: ' + str(data_indexed.loc[municname, 'predicted_uptake_rate']) if municname in list(data_indexed.index) else 'N/A'
       # Label each municipality with their IDs and predicted uptake rates       
      choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['MUNICNAME', 'predicted_uptake_rate'], labels=False))


      return map

# Create a function to display the ward map
def filter_ward_map(data,prov_column,munic_column,province,municipality):
      # Load the ward geojson file
      df = ward_geo()
      # Get the center cordinates for the municipalities
      muni_cord = pd.read_csv("data/munic-cord.csv")
      # Filter the geojson files for the wards in the province and municipality
      gdf = df[(df[prov_column] == province) & (df[munic_column] == municipality)]
      
      # Add the municipality to the map using its center cordinates
      map = folium.Map(location=[muni_cord['lat'][muni_cord['MUNICNAME'] == municipality],muni_cord['long'][muni_cord['MUNICNAME'] == municipality]], zoom_start = 8, tiles='CartoDB positron')
      # Connect the geo data with the predicted uptake rates 
      choropleth = folium.Choropleth(
            geo_data=gdf,
            data = data,
            columns = ('WARD_ID', 'predicted_uptake_rate'),
            key_on = 'feature.properties.WARD_ID',
            line_opacity=0.7,
            highlight=True
            )
      # Add the chloropleth to the map
      choropleth.geojson.add_to(map)
      # Change the dtype of the ward_id to str
      data['WARD_ID'] = data['WARD_ID'].astype(str)
      # Set the ward_id as the index
      data_indexed = data.set_index('WARD_ID')
      # Add the predicted uptake rates to the geo data for access from the geo data
      for feature in choropleth.geojson.data['features']:
            wardname = feature['properties']['WARD_ID']
            feature['properties']['predicted_uptake_rate'] = 'uptake_rate: ' + str(data_indexed.loc[wardname, 'predicted_uptake_rate']) if wardname in list(data_indexed.index) else 'N/A'

      # Label each wards with their IDs and predicted uptake rates
      choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['WARD_ID', 'predicted_uptake_rate'], labels=False))


      return map

# Create a function to display key metrics
def metric(df, filter_col, filter_value, metric):
      
      result = df[metric][df[filter_col] == filter_value]

      st.metric(metric,  result)




# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css") 


def main():
    
    tab1, tab2, tab3, tab4 = st.tabs([":house: Home", "Predictions", "What we do", "Contact Us"])

    with tab3:
        st.title("Fibre Connectivity in South African Townships")


        st.subheader("Why bring fibre to townships")

        st.image('image/internet township.jpg')

        st.write("Fiber optic technology is used for high-speed internet connectivity, which is becoming increasingly important in townships for several reasons:")
        st.write("**Increasing demand for high-speed internet:**")
        st.write("As more people in townships use the internet for education, work, entertainment, and communication, the demand for high-speed internet is growing.Improved access to information: With high-speed internet, people in townships can access information and resources that were previously unavailable, which can improve their quality of life and opportunities for success.")
        st.write("**Economic development:**")
        st.write("High-speed internet can attract new businesses and investments to townships, which can create jobs and stimulate economic growth.")
        st.write("**Education:**")
        st.write(" High-speed internet can provide access to online education and e-learning platforms, which can help students in townships access educational resources and opportunities.")
        st.write("**Healthcare:**")
        st.write("Telemedicine, or the use of telecommunication and information technologies to provide healthcare services remotely, is becoming increasingly important, especially in rural and underserved areas. High-speed internet can enable telemedicine services and improve healthcare access for people in townships.")

        st.subheader("The Problem")
        st.image('image/fibre_installers.jpeg', width= 700)

        st.write("Telco companies have limited data-driven & quantitative tools to support their fiber roll-out plans examples HH uptake rates, competitive roll-out etc. The current SaaS solutions mainly focus on advanced expansion cost calculations for example Comsof and Netadmin versus support identifying possible expansion areas ")

        st.subheader('The Solution')
        st.image('image/project-isizwe.0.1547549912.jpg', width=600)
        st.write('We have created a tool that provides data-driven revenue predictions by area which can drastically improve accuracy of expansion in business cases. The revenue predictions should be scalable across geographies but provide granular information, allowing for detailed view on expansion opportunities for Telco companies.')
        st.image("image/sales.jpeg")

    with tab1:

        # Set title for the dashboard
        st.title("Fibre Uptake Rates in South Africa")

        # Load datasets
        df_province = pd.read_csv('data/province-pred-uptake-rate.csv')
        df_ward = pd.read_csv('data/ward-pred-uptake-rate.csv')
        df_municipal = pd.read_csv('data/municipality-pred-uptake-rate.csv')

        # Load geojson dataset
        # gdf_province = gpd.read_file("prov.geojson")

        # Create sidebar contents
        # admin_boundaries = st.sidebar.radio('**Admin Levels**',['Province','District','Municipality'])


        # Create a checkbox to activate lists of provinces
        check_province = st.sidebar.checkbox('Drill Province')
        
        # Display provinces if box is checked
        if check_province:
             province_gran =  filter_province(df_province, "PROVINCE")

        # Create a checkbox to activate lists of municipalities
        check_municipality = st.sidebar.checkbox('Drill Municipality')

        # Display municipalities if box is checked
        if check_province and check_municipality:
              municipal = filter_municipality(df_municipal,"MUNICNAME", "PROVINCE", province_gran)



        # if check_province and check_municipality:
        #     st.header(f'{municipal} Uptake Rate in {province_gran} Province')

        # elif check_province:
        #     st.header(f'{province_gran} Province Uptake Rate')

        # else:
        #     st.header(f'Uptake Rate per Province')

        
        # Visulaize the unfilterd map
        if check_province and check_municipality:
             st_folium(filter_ward_map(df_ward,"PROVINCE","MUNICNAME",province_gran,municipal), width= 700, height= 450)

        elif check_province:
              st_folium(filter_muni_map(df_municipal,"PROVINCE",province_gran), width= 700, height= 450)

        else:
              st_folium(filter_province_map(df_province),width= 700, height= 450)


        # if check_province:
        #      pro = st_folium(filter_province_map(df_province),width= 700, height= 450)
        #      if pro['last_active_drawing']:
        #             prov_name = pro['last_active_drawing']['properties']['PROVINCE']
        #             mun = st_folium(filter_muni_map(df_municipal,"PROVINCE",prov_name), width= 700, height= 450)

        #             if check_municipality:
        #                  if mun['last_active_drawing']:
        #                         mun_name = pro['last_active_drawing']['properties']['MUNICNAME']
        #                         st_folium(filter_ward_map(df_ward,"PROVINCE","MUNICNAME",prov_name,mun_name), width= 700, height= 450)

        # else:
        #      st_folium(filter_province_map(df_province),width= 700, height= 450)
                         

        #Display Metrics
        if check_province and check_municipality:
            st.subheader(f'{municipal} Metrics')

        elif check_province:
            st.subheader(f'{province_gran} Metrics')
        

        met1, met2, met3 = st.columns(3)
        with met1:
                if check_province and check_municipality:
                      metric(df_municipal,"MUNICNAME",municipal, "predicted_uptake_rate")

                elif check_province:
                      metric(df_province,"PROVINCE",province_gran, "predicted_uptake_rate")
        with met2:
                if check_province and check_municipality:
                      metric(df_municipal,"MUNICNAME",municipal, "households")

                elif check_province:
                      metric(df_province,"PROVINCE",province_gran, "households")
        with met3:
                if check_province and check_municipality:
                      metric(df_municipal,"MUNICNAME",municipal, "population")

                elif check_province:
                      metric(df_province,"PROVINCE",province_gran, "population")


                      

        # st.title("Fibre Uptake in Administrative Levels of South Africa")

        # selection = st.sidebar.radio("Administrative Levels", ['Province', 'District', 'Municipality', 'Ward'])


        # # Segment the visual and selection options
        # admin, dashboard, viz = st.columns([2,3,2])
        # households = 1000
        # uptake_rate = 8.3

        # dashboard.subheader(f'**The household is** {households}')
        # dashboard.subheader(f'**The Uptake Rate is** {uptake_rate}%')



        # # Define the radio options
        # # radio_options = ['Province', 'District', 'Municipality', 'Ward']


        # # Create the sidebar with the radio button
        # # selection = admin.radio('**Select Administrative Level**', radio_options)

        # # Create the main section with the selectbox and the corresponding map
        # if selection == 'Province':
        #     st.header('Uptake Rate per Province')
            
        #     folium_static(province_map(), width=1000, height=500)

        # elif selection == 'District':
        #     st.header('Uptake Rate per District')
            
        #     folium_static(district_map(), width=1000, height=500)

        # else:
        #     st.header('Uptake Rate per Municipality')
            
        #     folium_static(municipality_map(), width=1000, height=500)


    with tab2:
        st.title("Predictions for Different Levels of Granularity")

        col1, col2, col3 = st.columns([1,2,1])
        col4, col5, col6 = st.columns([1,2,1])
        col7, col8, col9 = st.columns([1,2,1])
        col10, col11, col12 = st.columns([1,2,1])
        # x, button, y = st.columns([1,2,1])
        # a, dis, b = st.columns([1,2,1])

        age_above_60 = col8.text_input('% Age above 60',placeholder='Please enter the % population that are above 60 years')
        
        no_schooling = col5.text_input('% Not Schooling',placeholder='Please enter the % population that does not attend school')
        
        avg_income = col2.text_input('Average Income',placeholder='Please enter the average income')

        pipe_water_in_house = col11.text_input('% Pipe Water in House',placeholder='Please enter the % of houses with water in house')
        
        if (avg_income.isdigit() == True) and (no_schooling.isdigit() == True) and (no_schooling !="") and (age_above_60 !="") and (pipe_water_in_house != "") and (age_above_60.isdigit() == True) and (pipe_water_in_house.isdigit() == True):
            predict =st.button('Predict')

            if predict:
                # Get the features
                features = [age_above_60,no_schooling, avg_income, pipe_water_in_house]

                # Unickle the trained model
                predictor = joblib.load(open("model/RF_ward.pkl", "rb"))
                # Generate a fiber uptake prediction
                prediction = predictor.predict(np.array(features).reshape(1,-1))

                st.success(f'Fiber uptake rate is **{np.round(prediction[0],2)}%**')


        

    with tab4:
        st.title("Contributors")
        st.subheader("Team-17")

        col1, col2, col3 = st.columns(3)
        with col1: 
            st.image("image/olisa.png", width=200)
            st.info("""Olisa Clement""")

        with col2: 
            st.image("image/karabo.jpg", width=200)
            st.info("""Karabo Molema""")
            

        with col3:
            st.image("image/jonathan.jpg", width=200)
            st.info("""Jonathan Ajayi""")

        col4, col5, col6 = st.columns(3)

        with col4:
            st.image("image/nelson.jpg", width=200)
            st.info("""Nelson Mwembe""")

        with col5: 
            st.image("image/philile.jpg",  width=200)
            st.info("""Philile Luhlanga""")

        with col6:
            st.image("image/abdulrasheed.jpg", width=200)
            st.info("""Abdulrasheed Musa""")

        



        

        #Contact information
        with st.container():
            st.write("---")
            st.header("**If you have any questions or feedback, please don't hesitate to get in touch with us!**")
            st.write("##")

            # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
            contact_form = """
            <form action="https://formsubmit.co/ppluhlanga@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
            left_column, right_column = st.columns(2)
            with left_column:
                st.markdown(contact_form, unsafe_allow_html=True)
            with right_column:
                st.empty()

            st.write("---")  
            st.info(
                """
                **Physical Address**: 10 Bhabule Street,Nelspruit,1200\n
                **Phone number:** +234 806 279 2419\n
                **Fax Number:** +234 706 563 6456 \n
                :mailbox: team17@gmail.com \n
                :house: Team-17@Explore\n
                :chart: Team-17
            """ 
            )
            st.write("##")
# =====================================================================================================================================

# Hide streamlit styling
# hide_st_style = """
            #<style>
            #MainMenu {visibility: hidden;}
            #footer {visibility: hidden;}
            #header {visibility: hidden;}
            #</style>
          #  """
#st.markdown(hide_st_style, unsafe_allow_html=True)

        
if __name__ == '__main__':
    main()
