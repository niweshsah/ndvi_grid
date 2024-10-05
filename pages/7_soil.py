# import streamlit as st
# import leafmap.foliumap as leafmap

# st.set_page_config(layout="wide")

# markdown = """
# A Streamlit map template
# <https://github.com/opengeos/streamlit-map-template>
# """

# st.sidebar.title("About")
# st.sidebar.info(markdown)
# logo = "https://i.imgur.com/UbOXYAU.png"
# st.sidebar.image(logo)

# st.title("Marker Cluster")

# with st.expander("See source code"):
#     with st.echo():

#         m = leafmap.Map(center=[40, -100], zoom=4)
#         cities = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
#         regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

#         m.add_geojson(regions, layer_name="US Regions")
#         m.add_points_from_xy(
#             cities,
#             x="longitude",
#             y="latitude",
#             color_column="region",
#             icon_names=["gear", "map", "leaf", "globe"],
#             spin=True,
#             add_legend=True,
#         )

# m.to_streamlit(height=700)


# 2nd code

# import streamlit as st
# import leafmap.foliumap as leafmap
# import folium

# # Set the title of the Streamlit app
# st.title("Leafmap with Bounding Box")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)

# # Define coordinates for the bounding box
# bounding_box = [[35, -110], [45, -90]]  # Southwest and Northeast corners

# # Create a bounding box (rectangle) with a specific color and add it to the map
# rectangle = folium.Rectangle(
#     bounds=bounding_box,
#     color="blue",  # Color of the rectangle
#     fill=True,     # Fill the rectangle
#     fill_color="blue",  # Fill color of the rectangle
#     fill_opacity=0.2  # Opacity of the fill
# )
# rectangle.add_to(m)

# # Display the map in Streamlit
# m.to_streamlit(height=700)













# 3rd code


# import streamlit as st
# import leafmap.foliumap as leafmap
# from folium.plugins import Draw

# # Set the title of the Streamlit app
# st.title("Draw a Polygon on the Map")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)



# Draw(export=True).add_to(m)

# # m.add_child(draw)

# # Display the map in Streamlit
# output = m.to_streamlit(height=700)

# # Handle the GeoJSON output if the user has drawn a polygon

# # if output and 'all_drawings' in output:
# #     st.write("Drawn Polygon:")
# #     st.json(output['all_drawings'])









# 4TH CODE

# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw

# # Set the title of the Streamlit app
# st.title("Draw a Polygon and Store Coordinates")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)


# Draw(export=True).add_to(m)


# # Display the map in Streamlit and capture user interactions
# output = st_folium(m, height=700, width=700)

# # Check if there is a drawn polygon
# if output and output["last_active_drawing"] is not None:
#     # Extract coordinates from the drawn polygon
#     geometry = output["last_active_drawing"]["geometry"]
#     if geometry["type"] == "Polygon":
#         coordinates_list = geometry["coordinates"][0]  # First element for the outer boundary
        
#         # Display the list of coordinates
#         st.write("Polygon Coordinates (Longitude, Latitude):")
#         st.write(coordinates_list)
#     else: 
#         st.write("NOT WORKING")

# else:
#     st.write("Draw a polygon to see its coordinates.")

















# 5th code


# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# from shapely.geometry import Polygon, Point
# import numpy as np

# # Function to generate a grid of squares within the polygon bounds
# def generate_grid(polygon_coords, rows=10, cols=10):
#     # Convert polygon coordinates into a shapely Polygon
#     polygon = Polygon(polygon_coords)

#     # Get the bounds of the polygon
#     min_lon, min_lat, max_lon, max_lat = polygon.bounds

#     # Generate grid points
#     lat_step = (max_lat - min_lat) / rows
#     lon_step = (max_lon - min_lon) / cols

#     grid = []
#     for i in range(rows):
#         for j in range(cols):
#             # Get the bottom-left and top-right of the current square
#             lat_start = min_lat + i * lat_step
#             lat_end = lat_start + lat_step
#             lon_start = min_lon + j * lon_step
#             lon_end = lon_start + lon_step

