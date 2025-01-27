import streamlit as st
import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from geopy.distance import geodesic
from streamlit_folium import folium_static

# Initialize UserAgent object
ua = UserAgent()

# Dictionary of station identifiers
identifiers = {
    "Liverpool Street": "5E5615",
    "Bank": "5E551",
    "Moorgate": "5E6332",
    "Farringdon": "5E3431",
    "Barking": "5E587",
    "Dagenham Heathway": "5E2576",
    "Becontree": "5E761",
    "High Barnet": "5E4553",
    "Hendon": "5E4475",
    "Mill Hill Broadway": "5E6230",
    "Bexleyheath": "5E926",
    "Welling": "5E9740",
    "Sidcup": "5E8252",
    "Wembley Central": "5E9776",
    "Wembley Park": "5E9782",
    "Kilburn": "5E5120",
    "Bromley South": "5E1442",
    "Orpington": "5E6911",
    "Beckenham Junction": "5E743",
    "Euston": "5E3311",
    "King's Cross St Pancras": "5E5165",
    "Camden Town": "5E1712",
    "East Croydon": "5E3056",
    "West Croydon": "5E9818",
    "Norwood Junction": "5E6815",
    "Ealing Broadway": "5E3023",
    "Southall": "5E8459",
    "Acton Town": "5E77",
    "Enfield Town": "5E3272",
    "Southgate": "5E8489",
    "Edmonton Green": "5E3179",
    "North Greenwich": "5E6719",
    "Greenwich": "5E4001",
    "Woolwich Arsenal": "5E10286",
    "Hackney Central": "5E4073",
    "Dalston Junction": "5E15132",
    "Homerton": "5E4694",
    "Hammersmith": "5E4172",
    "Fulham Broadway": "5E3644",
    "Shepherd's Bush": "5E8156",
    "Wood Green": "5E10229",
    "Tottenham Hale": "5E9275",
    "Finsbury Park": "5E3515",
    "Harrow-on-the-Hill": "5E4289",
    "Harrow & Wealdstone": "5E4283",
    "Kenton": "5E5078",
    "Romford": "5E7769",
    "Upminster": "5E9434",
    "Gidea Park": "5E3737",
    "Uxbridge": "5E9473",
    "Ruislip": "5E7859",
    "West Drayton": "5E9824",
    "Hounslow Central": "5E4763",
    "Feltham": "5E3467",
    "Chiswick": "5E2081",
    "Angel": "5E245",
    "Highbury & Islington": "5E4583",
    "South Kensington": "5E8414",
    "Earls Court": "5E3038",
    "Notting Hill Gate": "5E6818",
    "Kingston": "5E5201",
    "Surbiton": "5E8912",
    "Norbiton": "5E6686",
    "Waterloo": "5E9662",
    "Brixton": "5E1400",
    "Clapham North": "5E2159",
    "Lewisham": "5E5525",
    "New Cross": "5E6536",
    "Catford": "5E1874",
    "Wimbledon": "5E10127",
    "Colliers Wood": "5E2255",
    "Morden": "5E6353",
    "Stratford": "5E8813",
    "Canning Town": "5E1733",
    "East Ham": "5E3080",
    "Ilford": "5E4877",
    "Gants Hill": "5E3668",
    "Wanstead": "5E9596",
    "Richmond": "5E7703",
    "Twickenham": "5E9365",
    "Kew Gardens": "5E5093",
    "London Bridge": "5E5792",
    "Canada Water": "5E1721",
    "Peckham Rye": "5E7070",
    "Sutton": "5E8918",
    "Carshalton": "5E1832",
    "Cheam": "5E1976",
    "Whitechapel": "5E10022",
    "Bethnal Green": "5E905",
    "Shadwell": "5E8102",
    "Walthamstow Central": "5E9587",
    "Leytonstone": "5E9557",
    "Chingford": "5E2057",
    "Clapham Junction": "5E2156",
    "Wandsworth Town": "5E5543",
    "Putney": "5E7478",
    "Victoria": "5E9491",
    "Paddington": "5E6965",
    "Charing Cross": "5E1940"
}

# Function to get cookies for each iteration
def get_cookies():
    return {'cookie_name': 'cookie_value'}

# Function to scrape property listings
def scrape_property_listings(url, max_pages=10):
    all_properties = []

    for page_num in range(max_pages):
        updated_url = f"{url}&index={page_num * 24}"  # 24 results per page
        headers = {'User-Agent': ua.random}
        cookies = get_cookies()
        
        response = requests.get(updated_url, headers=headers, cookies=cookies)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            json_data = soup.find('script', string=lambda text: text and 'window.jsonModel' in text)
            
            if json_data:
                try:
                    start_index = json_data.string.find('{"properties":')
                    json_model_str = json_data.string[start_index:]
                    properties = json.loads(json_model_str).get('properties', [])
                    
                    if not properties:
                        st.write(f"No properties found on page {page_num + 1}. Scraping stopped.")
                        break
                    
                    for property in properties:
                        property_url = f"https://www.rightmove.co.uk/properties/{property['id']}"
                        price_data = property.get('price', {})
                        pcm_price = pw_price = None
                        
                        if 'displayPrices' in price_data:
                            for price in price_data['displayPrices']:
                                if 'pcm' in price['displayPrice'].lower():
                                    pcm_price = price['displayPrice']
                                if 'pw' in price['displayPrice'].lower():
                                    pw_price = price['displayPrice']
                                    
                        property_data = {
                            'Property ID': property['id'],
                            'Summary': property['summary'],
                            'Address': property['displayAddress'],
                            'Bedrooms': property['bedrooms'],
                            'Bathrooms': property['bathrooms'],
                            'Longitude': property['location']['longitude'],
                            'Latitude': property['location']['latitude'],
                            'Property URL': property_url,
                            'Property type': property['propertySubType'],
                            'Listing Date': property.get("firstVisibleDate"),
                            'PCM Price': pcm_price,
                            'PW Price': pw_price,
                            'Size': property.get("displaySize"),
                            "Images": [img['srcUrl'] for img in property.get('propertyImages', {}).get('images', [])]
                        }
                        all_properties.append(property_data)
                except Exception as e:
                    st.error(f"Error parsing property data: {e}")
        else:
            st.error(f"Failed to retrieve data from {updated_url}")
        
        time.sleep(random.uniform(1, 3))
    
    df = pd.DataFrame(all_properties)
    df['Images'] = df['Images'].apply(lambda x: x[0] if isinstance(x, list) and x else None)
    return df



