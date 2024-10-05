import requests

# URL of the PNG file
url = 'https://docs.mapbox.com/help/datasheets/earthquakes-heatmap.png'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Open a file in binary write mode and save the content
    with open('earthquakes-heatmap.png', 'wb') as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to retrieve the image. Status code: {response.status_code}")