#             # Create the square as a list of coordinates
#             square_coords = [(lon_start, lat_start), (lon_end, lat_start), 
#                              (lon_end, lat_end), (lon_start, lat_end), 
#                              (lon_start, lat_start)]
            
#             # Convert to a Polygon and check if it's within the drawn polygon
#             square = Polygon(square_coords)
#             if polygon.intersects(square):
#                 # Add the square if it's inside the polygon
#                 grid.append(square_coords)
    
#     return grid

# # Set the title of the Streamlit app
# st.title("Draw a Polygon and View Heatmap Grid")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)

# # Add drawing functionality to the map
# Draw(export=True).add_to(m)

# # Display the map in Streamlit and capture user interactions
# output = st_folium(m, height=700, width=700)

# # Check if there is a drawn polygon
# if output and output.get("last_active_drawing") is not None:
#     geometry = output["last_active_drawing"]["geometry"]
#     if geometry["type"] == "Polygon":
#         # Extract coordinates from the drawn polygon
#         coordinates_list = geometry["coordinates"][0]  # First element for the outer boundary
        
#         # Generate the grid within the drawn polygon
#         grid_squares = generate_grid(coordinates_list, rows=10, cols=10)

#         # Add each grid square to the same map with a random color
#         for square in grid_squares:
#             color = "#{:02x}{:02x}{:02x}".format(np.random.randint(0, 255),
#                                                  np.random.randint(0, 255),
#                                                  100)  # Random color
#             folium.Polygon(locations=square, color=color, fill=True, fill_color=color, fill_opacity=0.6).add_to(m)
        
#         # Update the map with the heatmap grid
#         st_folium(m, width=700, height=500)
#     else:
#         st.write("Please draw a polygon.")
# else:
#     st.write("Draw a polygon to create a heatmap grid.")









# 6th code


# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# import numpy as np

# # Set the title of the Streamlit app
# st.title("Add a Raster Layer to the Map")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)

# # Add drawing functionality to the map
# Draw(export=True).add_to(m)

# # Add a raster layer (example image URL for demonstration)
# raster_url = 'https://docs.mapbox.com/help/data/earthquakes-heatmap.png'  # Example URL of a raster
# bounds = [[30, -130], [50, -70]]  # Bounds of the raster (SouthWest, NorthEast)

# # Add raster image overlay to the map
# folium.raster_layers.ImageOverlay(
#     name="Heatmap Raster",
#     image=raster_url,
#     bounds=bounds,
#     opacity=0.6,  # Set transparency
# ).add_to(m)

# # Display the map with the raster layer in Streamlit
# st_folium(m, height=700, width=700)













# 7TH CODE

# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw, HeatMap
# import folium
# import random
# import shapely.geometry as geom

# # Set the title of the Streamlit app
# st.title("Draw a Polygon and Heatmap Inside")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)

# # Add drawing functionality
# Draw(export=True).add_to(m)

# # Display the map and capture interactions
# output = st_folium(m, height=700, width=700)

# # Check if there is a drawn polygon
# if output and output["last_active_drawing"] is not None:
#     # Extract coordinates from the drawn polygon
#     geometry = output["last_active_drawing"]["geometry"]
    
#     if geometry["type"] == "Polygon":
#         coordinates_list = geometry["coordinates"][0]  # First element for the outer boundary
#         st.write("Polygon Coordinates (Longitude, Latitude):")
#         st.write(coordinates_list)

#         # Convert coordinates to a shapely Polygon
#         polygon = geom.Polygon(coordinates_list)
        
#         # Generate random heatmap points inside the polygon
#         heatmap_data = []
#         for _ in range(100):  # Generate 100 random points
#             lon = random.uniform(min(p[0] for p in coordinates_list), max(p[0] for p in coordinates_list))
#             lat = random.uniform(min(p[1] for p in coordinates_list), max(p[1] for p in coordinates_list))
#             point = geom.Point(lon, lat)
            
#             # Only include points that are inside the polygon
#             if polygon.contains(point):
#                 heatmap_data.append([lat, lon])  # Note that Folium HeatMap expects [lat, lon]


