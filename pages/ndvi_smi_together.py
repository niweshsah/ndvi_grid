import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import Draw
import folium
import shapely.geometry as geom
import numpy as np
import datetime
from sentinelhub import SHConfig, BBox, CRS, DataCollection, SentinelHubRequest, MimeType

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

def value_to_green_hex(ndvi_real, ndvi_max,ndvi_min):

    if ndvi_max != ndvi_min:
     value = (ndvi_real - ndvi_min)/(ndvi_max - ndvi_min)
     value = round(value,3)
    else:
     value = 1

    if not 0 <= value <= 1:
        print(value)
        raise ValueError("Input must be between 0 and 1")


    print("value: ",value)


    red_blue_component = int(255 * (1 - value))
    green_component = 255  # Green stays constant at 255
    
    # Create the hex color code
    hex_color = f"#{red_blue_component:02x}{green_component:02x}{red_blue_component:02x}"

    return hex_color


def value_to_blue_hex(ndvi_real, ndvi_max,ndvi_min):

    if ndvi_max != ndvi_min:
     value = (ndvi_real - ndvi_min)/(ndvi_max - ndvi_min)
     value = round(value,3)
    else:
     value = 1

    if not 0 <= value <= 1:
        print(value)
        raise ValueError("Input must be between 0 and 1")
    

    # print("value: ",value)


    red_green_component = int(255 * (1 - value))
    blue_component = 255  # Green stays constant at 255
    
    # Create the hex color code
    hex_color = f"#{red_green_component:02x}{red_green_component:02x}{blue_component:02x}"

    return hex_color

def show_legend():
    # Define colormap from green (value=1) to brown (value=0)
    cmap = mpl.colors.LinearSegmentedColormap.from_list("custom_cmap", ["white", "green"])

    # Create a figure and axis for the colorbar
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)

    # Create a colorbar
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')

    # Set the colorbar ticks and labels
    cb.set_ticks([0, 0.5, 1])
    cb.set_ticklabels(['0 (requires crop health attention)', '0.5', '1 (healthy crop)'])

    # Display the colorbar in Streamlit
    st.pyplot(fig)

