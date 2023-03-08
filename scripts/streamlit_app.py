import streamlit as st
import pandas as pd
import folium
import streamlit_folium

app_title = "Narcan Deployment in San Francisco, 2018-2023"
app_subtitle = "Source: Data SF / SFPD"

def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_subtitle)

    ## load data
    df = pd.read_csv("/Users/mengyu/code/sfpd-data/data/processed/narcan_deployment.csv")
    field_name = "Incident ID"
    metric_title = "Total number of Narcan deployment:"
    # total = df[field_name].count()
    # st.metric(metric_title, total)
    df = df.drop(columns=["Unnamed: 0"])

    ## display filters and map
    year_options = ['All years'] + sorted(df['Incident Year'].unique(), reverse=True)
    district_options = ['All police districts'] + sorted(df['Police District'].unique())

    year_filter = st.selectbox('Select year:', year_options)
    district_filter = st.selectbox('Select police district:', district_options)

    if year_filter == 'All years':
        filtered_df = df
    else:
        filtered_df = df[df['Incident Year'] == year_filter]

    if district_filter != 'All police districts':
        filtered_df = filtered_df[filtered_df['Police District'] == district_filter]

    # update the total based on the filters
    total = filtered_df[field_name].count()
    st.metric(metric_title, total)

    # Display the filtered data
    st.write(filtered_df)

    # Add markers for each location in the filtered data
    map_center = (filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean())
    m = folium.Map(location=map_center, zoom_start=12)
    for index, row in filtered_df.iterrows():
        tooltip = f"Incident Datetime: {row['Incident Datetime']}<br>Intersection: {row['Intersection']}"
        folium.Marker([row['Latitude'], row['Longitude']], tooltip=tooltip).add_to(m)

    # Display the filtered map using streamlit_folium
    st.write(streamlit_folium.folium_static(m))

if __name__ == "__main__":
    main()
