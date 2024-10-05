
import datetime
from sentinelhub import SHConfig, BBox, CRS, DataCollection, SentinelHubRequest, MimeType

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

# Example usage:


try:
    ndvi = get_ndvi(31.1471, 75.3412)
    print(f"NDVI value: {ndvi}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
