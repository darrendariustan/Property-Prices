import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

print("Loading data...")
# Load Data with correct dtype handling
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

print("Training model...")
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

# Create pipeline with a much smaller model
pipe_rf = Pipeline([
    ('preprocessor', preprocessor),
    ('scale', StandardScaler()),
    ('regressor', RandomForestRegressor(
        n_estimators=50,      # Reduced from 200
        max_depth=10,         # Reduced from 30
        min_samples_leaf=5,   # Increased from 1
        random_state=42
    ))
])

# Train model
pipe_rf.fit(X_train, y_train)

print("Saving model to pickle file...")
# Save model to pickle file
with open("house_price_model.pkl", "wb") as f:
    pickle.dump(pipe_rf, f)

# Also save a smaller version of the dataset for faster loading in the app
print("Saving processed dataset...")
df.to_csv("processed_apartments.csv", index=False)

print("Done! Model and processed dataset saved successfully.") 