def get_soil_moisture(latitude, longitude, bbox_size_m=1000):
    """
    Get Soil Moisture Index (MOISTURE-INDEX) value for a given latitude and longitude using Sentinel Hub.
    
    :param latitude: float, latitude of the point of interest
    :param longitude: float, longitude of the point of interest
    :param access_token: str, Sentinel Hub access token
    :param bbox_size_m: int, size of the bounding box in meters (default: 1000 meters)
    :return: float, Soil Moisture Index (MOISTURE-INDEX) value
    """
    # Configure Sentinel Hub
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MjgwNzI4OTUsImlhdCI6MTcyODA2OTI5NSwianRpIjoiYTM2NTJjYWEtYTM4MS00MTk4LTkwYjAtNjc2YzM1ZTBmMmFhIiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJzdWIiOiI1NGI3OGM4Ni04OTliLTRkZjctOTlmYi00OTQzMWM4MWJlZjIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiIwYzY4Mjk2Ni1kNjhjLTQ5YjYtYmI4MC1kYWQ1Yjk5OGE2NTMiLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRIb3N0IjoiMTQuMTM5LjM0LjEwMSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTBjNjgyOTY2LWQ2OGMtNDliNi1iYjgwLWRhZDViOTk4YTY1MyIsImNsaWVudEFkZHJlc3MiOiIxNC4xMzkuMzQuMTAxIiwiYWNjb3VudCI6ImM5Yzk0ODdlLWNhOTEtNDdmOS05Nzk1LWUwNWFjNWNkN2VjYiIsImNsaWVudF9pZCI6IjBjNjgyOTY2LWQ2OGMtNDliNi1iYjgwLWRhZDViOTk4YTY1MyJ9.dUHiDH2UZgpiw0I3a4S3RhhCcizUbHZuSz9o8KC64fzvnnCb8cpieDzEHoLqJrMWARCYZdcGE6R8O2ar_7eh-3EdkbXmiUXEBgF2qx_ZALbKAap_Ko2VVwqLaIF9AReF4uQF2rffByw3JNRVz-WhsjIINbJ-8ktGvY8DhsdX7iUoCrxAO1E8G8QJSAJILftyJiIYNhM1afQozLKJnAjRqT-i-D0dhmMihrqExu6KtS9bHZdIjPnGhpn7Rd9isesHj-DvWPujmGCEIUt_WQzaXwp6k_XSMrpqCa6Wh51Q375YloIe5x7QMRKCJo1tkl6FaqUh8ZC9NUA3B39UH5JCmw"

    client_id = '0c682966-d68c-49b6-bb80-dad5b998a653'
    client_secret = 'PMq7tG60PVURIo3DBzU39zvcdBizkZ5i'

    # Configure Sentinel Hub
    config = SHConfig()
    config.sh_client_id = client_id
    config.sh_client_secret = client_secret
    config.sh_token = access_token
    config.save()


    # Define bounding box (convert meters to degrees using a rough approximation for lat/lon)
    # Note: 1 degree of latitude is approximately 111 km (~111,000 meters)
    bbox_size_deg = bbox_size_m / 111000  # Convert meters to degrees
    
    bbox = BBox((longitude - bbox_size_deg / 2, latitude - bbox_size_deg / 2,
                 longitude + bbox_size_deg / 2, latitude + bbox_size_deg / 2), crs=CRS.WGS84)

    # Define pixel size in meters (set to 10 meters for Sentinel-2 data)
    pixel_size = 10

    # Calculate resolution in terms of pixels (area size in meters / pixel size)
    width_height = (int(bbox_size_m / pixel_size), int(bbox_size_m / pixel_size))

    # Define the Sentinel-2 L2A Soil Moisture Index evalscript
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B08", "B11"]
            }],
            output: {
                id: "default",
                bands: 1,
                sampleType: "FLOAT32"
            }
        };
    }

    function evaluatePixel(sample) {
        let moisture_index = (sample.B08 - sample.B11) / (sample.B08 + sample.B11);
        return [moisture_index];
    }
    """

    # Create a Sentinel Hub request
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=('2023-01-01', datetime.datetime.now().strftime('%Y-%m-%d')),
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF)
        ],
        bbox=bbox,
        size=width_height,  # Width/height derived from pixel size and bbox size
        config=config
    )

    # Get the data
    data = request.get_data()

    # Extract the Soil Moisture Index value (average of all pixels)
    moisture_values = data[0].flatten()
    moisture_index = float(moisture_values.mean())

    return moisture_index


def get_ndvi(latitude, longitude, bbox_size_m=1000):
    """
    Get NDVI value for a given latitude and longitude using Sentinel Hub.
    
    :param latitude: float, latitude of the point of interest
    :param longitude: float, longitude of the point of interest
    :param access_token: str, Sentinel Hub access token
    :param bbox_size_m: int, size of the bounding box in meters (default: 1000 meters)
    :return: float, NDVI value
    """


    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MjgwNzI4OTUsImlhdCI6MTcyODA2OTI5NSwianRpIjoiYTM2NTJjYWEtYTM4MS00MTk4LTkwYjAtNjc2YzM1ZTBmMmFhIiwiaXNzIjoiaHR0cHM6Ly9zZXJ2aWNlcy5zZW50aW5lbC1odWIuY29tL2F1dGgvcmVhbG1zL21haW4iLCJzdWIiOiI1NGI3OGM4Ni04OTliLTRkZjctOTlmYi00OTQzMWM4MWJlZjIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiIwYzY4Mjk2Ni1kNjhjLTQ5YjYtYmI4MC1kYWQ1Yjk5OGE2NTMiLCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJjbGllbnRIb3N0IjoiMTQuMTM5LjM0LjEwMSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LTBjNjgyOTY2LWQ2OGMtNDliNi1iYjgwLWRhZDViOTk4YTY1MyIsImNsaWVudEFkZHJlc3MiOiIxNC4xMzkuMzQuMTAxIiwiYWNjb3VudCI6ImM5Yzk0ODdlLWNhOTEtNDdmOS05Nzk1LWUwNWFjNWNkN2VjYiIsImNsaWVudF9pZCI6IjBjNjgyOTY2LWQ2OGMtNDliNi1iYjgwLWRhZDViOTk4YTY1MyJ9.dUHiDH2UZgpiw0I3a4S3RhhCcizUbHZuSz9o8KC64fzvnnCb8cpieDzEHoLqJrMWARCYZdcGE6R8O2ar_7eh-3EdkbXmiUXEBgF2qx_ZALbKAap_Ko2VVwqLaIF9AReF4uQF2rffByw3JNRVz-WhsjIINbJ-8ktGvY8DhsdX7iUoCrxAO1E8G8QJSAJILftyJiIYNhM1afQozLKJnAjRqT-i-D0dhmMihrqExu6KtS9bHZdIjPnGhpn7Rd9isesHj-DvWPujmGCEIUt_WQzaXwp6k_XSMrpqCa6Wh51Q375YloIe5x7QMRKCJo1tkl6FaqUh8ZC9NUA3B39UH5JCmw"



    client_id = '0c682966-d68c-49b6-bb80-dad5b998a653'
    client_secret = 'PMq7tG60PVURIo3DBzU39zvcdBizkZ5i'

    # Configure Sentinel Hub
    config = SHConfig()
    config.sh_client_id = client_id
    config.sh_client_secret = client_secret
    config.sh_token = access_token
    config.save()

    # Define bounding box (convert meters to degrees using a rough approximation for lat/lon)
    # Note: 1 degree of latitude is approximately 111 km (~111,000 meters)
    bbox_size_deg = bbox_size_m / 111000  # Convert meters to degrees
    
    bbox = BBox((longitude - bbox_size_deg / 2, latitude - bbox_size_deg / 2,
                 longitude + bbox_size_deg / 2, latitude + bbox_size_deg / 2), crs=CRS.WGS84)

    # Define pixel size in meters (set to 10 meters for Sentinel-2 data)
    pixel_size = 10

    # Calculate resolution in terms of pixels (area size in meters / pixel size)
    width_height = (int(bbox_size_m / pixel_size), int(bbox_size_m / pixel_size))

    # Define the Sentinel-2 L2A NDVI evalscript
    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B04", "B08"]
            }],
            output: {
                id: "default",
                bands: 1,
                sampleType: "FLOAT32"
            }
        };
    }

    function evaluatePixel(sample) {
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
        return [ndvi];
    }
    """

    # Create a Sentinel Hub request
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=('2023-01-01', datetime.datetime.now().strftime('%Y-%m-%d')),
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.TIFF)
        ],
        bbox=bbox,
        size=width_height,  # Width/height derived from pixel size and bbox size
        config=config
    )

    # Get the data
    data = request.get_data()

    # Extract the NDVI value (average of all pixels)
    ndvi_values = data[0].flatten()
    ndvi_value = float(ndvi_values.mean())

    return ndvi_value


