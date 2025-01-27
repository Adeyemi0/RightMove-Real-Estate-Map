# London Property Listings Scraper

This project is a Streamlit app that scrapes property listings from the Rightmove website based on user-specified station locations in London. It allows users to filter property listings by the number of bedrooms, price, and property type, and visualize the results on a map.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Visualizing the Data](#visualizing-the-data)
- [Requirements](#requirements)
- [Contributing](#contributing)

## Features
- Select a station from a dropdown list to scrape property listings within the proximity.
- Filter properties by:
  - Maximum number of bedrooms
  - Maximum price (£)
  - Property type (Detached, Semi-detached, Terraced, Flat, Bungalow)
- Scrapes property details such as:
  - Property ID
  - Address
  - Bedrooms and Bathrooms
  - Property Type
  - Price (per month or per week)
  - Property Size
  - Listing Date
  - Property URL
  - Latitude and Longitude (for mapping)
  - Images
- Map visualization of properties on a Folium map.
- Integration with a CSV of amenities data for better property analysis (optional).

## Installation
To run the project locally, follow these steps:

### Clone the repository:
```bash
git clone https://github.com/RightMove-Real-Estate-Map.git
```

### Navigate into the project directory:
```bash
cd london-property-listings-scraper
```

### Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

### Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Run the Streamlit app:
```bash
streamlit run app.py
```

Open the app in your browser at [https://rightmove-real-estate-map-eqbj5l5mmdhngphloomwsg.streamlit.app/).

## Usage
1. After launching the app, you will see a dropdown to select a station in London.
2. You can enter optional filters such as the maximum number of bedrooms, price limit, and property type.
3. Click on the **Search Properties** button to begin scraping property data.
4. Once the scraping is complete, the property listings will be displayed in a DataFrame below.
5. You can visualize the properties on a map by clicking the **'Map View'** option.

## How it works
### Web Scraping:
- The app uses `requests` to scrape property data from Rightmove, a popular UK property listing website.
- It uses a `UserAgent` object from the `fake_useragent` library to generate random user agents to mimic a real browser.
- The scraped data is parsed using `BeautifulSoup` and extracted as JSON objects from the Rightmove page.

### Mapping:
- Property locations (latitude, longitude) are extracted and visualized on a `Folium` map using `MarkerCluster` to show multiple points in proximity.
- Optionally, additional amenities data can be visualized alongside the property listings.

### Rate Limiting:
- Scraping requests are spaced out using the `time.sleep()` method to avoid overwhelming the website.

## Visualizing the Data
The app uses `Folium` to provide an interactive map showing the locations of scraped properties.

### Map View:
- A map of London is displayed with markers representing properties near the selected station.
- Markers are clustered for easier visualization.

### CSV Integration (Optional):
- The app allows loading additional amenity data from a CSV file (`amenity_data_london.csv`) to show nearby amenities like schools, parks, etc.

## Requirements
Below is the list of Python dependencies required for this project. These can be installed using pip from the `requirements.txt` file.

```bash
streamlit
requests
beautifulsoup4
fake_useragent
pandas
folium
geopy
streamlit_folium
```

## Contributing
Contributions are welcome! If you’d like to contribute:

1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-branch-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch-name
   ```
5. Open a pull request.


