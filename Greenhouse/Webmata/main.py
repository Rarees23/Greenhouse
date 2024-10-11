import requests
import json

input_file = "data.json"  # Path to the JSON file
url = "http://127.0.0.1:8080/api/data"  # URL for the POST request (updated to match the Flask app)

# Open the JSON file
with open(input_file, 'r') as file:
    # Load data from JSON file
    sensor_data = json.load(file)

# Process each item in the JSON data
if isinstance(sensor_data, dict) and 'sensors' in sensor_data:
    for item in sensor_data['sensors']:
        try:
            # Make the POST request with the data item
            response = requests.post(url, json=item)

            # Check if the response status code indicates an error
            if response.status_code == 200:
                print(f"Successfully posted data: {item}")
            else:
                print(f"Failed to post data: {response.status_code}, {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
else:
    print("Error: JSON file does not contain valid sensor data.")