# Initialize session state
if 'grid_squares' not in st.session_state:
    st.session_state.grid_squares_1 = []
    st.session_state.grid_squares_2 = []
if 'last_polygon' not in st.session_state:
    st.session_state.last_polygon = None

# Set up the Streamlit page
st.title("Polygon Grid Generator")
st.write("Draw a polygon on the left map, and see the result on the right!")

# Create two columns for the maps
col1, col2 , col3 = st.columns(3)

# Sidebar controls
with st.sidebar:
    # grid_size = st.slider("Grid Size (degrees)", 0.01, 0.1, 0.01, 0.01)
    grid_size = st.slider("Grid Size (degrees)", 0.001, 0.01, 0.001, 0.001)
    opacity = st.slider("Grid Opacity", 0.1, 1.0, 0.5, 0.1)
    
    if st.button("Clear Grid"):
        st.session_state.grid_squares_1 = []
        st.session_state.grid_squares_2 = []
        st.session_state.last_polygon = None


def generate_grid(polygon, grid_size):
    minx, miny, maxx, maxy = polygon.bounds
    x_coords = np.arange(minx, maxx, grid_size)
    y_coords = np.arange(miny, maxy, grid_size)
    
    ndvi_values = []
    smi_values = []
    
    # First pass to collect all NDVI values to determine range
    for x in x_coords:
        for y in y_coords:
            centre_x = x + (grid_size/2)
            centre_y = y + (grid_size/2)
            # centre_x = round(centre_x,4)
            # centre_y = round(centre_y,4)
            print("hello")
            ndvi = get_ndvi(centre_y, centre_x)
            ndvi_values.append(ndvi)

            smi = get_soil_moisture(centre_y,centre_x)
            smi_values.append(smi)

            # ndvi_dict = {(centre_y, centre_x):ndvi}
    
    # Determine NDVI range
    # print(ndvi_dict)
    # print()
    
    # Determine NDVI range
    min_ndvi = min(ndvi_values)
    max_ndvi = max(ndvi_values)

    max_smi = max(smi_values)
    min_smi = min(smi_values)

    # print("max ndvi: ",max_ndvi, " min_ndvi: ",min_ndvi)
    # print("max smi: ",max_smi, " min_ndvi: ",min_smi)
    
    
    grid_squares_nvdi = []
    grid_squares_smi = []
    
    # Second pass to generate grid squares and assign color based on NDVI
    # i = 0
    for x in x_coords:
        for y in y_coords:
            square = geom.box(x, y, x + grid_size, y + grid_size)

            centre_x = x + (grid_size/2)
            centre_y = y + (grid_size/2)

            # centre_x = round(centre_x,4)
            # centre_y = round(centre_y,4)

            # keys_list = list(ndvi_dict.keys())
            # if(i == keys_list.size)
            # (centre_y, centre_x) = keys_list[i]
            # i = i + 1
            
            if polygon.intersects(square):
                # ndvi = ndvi_dict.get((centre_y, centre_x))
                ndvi = get_ndvi(centre_y, centre_x)
                smi = get_soil_moisture(centre_y,centre_x)
                
                print("centre_y test: ",centre_y)
                print("centre_x test: ",centre_x)
                print("ndvi test: ",ndvi)
                print("ndvi test: ",smi)
                color_ndvi = value_to_green_hex(ndvi, min_ndvi, max_ndvi)
                color_smi = value_to_blue_hex(smi, min_smi, max_smi)
                # print("color nvdi: ", color_ndvi)
                # print("color smi: ", color_smi)
                # print()
                print("latitude: ",centre_y," longitude: ",centre_x)
                print("ndvi: ",ndvi)
                print("ndvi: ",smi)
                print()
                grid_squares_nvdi.append((list(square.exterior.coords), color_ndvi))
                grid_squares_smi.append((list(square.exterior.coords), color_smi))

                grid_square = []
                grid_square.append(grid_squares_nvdi)
                grid_square.append(grid_squares_smi)
    
    return grid_square