#         print("heatmap_data")
#         # Add HeatMap layer only if we have valid heatmap data
#         if heatmap_data:
#             HeatMap(heatmap_data, radius=15, blur=10, max_zoom=1).add_to(m)
#         else:
#             st.write("No points generated inside the polygon for the heatmap.")
#     else:
#         st.write("Draw a valid polygon.")
# else:
#     st.write("Draw a polygon to see its coordinates and heatmap inside.")
    
# print("DONE")

# # Display the map with the heatmap inside the polygon
# st_folium(m, height=700, width=700)












# 8TH CODE


# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# import shapely.geometry as geom
# import numpy as np
# import random

# # Set the title of the Streamlit app
# st.title("Draw a Polygon and Colorful Grid Inside")

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)

# # Add drawing functionality
# Draw(export=True).add_to(m)

# # Display the map and capture interactions
# output = st_folium(m, height=700, width=700)

# # Function to generate grid squares inside the polygon
# def generate_colored_grid(polygon, x_spacing, y_spacing):
#     # Get the bounds of the polygon (min_x, min_y, max_x, max_y)
#     min_x, min_y, max_x, max_y = polygon.bounds

#     # Generate grid points based on the spacing
#     x_coords = np.arange(min_x, max_x, x_spacing)
#     y_coords = np.arange(min_y, max_y, y_spacing)
    
#     grid_squares = []

#     # Create squares (rectangles) for each combination of x and y coordinates
#     for x in x_coords:
#         for y in y_coords:
#             # Define the corner points of the square (rectangle)
#             bottom_left = geom.Point(x, y)
#             top_right = geom.Point(x + x_spacing, y + y_spacing)
            
#             # Create the square (a polygon representing the grid cell)
#             square = geom.box(minx=x, miny=y, maxx=x + x_spacing, maxy=y + y_spacing)
            
#             # Only include squares that are inside the drawn polygon
#             if polygon.intersects(square):
#                 # Assign a random color
#                 color = "#%06x" % random.randint(0, 0xFFFFFF)
#                 grid_squares.append((square, color))

#     return grid_squares

# # Check if there is a drawn polygon
# if output and output["last_active_drawing"] is not None:
#     # Extract coordinates from the drawn polygon
#     geometry = output["last_active_drawing"]["geometry"]
    
#     if geometry["type"] == "Polygon":
#         coordinates_list = geometry["coordinates"][0]  # First element for the outer boundary
#         # st.write("Polygon Coordinates (Longitude, Latitude):")
#         # st.write(coordinates_list)

#         # Convert coordinates to a shapely Polygon
#         polygon = geom.Polygon(coordinates_list)
        
#         # Define the grid spacing (e.g., 0.1 degrees)
#         x_spacing = 0.01
#         y_spacing = 0.01

#         # Generate grid squares inside the polygon with colors
#         grid_squares = generate_colored_grid(polygon, x_spacing, y_spacing)

#         # Check if we have valid grid squares
#         if grid_squares:
#             for square, color in grid_squares:
#                 # Extract the coordinates of the square (rectangle)
#                 coords = list(square.exterior.coords)
                
#                 # Add each grid square to the map as a Polygon with a random color
#                 folium.Polygon(
#                     locations=[(lat, lon) for lon, lat in coords],  # Lat, Lon for folium
#                     color=color,
#                     fill=True,
#                     fill_color=color,
#                     fill_opacity=0.7,
#                 ).add_to(m)
#         else:
#             st.write("No grid squares generated inside the polygon.")
#     else:
#         st.write("Draw a valid polygon.")
# else:
#     st.write("Draw a polygon to see the colored grid inside.")
    
# # Display the map with the grid squares inside the polygon
# st_folium(m, height=700, width=700)





























# 9th code












# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# import shapely.geometry as geom
# import numpy as np
# import random

# # Set the title of the Streamlit app
# st.title("Draw a Polygon and Colorful Grid Inside")

# # Check if a polygon is already drawn
# if "polygon_drawn" not in st.session_state:
#     st.session_state.polygon_drawn = False

