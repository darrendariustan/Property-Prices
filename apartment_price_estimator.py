import streamlit as st
import pandas as pd
import pickle
import numpy as np
import folium
from streamlit_folium import folium_static
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import os

# Page configuration
st.set_page_config(
    page_title="Apartment Price Estimator",
    layout="wide"
)

# Load Data with correct dtype handling
@st.cache_data
def load_data():
    # Try to load the preprocessed dataset first, if it exists
    if os.path.exists("processed_apartments.csv"):
        print("Loading preprocessed data...")
        return pd.read_csv("processed_apartments.csv", dtype={'code_postal': str})
    
    # Fallback to original dataset if preprocessed doesn't exist
    print("Loading original data...")
    FILE_URL = "french_real_estate_sales_raw.csv"
    df = pd.read_csv(FILE_URL, dtype={'code_postal': str}, low_memory=False)
    
    # Filter valid data
    df = df[df['latitude'].notna() & df['longitude'].notna()]
    df = df[(df['valeur_fonciere'] > 10000) & (df['valeur_fonciere'] < 2000000)]
    
    # Keep only relevant columns and drop missing values
    df = df[['valeur_fonciere', 'surface_reelle_bati', 'nombre_pieces_principales', 
             'code_postal', 'nom_commune', 'adresse_nom_voie', 'type_local', 'latitude', 'longitude']].dropna()
    
    # Filter to apartments only
    df = df[df['type_local'] == 'Appartement']
    
    return df

# Load data
df = load_data()

# Load pre-trained model or train model if not available
@st.cache_resource
def load_model():
    # Try to load pre-trained model
    try:
        print("Loading pre-trained model...")
        with open("house_price_model.pkl", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError) as e:
        print(f"Pre-trained model not found: {e}. Training new model...")
        # If model file doesn't exist, train the model
        return prepare_model(df)

# Train model function (used only if pre-trained model is not available)
def prepare_model(df):
    # Create feature matrix X and target vector y
    X = df[['code_postal', 'nombre_pieces_principales', 'surface_reelle_bati']]
    y = df['valeur_fonciere']
    
    # Create train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['code_postal']),
            ('num', 'passthrough', ['nombre_pieces_principales', 'surface_reelle_bati'])
        ]
    )
    
    # Create pipeline
    pipe_rf = Pipeline([
        ('preprocessor', preprocessor),
        ('scale', StandardScaler()),
        ('regressor', RandomForestRegressor(
            n_estimators=50,      # Reduced from 100
            max_depth=10,         # Reduced from 20
            min_samples_leaf=5,   # Increased from 1
            random_state=42
        ))
    ])
    
    # Train model (with reduced complexity for faster training)
    pipe_rf.fit(X_train, y_train)
    
    # Save model to pickle file for future use
    try:
        with open("house_price_model.pkl", "wb") as f:
            pickle.dump(pipe_rf, f)
        print("Model trained and saved successfully!")
    except Exception as e:
        print(f"Warning: Could not save model to file: {e}")
    
    return pipe_rf

# Load or prepare model
pipe_rf = load_model()

# Main UI
st.title("\U0001F3E0 Apartment Price Estimator")
st.write("Select an apartment to check if it's *underpriced or overpriced*")

# Dropdown Selections: Choose Area and Street
city = st.selectbox("Select Area", sorted(df["nom_commune"].unique()))
filtered_df = df[df["nom_commune"] == city]

street = st.selectbox("Select Street", sorted(filtered_df["adresse_nom_voie"].unique()))
filtered_df = filtered_df[filtered_df["adresse_nom_voie"] == street]

# Add advanced filters for size and number of rooms if there are multiple properties
if len(filtered_df) > 1:
    st.subheader("Filter Properties")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Surface area range filter
        min_surface = int(filtered_df["surface_reelle_bati"].min())
        max_surface = int(filtered_df["surface_reelle_bati"].max())
        surface_range = st.slider("Surface Area (m²)", 
                                 min_value=min_surface, 
                                 max_value=max_surface, 
                                 value=(min_surface, max_surface))
        
    with col2:
        # Number of rooms filter
        room_counts = sorted(filtered_df["nombre_pieces_principales"].unique())
        selected_rooms = st.multiselect("Number of Rooms", 
                                     options=room_counts,
                                     default=room_counts)
    
    # Apply filters
    filtered_df = filtered_df[(filtered_df["surface_reelle_bati"] >= surface_range[0]) & 
                            (filtered_df["surface_reelle_bati"] <= surface_range[1])]
    
    if selected_rooms:
        filtered_df = filtered_df[filtered_df["nombre_pieces_principales"].isin(selected_rooms)]
    
    # Show filter results 
    st.info(f"Found {len(filtered_df)} properties matching your filters.")

# Use a meaningful identifier instead of index
filtered_df = filtered_df.reset_index(drop=True)
filtered_df['address_id'] = filtered_df.index

# Calculate price per square meter for better comparison
filtered_df['price_per_sqm'] = filtered_df['valeur_fonciere'] / filtered_df['surface_reelle_bati']

# Create more informative address display with price per sqm
address_display = [f"{row['adresse_nom_voie']} ({row['surface_reelle_bati']}m², {int(row['nombre_pieces_principales'])} rooms, €{row['valeur_fonciere']:,.0f} | €{row['price_per_sqm']:,.0f}/m²)" 
                  for _, row in filtered_df.iterrows()]