# Drawing map
with col1:
    st.subheader("Draw Polygon")
    m_draw = leafmap.Map(center=[31.14, 75.34], zoom=15)
    # m_draw = leafmap.Map(center=[26.91, 70.9], zoom=15)
    m_draw.add_basemap("HYBRID")
    Draw(export=True).add_to(m_draw)
    draw_output = st_folium(m_draw, height=400, width=None, key="draw_map")

# Result map
with col2:
    st.subheader("Generated Grid")
    m_result = leafmap.Map(center=[31.14, 75.34], zoom=15)
    # m_result = leafmap.Map(center=[26.91, 70.9], zoom=15)
    m_result.add_basemap("HYBRID")


    # Process the drawn polygon
    if (draw_output 
        and draw_output.get("last_active_drawing") 
        and draw_output["last_active_drawing"].get("geometry")):
        
        geometry = draw_output["last_active_drawing"]["geometry"]
        
        if geometry["type"] == "Polygon":
            coords = geometry["coordinates"][0]
            
            # Only update if the polygon has changed
            if str(coords) != str(st.session_state.last_polygon):
                st.session_state.last_polygon = coords
                current_polygon = geom.Polygon(coords)
                st.session_state.grid_squares_1 = (generate_grid(current_polygon, grid_size))[0] # ndvi grid squares

    # Always add stored grid squares to the result map
    for coords, color in st.session_state.grid_squares_1:
        print("color ndvi: ", color)

        folium.Polygon(
            locations=[(lat, lon) for lon, lat in coords],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=opacity,
        ).add_to(m_result)

    st_folium(m_result, height=400, width=None, key="result_map")

with col3:
    st.subheader("Generated Grid")
    m_result1 = leafmap.Map(center=[31.14, 75.34], zoom=15)
    # m_result = leafmap.Map(center=[26.91, 70.9], zoom=15)

    m_result1.add_basemap("HYBRID")

    smi_grid = []

    # Process the drawn polygon
    if (draw_output 
        and draw_output.get("last_active_drawing") 
        and draw_output["last_active_drawing"].get("geometry")):
        
        geometry = draw_output["last_active_drawing"]["geometry"]
        
        if geometry["type"] == "Polygon":
            coords = geometry["coordinates"][0]
            
            # Only update if the polygon has changed
            # if str(coords) != str(st.session_state.last_polygon):
            st.session_state.last_polygon = coords
            current_polygon = geom.Polygon(coords)
            print("hello 2")
            st.session_state.grid_squares_2 = (generate_grid(current_polygon, grid_size))[1] # smi grid squares
            # smi_grid = (generate_grid(current_polygon, grid_size))[1] # smi grid squares


    # print("hello 3")

    # Always add stored grid squares to the result map
    # if len(smi_grid) > 0:
    for coords, color in st.session_state.grid_squares_2:
        print("color smi: ", color)
        folium.Polygon(
            locations=[(lat, lon) for lon, lat in coords],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=opacity,
        ).add_to(m_result1)

    st_folium(m_result1, height=400, width=None, key="result_map1")


# Show stats
if st.session_state.grid_squares_1 :
    print("DONE")
    # st.metric("Grid Squares Generated", len(st.session_state.grid_squares))
    show_legend()

else:
    print("NOT DONE")