# # Create a Leafmap map centered on a specific location
# m = leafmap.Map(center=[40, -100], zoom=4)

# # Add drawing functionality
# Draw(export=True).add_to(m)

# # Display the map and capture interactions
# output = st_folium(m, height=700, width=700, key="map1")

# # Function to generate grid squares inside the polygon
# def generate_colored_grid(polygon, x_spacing, y_spacing):
#     # Get the bounds of the polygon (min_x, min_y, max_x, max_y)
#     min_x, min_y, max_x, max_y = polygon.bounds

#     # Generate grid points based on the spacing
#     x_coords = np.arange(min_x, max_x, x_spacing)
#     y_coords = np.arange(min_y, max_y, y_spacing)
    
#     grid_squares = []

#     # Create squares (rectangles) for each combination of x and y coordinates
#     for x in x_coords:
#         for y in y_coords:
#             # Create the square (a polygon representing the grid cell)
#             square = geom.box(minx=x, miny=y, maxx=x + x_spacing, maxy=y + y_spacing)
            
#             # Only include squares that are inside the drawn polygon
#             if polygon.intersects(square):
#                 # Assign a random color
#                 color = "#%06x" % random.randint(0, 0xFFFFFF)
                
#                 # Calculate the center of the square
#                 center = square.centroid
                
#                 grid_squares.append((square, color, (center.y, center.x)))  # Store the center coordinates

#     return grid_squares

# # Check if there is a drawn polygon
# if output and output["last_active_drawing"] is not None and not st.session_state.polygon_drawn:
#     # Extract coordinates from the drawn polygon
#     geometry = output["last_active_drawing"]["geometry"]
    
#     if geometry["type"] == "Polygon":
#         coordinates_list = geometry["coordinates"][0]  # First element for the outer boundary
#         st.write("Polygon Coordinates (Longitude, Latitude):")
#         st.write(coordinates_list)

#         # Convert coordinates to a shapely Polygon
#         polygon = geom.Polygon(coordinates_list)
        
#         # Define the grid spacing (e.g., 0.5 degrees)
#         x_spacing = 1
#         y_spacing = 1

#         # Generate grid squares inside the polygon with colors
#         grid_squares = generate_colored_grid(polygon, x_spacing, y_spacing)

#         # Check if we have valid grid squares
#         if grid_squares:
#             for square, color, center in grid_squares:
#                 # Extract the coordinates of the square (rectangle)
#                 coords = list(square.exterior.coords)
                
#                 # Add each grid square to the map as a Polygon with a random color
#                 folium.Polygon(
#                     locations=[(lat, lon) for lon, lat in coords],  # Lat, Lon for folium
#                     color=color,
#                     fill=True,
#                     fill_color=color,
#                     fill_opacity=0.7,
#                 ).add_to(m)

#                 # Display the center coordinates of the square
#                 st.write(f"Center of Square (Longitude, Latitude): {center}")

#             # Flag the polygon as drawn to avoid re-rendering
#             # st.session_state.polygon_drawn = True

# # Display the map with the grid squares inside the polygon only when a polygon is drawn
# st_folium(m, height=700, width=700, key="map2")































# 10th code





# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# import shapely.geometry as geom
# import numpy as np
# import random

# # Set up the Streamlit page
# st.title("Polygon Grid Generator")
# st.write("Draw a polygon on the map, and I'll fill it with colorful grid squares!")

# # Sidebar controls
# with st.sidebar:
#     grid_size = st.slider("Grid Size (degrees)", 0.1, 2.0, 0.5, 0.1)
#     opacity = st.slider("Grid Opacity", 0.1, 1.0, 0.7, 0.1)

# def generate_grid(polygon, grid_size):
#     # Get the bounds of the polygon
#     minx, miny, maxx, maxy = polygon.bounds
    
#     # Generate grid points
#     x_coords = np.arange(minx, maxx, grid_size)
#     y_coords = np.arange(miny, maxy, grid_size)
    