# Streamlit App
st.title('London Property Listings Scraper')

# User input for station name
station_name = st.selectbox("Choose a station:", list(identifiers.keys()))

# Optional user inputs
max_bedrooms = st.number_input("Enter maximum number of bedrooms (optional):", min_value=0, step=1, key="max_bedrooms", value=0)
max_price = st.number_input("Enter maximum price (£) (optional):", min_value=0, step=100, key="max_price", value=0)
property_type = st.selectbox("Select property type (optional):", ['', 'Detached', 'Semi-detached', 'Terraced', 'Flat', 'Bungalow'])

if st.button('Search Properties'):
    status_message = st.empty()
    status_message.text("Starting the scraping process...")
    # Build the base URL
    base_url = f"https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=STATION%{identifiers[station_name]}"

    # Add optional parameters if the user provided values
    if max_bedrooms > 0:
        base_url += f"&maxBedrooms={max_bedrooms}"
    if max_price > 0:
        base_url += f"&maxPrice={max_price}"
    if property_type:
        base_url += f"&propertyTypes={property_type}"
    
    # Scrape the listings
    df_properties = scrape_property_listings(base_url)
    
    if not df_properties.empty: 
        status_message.text("Scraping is complete!")
        # Load the CSV file into a DataFrame (replace this with your actual file path)
        point_geometries = pd.read_csv("amenity_data_london.csv")

        # 📍 Initialize Folium Map
        m = folium.Map(location=[51.5, -0.12], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)

        # 🏠 Function to find nearest amenities for each type
        def find_nearest_amenities(property_lat, property_lon):
            nearest_amenities = {}
            for amenity in ['hospital', 'restaurant', 'school', 'bus_station', 'train_station']:
                subset = point_geometries[point_geometries['amenity_type'] == amenity]
                if subset.empty:
                    continue
                distances = subset.apply(
                    lambda row: geodesic((property_lat, property_lon), (row['latitude'], row['longitude'])).meters, axis=1
                )
                if distances.empty:  # Ensure distances exist before indexing
                    continue
                nearest_idx = distances.idxmin()

                if nearest_idx not in subset.index:  # Avoid out-of-bounds indexing
                    continue
                nearest_amenity = subset.loc[nearest_idx]
                nearest_name = nearest_amenity['name'] if pd.notna(nearest_amenity['name']) and nearest_amenity['name'] else "Unknown"
                nearest_amenities[amenity] = (nearest_name, distances.min())
                
            return nearest_amenities

        # Add Property Markers
        for idx, row in df_properties.iterrows():
            property_lat, property_lon = row['Latitude'], row['Longitude']
            nearest_amenities = find_nearest_amenities(property_lat, property_lon)
            amenities_html = "".join(
                f"<b>Nearest {amenity.capitalize()}:</b> {info[0]} - {info[1]:.2f}m<br>"
                for amenity, info in nearest_amenities.items()
            )
            address = row.get('Address', 'Address not available') 
            if isinstance(row['Images'], str) and row['Images'].strip():
                image_url = row['Images'].split(',')[0].strip()  # Take the first image
            else:
                image_url = "https://via.placeholder.com/200"  # Placeholder if empty
            
            popup_html = f"""
            <div style="font-family: Arial, sans-serif;">
            <h4 style="color: #2a2a2a; font-size: 20px; margin-bottom: 10px;">Property Description</h4>
            <p style="color: #555; font-size: 16px; margin-bottom: 15px; line-height: 1.5;">{row['Summary']}</p>
            <img src="{image_url}" width="100%" style="border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); margin-bottom: 10px;">
            <div style="margin-bottom: 10px;">
            <b>Address:</b> {address}<br><br>
            <b>Bedrooms:</b> {row['Bedrooms']} | <b>Bathrooms:</b> {row['Bathrooms']}<br>
            <b>PCM Price:</b> <span style="color: #006400; font-weight: bold;">{row['PCM Price']}</span><br><br>
            </div>
            <div style="margin-bottom: 15px;">
            <h5 style="color: #2a2a2a; font-size: 16px;">Nearest Amenities</h5>
            {amenities_html}
            </div>
            <a href="{row['Property URL']}" target="_blank" 
            style="display: inline-block; text-decoration: none; padding: 10px 15px; background-color: #007bff; color: white; border-radius: 5px; font-weight: bold;">
            View Property
            </a>
            </div>
            """

            folium.Marker(
                location=[property_lat, property_lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"Price: {row['PCM Price']} | {row['Address']}",
                icon=folium.Icon(color="blue", icon="home")
                ).add_to(marker_cluster)
            
        folium_static(m)

        # Save the map to an HTML file
        map_filename = "london_property_map.html"
        m.save(map_filename)

    else:
        st.write("No properties found.")
