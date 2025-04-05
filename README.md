# French Real Estate Property Viewer

A Streamlit web application for exploring and visualizing French real estate property data. This interactive tool allows users to browse properties by location, view detailed property information, and see property locations on an interactive map.

## Features

- **Property Selection**: Browse properties by street name
- **Detailed Information**: View property details including:
  - Postal code
  - Property type
  - Property value
  - Number of rooms
  - Surface area (in square meters)
- **Interactive Map**: Visualize the exact location of properties using an interactive map
- **Filtering Capabilities**: Select specific properties using unique IDs

## Dataset

The application uses the `french_real_estate_sales_raw.csv` dataset, which contains detailed information about real estate sales in France including:
- Property locations (addresses, coordinates)
- Property characteristics (type, size, number of rooms)
- Sale values
- Property IDs and other metadata

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/darrendariustan/property-prices.git
   cd property-prices
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
   streamlit run property_viewer.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Use the dropdown menus to select properties by street name and specific property ID

4. View property details and location on the interactive map

## Dependencies

- streamlit - Web application framework
- pandas - Data manipulation and analysis
- scikit-learn - Machine learning utilities
- seaborn - Statistical data visualization
- matplotlib - Plotting library
- watchdog - File system monitoring
- geopy - Geocoding operations

## Project Structure

- `property_viewer.py` - Main Streamlit application
- `french_real_estate_sales_raw.csv` - Dataset of French real estate properties
- `map_code.ipynb` - Jupyter notebook with mapping functionality development
- `requirements.txt` - Project dependencies

## Future Enhancements

- Price prediction functionality
- Advanced filtering options
- Trend analysis for property values by region
- Comparative analysis between different property types

## License

This project is available for educational and personal use.

---

Created as part of the Prototyping Data & AI course at ESADE Business School.