if len(address_display) > 0:
    selected_idx = st.selectbox("Select Apartment", range(len(address_display)), format_func=lambda x: address_display[x])
    
    # Retrieve Apartment Details
    apartment = filtered_df.iloc[selected_idx]
    size = apartment["surface_reelle_bati"]
    rooms = int(apartment["nombre_pieces_principales"])
    price_paid = apartment["valeur_fonciere"]
    postal_code = apartment["code_postal"]
    lat = apartment["latitude"]
    lon = apartment["longitude"]
    
    # Display price per square meter for easier comparison
    price_per_sqm = price_paid / size
    
    st.subheader("Apartment Details")
    st.write(f"\U0001F4CD *Location:* {city}, {street}")
    st.write(f"\U0001F4CF *Size:* {size} m²")
    st.write(f"\U0001F6CF *Rooms:* {rooms}")
    st.write(f"\U0001F4B0 *Price Paid:* €{price_paid:,.2f} (€{price_per_sqm:,.2f}/m²)")
    st.write(f"*Postal Code:* {postal_code}")
    
    # Ensure input features are correctly transformed
    input_df = pd.DataFrame([[postal_code, rooms, size]], 
                           columns=["code_postal", "nombre_pieces_principales", "surface_reelle_bati"])
    
    # Predict using pipeline
    predicted_price = pipe_rf.predict(input_df)[0]
    
    # Show difference between actual and predicted
    price_diff = predicted_price - price_paid
    percent_diff = (price_diff / price_paid) * 100
    
    # Calculate price per square meter for comparison
    price_per_sqm = price_paid / size
    predicted_price_per_sqm = predicted_price / size
    
    st.subheader("Predicted Apartment Price")
    st.write(f"\U0001F4B8 *Predicted Price:* €{predicted_price:,.2f} (€{predicted_price_per_sqm:,.2f}/m²)")
    
    # Compare with actual price
    if price_paid < predicted_price:
        st.success(f"The apartment is underpriced by €{price_diff:,.2f} ({percent_diff:.1f}%)!")
    else:
        st.error(f"The apartment is overpriced by €{-price_diff:,.2f} ({-percent_diff:.1f}%)!")
    
    # Test postal code sensitivity
    st.subheader("Postal Code Sensitivity Test")
    st.write("Testing how postal code affects predicted price:")
    
    # Get 5 random postal codes
    random_postal_codes = np.random.choice(df['code_postal'].unique(), 5)
    
    postal_test_results = []
    for test_code in random_postal_codes:
        test_input = input_df.copy()
        test_input['code_postal'] = test_code
        test_price = pipe_rf.predict(test_input)[0]
        postal_test_results.append({
            'postal_code': test_code,
            'predicted_price': test_price,
            'difference': test_price - predicted_price,
            'percent_diff': ((test_price - predicted_price) / predicted_price) * 100
        })
    
    # Display results
    postal_df = pd.DataFrame(postal_test_results)
    st.dataframe(postal_df)
    
    # Display map centered on selected apartment
    st.subheader("Apartment Map")
    m = folium.Map(location=[lat, lon], zoom_start=15)
    
    color = 'green' if price_paid < predicted_price else 'red'
    folium.Marker(
        location=[lat, lon],
        popup=f"Price Paid: €{price_paid:,.2f}<br>Predicted Price: €{predicted_price:,.2f}",
        icon=folium.Icon(color=color)
    ).add_to(m)
    
    folium_static(m)
    
    # Show similar properties in the area
    st.subheader("Similar Properties in this Area")
    
    # Find similar properties in the same postal code and with similar size
    similar_props = df[(df['code_postal'] == postal_code) & 
                       (df['surface_reelle_bati'] >= size * 0.8) &
                       (df['surface_reelle_bati'] <= size * 1.2) &
                       (df.index != apartment.name)]
    
    if len(similar_props) > 0:
        # Predict prices for similar properties
        similar_input = similar_props[['code_postal', 'nombre_pieces_principales', 'surface_reelle_bati']]
        similar_props['predicted_price'] = pipe_rf.predict(similar_input)
        
        # Create map
        sm = folium.Map(location=[lat, lon], zoom_start=14)
        
        # Add selected apartment
        folium.Marker(
            location=[lat, lon],
            popup=f"Selected Apartment<br>Price: €{price_paid:,.2f}<br>Predicted: €{predicted_price:,.2f}",
            icon=folium.Icon(color=color, icon='home')
        ).add_to(sm)
        
        # Add similar properties
        for _, row in similar_props.head(50).iterrows():
            sim_color = 'green' if row['valeur_fonciere'] < row['predicted_price'] else 'red'
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Size: {row['surface_reelle_bati']}m²<br>Rooms: {int(row['nombre_pieces_principales'])}<br>Price Paid: €{row['valeur_fonciere']:,.2f}<br>Predicted: €{row['predicted_price']:,.2f}",
                icon=folium.Icon(color=sim_color)
            ).add_to(sm)
        
        folium_static(sm)
        
        if len(similar_props) > 50:
            st.info(f"Showing 50 of {len(similar_props)} similar properties for performance reasons.")
            
        # Add legend explaining the markers
        legend_col1, legend_col2 = st.columns(2)
        with legend_col1:
            st.markdown("🟢 **Green**: Underpriced (actual < predicted)")
        with legend_col2:
            st.markdown("🔴 **Red**: Overpriced (actual > predicted)")
    else:
        st.info("No similar properties found in this area with comparable size.")
else:
    st.warning("No apartments found on this street. Please select another street.") 