#     grid_squares = []
#     for x in x_coords:
#         for y in y_coords:
#             # Create a square
#             square = geom.box(x, y, x + grid_size, y + grid_size)
            
#             # Only keep squares that intersect with the polygon
#             if polygon.intersects(square):
#                 # Generate a random color
#                 color = f"#{random.randint(0, 0xFFFFFF):06x}"
#                 grid_squares.append((square, color))
    
#     return grid_squares

# # Create the map
# m = leafmap.Map(center=[40, -100], zoom=4)
# Draw(export=True).add_to(m)

# # Display the map and get the drawn features
# output = st_folium(m, height=500, width=700)

# # Process the drawn polygon
# if (output 
#     and output.get("last_active_drawing") 
#     and output["last_active_drawing"].get("geometry")):
    
#     geometry = output["last_active_drawing"]["geometry"]
    
#     if geometry["type"] == "Polygon":
#         # Convert the drawn polygon to a shapely polygon
#         coords = geometry["coordinates"][0]
#         polygon = geom.Polygon(coords)
        
#         # Generate grid squares
#         grid_squares = generate_grid(polygon, grid_size)
        
#         # Add grid squares to the map
#         for square, color in grid_squares:
#             coords = list(square.exterior.coords)
#             folium.Polygon(
#                 locations=[(lat, lon) for lon, lat in coords],
#                 color=color,
#                 fill=True,
#                 fill_color=color,
#                 fill_opacity=opacity,
#             ).add_to(m)
        
#         # Show some stats
#         st.write(f"Generated {len(grid_squares)} grid squares!")

# # Display the updated map
# st_folium(m, height=500, width=700)














# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# import shapely.geometry as geom
# import numpy as np
# import random

# # Initialize session state
# if 'grid_squares' not in st.session_state:
#     st.session_state.grid_squares = []
# if 'last_polygon' not in st.session_state:
#     st.session_state.last_polygon = None

# # Set up the Streamlit page
# st.title("Polygon Grid Generator")
# st.write("Draw a polygon on the left map, and see the result on the right!")

# # Create two columns for the maps
# col1, col2 = st.columns(2)

# # Sidebar controls
# with st.sidebar:
#     grid_size = st.slider("Grid Size (degrees)", 0.1, 2.0, 0.5, 0.1)
#     opacity = st.slider("Grid Opacity", 0.1, 1.0, 0.7, 0.1)
    
#     if st.button("Clear Grid"):
#         st.session_state.grid_squares = []
#         st.session_state.last_polygon = None

# def generate_grid(polygon, grid_size):
#     minx, miny, maxx, maxy = polygon.bounds
#     x_coords = np.arange(minx, maxx, grid_size)
#     y_coords = np.arange(miny, maxy, grid_size)
    
#     grid_squares = []
#     for x in x_coords:
#         for y in y_coords:
#             square = geom.box(x, y, x + grid_size, y + grid_size)
#             if polygon.intersects(square):
#                 color = f"#{random.randint(0, 0xFFFFFF):06x}"
#                 grid_squares.append((list(square.exterior.coords), color))
    
#     return grid_squares

# # Drawing map
# with col1:
#     st.subheader("Draw Polygon")
#     m_draw = leafmap.Map(center=[40, -100], zoom=4)
#     Draw(export=True).add_to(m_draw)
#     draw_output = st_folium(m_draw, height=400, width=None, key="draw_map")

# # Result map
# with col2:
#     st.subheader("Generated Grid")
#     m_result = leafmap.Map(center=[40, -100], zoom=4)

#     # Process the drawn polygon
#     if (draw_output 
#         and draw_output.get("last_active_drawing") 
#         and draw_output["last_active_drawing"].get("geometry")):
        
#         geometry = draw_output["last_active_drawing"]["geometry"]
        
#         if geometry["type"] == "Polygon":
#             coords = geometry["coordinates"][0]
            
#             # Only update if the polygon has changed
#             if str(coords) != str(st.session_state.last_polygon):
#                 st.session_state.last_polygon = coords
#                 current_polygon = geom.Polygon(coords)
#                 st.session_state.grid_squares = generate_grid(current_polygon, grid_size)

