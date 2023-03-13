import streamlit as st
import pandas as pd
import folium
import streamlit_folium

app_title = "Drug-related arrests in San Francisco, 2018-2023"
app_subtitle = "Source: Data SF / SFPD"

def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_subtitle)

    ## load data
    df = pd.read_csv("/Users/mengyu/code/sfpd-data/data/processed/drug_arrest_data.csv")
    field_name = "Incident ID"
    metric_title = "Total number of drug-related arrests:"
    # total = df[field_name].count()
    # st.metric(metric_title, total)
    df = df.drop(columns=["Unnamed: 0"])

    ## display filters and map
    year_options = ['All years'] + sorted(df['Incident Year'].unique(), reverse=True)
    neighborhood_options = ['All neighborhoods'] + sorted(df['Analysis Neighborhood'].astype(str).unique())

    year_filter = st.selectbox('Select year:', year_options)
    neighborhood_filter = st.selectbox('Select neighborhod:', neighborhood_options)

    if year_filter == 'All years':
        filtered_df = df
    else:
        filtered_df = df[df['Incident Year'] == year_filter]

    if neighborhood_filter != 'All neighborhoods':
        filtered_df = filtered_df[filtered_df['Analysis Neighborhood'] == neighborhood_filter]

    # Remove any rows with missing latitude or longitude values
    filtered_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])

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
        folium.Marker(
            [row['Latitude'], row['Longitude']], 
        tooltip=tooltip
        ).add_to(m)

    # Display the filtered map using streamlit_folium
    st.write(streamlit_folium.folium_static(m))

if __name__ == "__main__":
    main()
