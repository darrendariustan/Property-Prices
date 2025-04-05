## Own version

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load dataset
@st.cache_data
def load_data():
    file_path = "french_real_estate_sales_raw.csv"
    df = pd.read_csv(file_path, low_memory=False)
    return df

df = load_data()

# Streamlit App Title
st.title("French Real Estate Property Viewer")

# User Selection
property_selection = st.selectbox(
    "Select a Property by Street Name:",
    df["adresse_nom_voie"].dropna().unique()
)

# Filter dataset based on selection
selected_data = df[df["adresse_nom_voie"] == property_selection] #Feature 1

# Allow users to pick one specific property using its unique ID
if not selected_data.empty:
    property_id = st.selectbox(
        "Select a specific property:",
        selected_data["id_mutation"].unique()
    )
    selected_data = selected_data[selected_data["id_mutation"] == property_id]

# Display details of selected property (Features 2, 3, 4, 5, 6)
if not selected_data.empty:
    st.subheader("Property Details")
    st.write(selected_data[["code_postal", "type_local", "valeur_fonciere", "nombre_pieces_principales", "surface_reelle_bati"]].drop_duplicates())
    
    # Map Visualization (Feature 7, 8)
    st.subheader("Location Map")
    map_center = [selected_data.iloc[0]["latitude"], selected_data.iloc[0]["longitude"]]
    m = folium.Map(location=map_center, zoom_start=15)
    for _, row in selected_data.iterrows():
        # Ensure the value is a valid number before displaying it
        price = row["valeur_fonciere"] if pd.notna(row["valeur_fonciere"]) and row["valeur_fonciere"] >= 0 else "N/A"

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['type_local']}: {row['valeur_fonciere']}€",
        ).add_to(m)
    folium_static(m)
else:
    st.warning("No data available for the selected property.")