#     # Always add stored grid squares to the result map
#     for coords, color in st.session_state.grid_squares:
#         folium.Polygon(
#             locations=[(lat, lon) for lon, lat in coords],
#             color=color,
#             fill=True,
#             fill_color=color,
#             fill_opacity=opacity,
#         ).add_to(m_result)

#     st_folium(m_result, height=400, width=None, key="result_map")

# # Show stats
# if st.session_state.grid_squares:
#     st.metric("Grid Square




















# 11th code

# Polygon Grid Generator

# import streamlit as st
# import leafmap.foliumap as leafmap
# from streamlit_folium import st_folium
# from folium.plugins import Draw
# import folium
# import shapely.geometry as geom
# import numpy as np
# import random

# # Initialize session state
# if 'grid_generated' not in st.session_state:
#     st.session_state.grid_generated = False
# if 'last_polygon' not in st.session_state:
#     st.session_state.last_polygon = None

# # Set up the Streamlit page
# st.title("Polygon Grid Generator")
# st.write("Draw a polygon on the left map, and see the result on the right!")

# # Create two columns for the maps
# col1, col2 = st.columns(2)

# # Sidebar controls
# with st.sidebar:
#     grid_size = st.slider("Grid Size (degrees)", 0.1, 2.0, 0.5, 0.1)
#     opacity = st.slider("Grid Opacity", 0.1, 1.0, 0.7, 0.1)
    
#     if st.button("Generate Grid"):
#         st.session_state.grid_generated = True

# def generate_grid(polygon, grid_size):
#     minx, miny, maxx, maxy = polygon.bounds
#     x_coords = np.arange(minx, maxx, grid_size)
#     y_coords = np.arange(miny, maxy, grid_size)
    
#     grid_squares = []
#     for x in x_coords:
#         for y in y_coords:
#             square = geom.box(x, y, x + grid_size, y + grid_size)
#             if polygon.intersects(square):
#                 color = f"#{random.randint(0, 0xFFFFFF):06x}"
#                 grid_squares.append((square, color))
    
#     return grid_squares

# # Drawing map
# with col1:
#     st.subheader("Draw Polygon")
#     m_draw = leafmap.Map(center=[40, -100], zoom=4)
#     Draw(export=True).add_to(m_draw)
#     draw_output = st_folium(m_draw, height=400, width=None, key="draw_map")

# # Result map
# with col2:
#     st.subheader("Generated Grid")
#     m_result = leafmap.Map(center=[40, -100], zoom=4)

#     # Process the drawn polygon
#     if (draw_output 
#         and draw_output.get("last_active_drawing") 
#         and draw_output["last_active_drawing"].get("geometry")):
        
#         geometry = draw_output["last_active_drawing"]["geometry"]
        
#         if geometry["type"] == "Polygon":
#             coords = geometry["coordinates"][0]
#             current_polygon = geom.Polygon(coords)
            
#             # Only update if the polygon has changed or generate button is clicked
#             if (st.session_state.last_polygon != coords or 
#                 st.session_state.grid_generated):
                
#                 st.session_state.last_polygon = coords
#                 grid_squares = generate_grid(current_polygon, grid_size)
                
#                 # Add grid squares to the result map
#                 for square, color in grid_squares:
#                     coords = list(square.exterior.coords)
#                     folium.Polygon(
#                         locations=[(lat, lon) for lon, lat in coords],
#                         color=color,
#                         fill=True,
#                         fill_color=color,
#                         fill_opacity=opacity,
#                     ).add_to(m_result)
                
#                 # Show stats
#                 st.session_state.grid_generated = False
#                 st.metric("Grid Squares Generated", len(grid_squares))

#     result_map = st_folium(m_result, height=400, width=None, key="result_map")













# 13th code:



import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
from folium.plugins import Draw
import folium
import shapely.geometry as geom
import numpy as np
import random
import colorsys
import datetime
from sentinelhub import SHConfig, BBox, CRS, DataCollection, SentinelHubRequest, MimeType


