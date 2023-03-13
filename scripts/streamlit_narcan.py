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
    df = pd.read_csv("https://raw.githubusercontent.com/fishdmy/sfpd-data/main/data/processed/narcan_deployment.csv")
    field_name = "Incident ID"
    metric_title = "Total number of Narcan deployment:"
    # total = df[field_name].count()
    # st.metric(metric_title, total)
    df = df.drop(columns=["Unnamed: 0"])

    ## display filters and map
    year_options = ['All years'] + sorted(df['Incident Year'].unique(), reverse=True)
    neighborhood_options = ['All neighborhoods'] + sorted(df['Analysis Neighborhood'].unique())

    year_filter = st.selectbox('Select year:', year_options)
    neighborhood_filter = st.selectbox('Select neighborhod:', neighborhood_options)

    if year_filter == 'All years':
        filtered_df = df
    else:
        filtered_df = df[df['Incident Year'] == year_filter]

    if neighborhood_filter != 'All neighborhoods':
        filtered_df = filtered_df[filtered_df['Analysis Neighborhood'] == neighborhood_filter]

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







# import streamlit as st
# import pandas as pd
# import folium
# from streamlit_folium import folium_static
# import streamlit.components.v1 as components


# app_title = "Where do drug-related arrests and Narcan deployment occur in San Francisco?"

# def main():
#     st.set_page_config(app_title)
#     st.title(app_title)

#     display_data_and_map("Narcan Deployment, 2018-2023", "/Users/mengyu/code/sfpd-data/data/processed/narcan_deployment.csv", "Incident ID")
#     display_data_and_map("Drug-related arrests in San Francisco, 2018-2023", "/Users/mengyu/code/sfpd-data/data/processed/drug_arrest_data.csv", "IncidntNum")

# def display_data_and_map(title, data_file_path, field_name):
#     st.header(title)
#     ## load data
#     df = pd.read_csv(data_file_path)
#     metric_title = f"Total number of {title}:"
#     df = df.drop(columns=["Unnamed: 0"])

#     ## display filters and map
#     year_options = ['All years'] + sorted(df['Incident Year'].unique(), reverse=True)
#     neighborhood_options = ['All neighborhoods'] + sorted(df['Analysis Neighborhood'] <br> .astype(str).unique().tolist())

#     year_filter = st.selectbox('Select year:', year_options)
#     neighborhood_filter = st.selectbox('Select neighborhood:', neighborhood_options)

#     if year_filter == 'All years':
#         filtered_df = df
#     else:
#         filtered_df = df[df['Incident Year'] == year_filter]

#     if neighborhood_filter != 'All neighborhoods':
#         filtered_df = filtered_df[filtered_df['Analysis Neighborhood'] == neighborhood_filter]

#     # update the total based on the filters
#     total = filtered_df[field_name].count()
#     st.metric(metric_title, total)

#     # Display the filtered data
#     st.write(filtered_df)

#     # Add markers for each location in the filtered data
#     map_center = (filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean())
#     m = folium.Map(location=map_center, zoom_start=12)
#     for index, row in filtered_df.iterrows():
#         tooltip = f"Incident Datetime: {row['Incident Datetime']}<br>Intersection: {row['Intersection']}"
#         folium.Marker(
#             [row['Latitude'], row['Longitude']], 
#             tooltip=tooltip
#         ).add_to(m)

#     # Display the filtered map using an iframe and the components.html function
#     map_html = folium_static(m, width=700, height=500)
#     components.html(f'<iframe srcdoc="{map_html}" width=700 height=500></iframe>')
    

# if __name__ == "__main__":
#     main()
