import streamlit as st
import pandas as pd
import folium
import streamlit_folium

app_title = "San Francisco Drug Data, 2018-2023"
app_subtitle = "Source: Data SF / SFPD"

@st.cache(allow_output_mutation=True)
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def filter_data(df, year_filter, neighborhood_filter):
    if year_filter == 'All years':
        filtered_df = df
    else:
        filtered_df = df[df['Incident Year'] == year_filter]

    if neighborhood_filter != 'All neighborhoods':
        filtered_df = filtered_df[filtered_df['Analysis Neighborhood'] == neighborhood_filter]

    # update the total based on the filters
    total = filtered_df['Incident ID'].count()

    # Add markers for each location in the filtered data
    map_center = (filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean())
    m = folium.Map(location=map_center, zoom_start=12)
    for index, row in filtered_df.iterrows():
        tooltip = f"Incident Datetime: {row['Incident Datetime']}<br>Intersection: {row['Intersection']}"
        folium.Marker(
            [row['Latitude'], row['Longitude']], 
            tooltip=tooltip
        ).add_to(m)

    return filtered_df, total, m

def main():
    st.set_page_config(app_title)
    st.title(app_title)
    st.caption(app_subtitle)

    ## load data
    narcan_df = load_data("/Users/mengyu/code/sfpd-data/data/processed/narcan_deployment.csv")
    drug_arrest_df = load_data("/Users/mengyu/code/sfpd-data/data/processed/drug_arrest_data.csv")
    narcan_df = narcan_df.drop(columns=["Unnamed: 0"])
    drug_arrest_df = drug_arrest_df.drop(columns=["Unnamed: 0"])

    ## display filters and maps
    year_options = ['All years'] + sorted(narcan_df['Incident Year'].unique(), reverse=True)
    neighborhood_options = ['All neighborhoods'] + sorted(narcan_df['Analysis Neighborhood'].unique())

    narcan_year_filter = st.selectbox('Narcan data: Select year:', year_options)
    narcan_neighborhood_filter = st.selectbox('Narcan data: Select neighborhood:', neighborhood_options)

    drug_year_filter = st.selectbox('Drug arrest data: Select year:', year_options)
    drug_neighborhood_filter = st.selectbox('Drug arrest data: Select neighborhood:', neighborhood_options)

    st.subheader("Narcan Deployment")
    narcan_filtered_df, narcan_total, narcan_map = filter_data(narcan_df, narcan_year_filter, narcan_neighborhood_filter)
    st.metric("Total number of Narcan deployment:", narcan_total)
    st.write(narcan_filtered_df)
    st.write(streamlit_folium.folium_static(narcan_map))

    st.subheader("Drug-Related Arrests")
    drug_filtered_df, drug_total, drug_map = filter_data(drug_arrest_df, drug_year_filter, drug_neighborhood_filter)
    st.metric("Total number of drug-related arrests:", drug_total)
    st.write(drug_filtered_df)
    st.write(streamlit_folium.folium_static(drug_map))

if __name__ == "__main__":
    main()