import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import Polygon
import requests
import json
import math
from datetime import datetime, timedelta
from branca.colormap import linear
import numpy as np



def irrigation_mapping():
    st.title("Irrigation Mapping")

    # Load Kc values from the uploaded JSON file
    with open('utils/kc_values.json', 'r') as f:
        kc_values = json.load(f)

    # NASA POWER API fetch function
    def fetch_nasa_power_data(latitude, longitude, date):
        base_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PS,ALLSKY_SFC_SW_DWN,T2M_MAX,T2M_MIN,WS2M,RH2M&community=AG&longitude={longitude}&latitude={latitude}&start={date}&end={date}&format=JSON"
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()['properties']['parameter']
            return data
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
            return None

    # Function to calculate ET₀ (Reference Evapotranspiration)
    def calculate_et0(data, date):
        gamma = 0.665e-3 * data['PS'][date]  # Psychrometric constant (kPa/°C)
        Rn = data['ALLSKY_SFC_SW_DWN'][date] * 0.0864  # Convert W/m² to MJ/m²/day
        T_max = data['T2M_MAX'][date]  # Max temperature (°C)
        T_min = data['T2M_MIN'][date]  # Min temperature (°C)
        T_mean = (T_max + T_min) / 2  # Mean temperature
        U2 = data['WS2M'][date]  # Wind speed at 2m (m/s)
        RH_mean = data['RH2M'][date]  # Mean relative humidity (%)

        # Calculate saturation vapor pressure (kPa)
        e_s = 0.6108 * (math.exp((17.27 * T_max) / (T_max + 237.3)) + math.exp((17.27 * T_min) / (T_min + 237.3))) / 2
        # Actual vapor pressure (kPa)
        e_a = e_s * (RH_mean / 100)
        # Slope of vapor pressure curve (kPa/°C)
        delta = (4098 * (0.6108 * math.exp((17.27 * T_mean) / (T_mean + 237.3)))) / ((T_mean + 237.3) ** 2)

        # Penman-Monteith equation for ET₀
        ET0 = (0.408 * delta * (Rn - 0) + gamma * (900 / (T_mean + 273)) * U2 * (e_s - e_a)) / (delta + gamma * (1 + 0.34 * U2))
        return ET0

    # Function to calculate water needed based on ET₀ and crop coefficient
    def calculate_water_needed(et0, kc):
        return max(0, kc * et0)

    # Initialize the map at a farm location in California, USA
    farm_latitude = 36.3295  # Latitude of a farm in Central Valley, CA
    farm_longitude = -119.3091  # Longitude of a farm in Central Valley, CA
    m = folium.Map(location=[farm_latitude, farm_longitude], zoom_start=12)

    # Allow user to draw polygons on the map
    folium.plugins.Draw(export=True).add_to(m)
    st_folium_map = st_folium(m, width=700, height=500)

    # Check if there are any drawings in the map output
    if st_folium_map and 'all_drawings' in st_folium_map:
        drawings = st_folium_map['all_drawings']
        if len(drawings) == 0:
            st.warning("No drawings detected. Please draw a polygon or rectangle.")
        else:
            # Loop through each drawing (polygon or rectangle)
            for drawing in drawings:
                geometry = drawing['geometry']
                coordinates = geometry['coordinates'][0]

                # Check if it's a valid polygon
                if len(coordinates) < 4:
                    st.error("Invalid geometry detected. Ensure you draw a proper polygon.")
                    continue

                polygon = Polygon(coordinates)

                # Function to divide the polygon into a grid of smaller polygons
                def divide_polygon(polygon, grid_size):
                    minx, miny, maxx, maxy = polygon.bounds
                    grid_polygons = []
                    for x in np.arange(minx, maxx, grid_size):
                        for y in np.arange(miny, maxy, grid_size):
                            grid_cell = Polygon([(x, y), (x + grid_size, y), (x + grid_size, y + grid_size), (x, y + grid_size)])
                            if grid_cell.intersects(polygon):
                                grid_polygons.append(grid_cell.intersection(polygon))
                    return grid_polygons

                # Date range for NASA POWER data
                current_date = datetime.now()
                five_days_before = current_date - timedelta(days=5)
                date = five_days_before.strftime("%Y%m%d")

                irrigation_results = {}

                # Divide the polygon into smaller grid cells
                grid_polygons = divide_polygon(polygon, grid_size=0.001)  # Grid size in degrees, adjust as needed

                # Crop and growth stage selection
                crop = st.selectbox("Select Crop Type", list(kc_values.keys()))
                growth_stage = st.selectbox("Select Growth Stage", kc_values[crop].keys())
                kc = kc_values[crop][growth_stage]

                # Loop through each grid polygon
                for grid in grid_polygons:
                    centroid = grid.centroid
                    latitude, longitude = centroid.y, centroid.x

                    # Fetch weather data from NASA POWER API
                    data = fetch_nasa_power_data(latitude, longitude, date)
                    if data:
                        et0 = calculate_et0(data, date)  # Calculate ET₀
                        water_needed = calculate_water_needed(et0, kc)  # Calculate irrigation requirement
                        irrigation_results[grid] = water_needed

                # Convert results to GeoDataFrame for visualization
                gdf = gpd.GeoDataFrame({'geometry': list(irrigation_results.keys()), 'water_needed': list(irrigation_results.values())})

                # Create color map for irrigation needs
                colormap = linear.YlGnBu_09.scale(gdf['water_needed'].min(), gdf['water_needed'].max())
                colormap.caption = 'Irrigation Needs (mm/day)'

                # Create a new map centered at the location
                map_with_irrigation = folium.Map(location=[latitude, longitude], zoom_start=12)
                map_with_irrigation.add_child(colormap)

                # Add grid cells with color-coding to the map
                for _, row in gdf.iterrows():
                    water_needed = row['water_needed']
                    color = colormap(water_needed)
                    folium.GeoJson(
                        row['geometry'],
                        style_function=lambda x, color=color: {
                            'fillColor': color,
                            'color': 'black',
                            'weight': 0.5,
                            'fillOpacity': 0.6
                        }
                    ).add_to(map_with_irrigation)

                # Display the map in Streamlit
                st_folium(map_with_irrigation, width=700, height=500)