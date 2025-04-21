# Apartment Price Estimator

A Streamlit web application for analyzing French apartment prices. This interactive tool helps users determine if properties are underpriced or overpriced based on machine learning predictions.

## Live Demo

The application is deployed and can be accessed at: [Apartment Price Estimator](https://your-render-url-here.onrender.com)

## Features

- **Intuitive Interface**: Easy-to-use interface for property selection and analysis
- **Location-Based Selection**: Find properties by area, street, and specific apartment
- **Advanced Filtering**: Filter properties by:
  - Surface area (m²)
  - Number of rooms
- **Price Comparison**: See actual vs. predicted prices with:
  - Price per square meter (€/m²) calculations
  - Percentage difference analysis
  - Clear underpriced/overpriced indicators
- **Interactive Maps**: Two map visualizations:
  - Selected apartment with price details
  - Similar properties in the area with underpriced/overpriced color coding
- **Postal Code Analysis**: Test how postal codes affect property values with sensitivity analysis

## Dataset

The application uses the `french_real_estate_sales_raw.csv` dataset containing detailed information about real estate sales in France including:
- Property locations (addresses, coordinates)
- Property characteristics (type, size, number of rooms)
- Sale values
- Postal codes and other geographical data

## Machine Learning Model

The application uses a Random Forest Regressor for price prediction with:
- OneHotEncoding for postal codes
- Standardized scaling for numeric features
- High-dimensional feature handling for location data

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/apartment-price-estimator.git
   cd apartment-price-estimator
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run apartment_price_estimator.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Select an area, street, and apartment using the dropdowns

4. Apply filters if needed to narrow down property options

5. View the price analysis and prediction

6. Explore similar properties on the interactive map

## Deployment

### Deploy to Render

1. Create a [Render](https://render.com/) account if you don't have one already.

2. Click "New +" button in the Render dashboard and select "Web Service".

3. Connect your GitHub repository or use the "Public Git repository" option with the URL of your repository.

4. Fill in the following details:
   - Name: apartment-price-estimator (or your preferred name)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run apartment_price_estimator.py --server.port $PORT --server.address 0.0.0.0`

5. Choose a plan (Free plan works fine for this application)

6. Click "Create Web Service"

7. Wait for the deployment to complete and access your app at the provided URL.

## Dependencies

- streamlit - Web application framework
- pandas - Data manipulation and analysis
- scikit-learn - Machine learning models and preprocessing
- numpy - Numerical computing
- folium - Interactive map creation
- streamlit-folium - Streamlit component for Folium maps
- watchdog - File system monitoring (for Streamlit hot-reloading)

## Project Structure

- `apartment_price_estimator.py` - Main Streamlit application
- `french_real_estate_sales_raw.csv` - Dataset of French real estate properties
- `requirements.txt` - Project dependencies
- `render.yaml` - Configuration for Render deployment
- `setup.sh` - Setup script for Streamlit configuration
- `Procfile` - Process file for web deployment

## License

Created as part of the Prototyping Data & AI course at ESADE Business School.