def value_to_green_hex(ndvi_real, ndvi_max,ndvi_min):

    if ndvi_max != ndvi_min:
     value = (ndvi_real - ndvi_min)/(ndvi_max - ndvi_min)
     value = round(value,3)
    else:
     value = 1

    if not 0 <= value <= 1:
        print(value)
        raise ValueError("Input must be between 0 and 1")
    
    # Convert the value to an 8-bit integer (0-255)
    # green_component = int(value * 255)
    
    # Create the hex color code
    # Red and Blue components are always 255 (FF)
    # Green component varies based on input



    print("value: ",value)


    red_blue_component = int(255 * (1 - value))
    green_component = 255  # Green stays constant at 255
    
    # Create the hex color code
    hex_color = f"#{red_blue_component:02x}{green_component:02x}{red_blue_component:02x}"


    # if value > 0.7:
    #     # Green (#00FF00)
    #     return "#00FF00"
    # elif value > 0.3:
    #     # Purple (#800080)
    #     return "#800080"
    #     # Red (#FF0000)
    # return "#FF0000"
    
    return hex_color



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

# Initialize session state
if 'grid_squares' not in st.session_state:
    st.session_state.grid_squares = []
if 'last_polygon' not in st.session_state:
    st.session_state.last_polygon = None

# Set up the Streamlit page
st.title("Polygon Grid Generator")
st.write("Draw a polygon on the left map, and see the result on the right!")

# Create two columns for the maps
col1, col2 = st.columns(2)

# Sidebar controls
with st.sidebar:
    # grid_size = st.slider("Grid Size (degrees)", 0.01, 0.1, 0.01, 0.01)
    grid_size = st.slider("Grid Size (degrees)", 0.001, 0.01, 0.001, 0.001)
    opacity = st.slider("Grid Opacity", 0.1, 1.0, 0.5, 0.1)
    
    if st.button("Clear Grid"):
        st.session_state.grid_squares = []
        st.session_state.last_polygon = None


def generate_grid(polygon, grid_size):
    minx, miny, maxx, maxy = polygon.bounds
    x_coords = np.arange(minx, maxx, grid_size)
    y_coords = np.arange(miny, maxy, grid_size)
    
    ndvi_values = []
    
    # First pass to collect all NDVI values to determine range
    for x in x_coords:
        for y in y_coords:
            centre_x = x + (grid_size/2)
            centre_y = y + (grid_size/2)
            # centre_x = round(centre_x,4)
            # centre_y = round(centre_y,4)
            print("hello")
            ndvi = get_soil_moisture(centre_y, centre_x)
            ndvi_values.append(ndvi)

            ndvi_dict = {(centre_y, centre_x):ndvi}
    
    # Determine NDVI range
    # print(ndvi_dict)
    # print()
    
    # Determine NDVI range
    min_ndvi = min(ndvi_values)
    max_ndvi = max(ndvi_values)

    print("max ndvi: ",max_ndvi, " min_ndvi: ",min_ndvi)
    
    
    grid_squares = []
    
    # Second pass to generate grid squares and assign color based on NDVI
    i = 0
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
                ndvi = get_soil_moisture(centre_y, centre_x)
                
                print("centre_y test: ",centre_y)
                print("centre_x test: ",centre_x)
                print("ndvi test: ",ndvi)
                color = value_to_green_hex(ndvi, min_ndvi, max_ndvi)
                print("latitude: ",centre_y," longitude: ",centre_x)
                print("ndvi: ",ndvi)
                print()
                grid_squares.append((list(square.exterior.coords), color))
    
    return grid_squares

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
                st.session_state.grid_squares = generate_grid(current_polygon, grid_size)

    # Always add stored grid squares to the result map
    for coords, color in st.session_state.grid_squares:
        folium.Polygon(
            locations=[(lat, lon) for lon, lat in coords],
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=opacity,
        ).add_to(m_result)

    st_folium(m_result, height=400, width=None, key="result_map")

# Show stats
if st.session_state.grid_squares:
    print("DONE")
    st.metric("Grid Squares Generated", len(st.session_state.grid_squares))
