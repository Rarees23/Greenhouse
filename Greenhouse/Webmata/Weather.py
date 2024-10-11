from flask import Flask, render_template, jsonify, request  # Import jsonify and request
from datetime import datetime
import serial
import time
import threading
import json  # Ensure the json module is imported

app = Flask(__name__)

# Initialize serial connection (update the COM port as necessary)
try:
    ser = serial.Serial('COM3', 9600)  # Change COM port as needed
    time.sleep(2)  # Wait for the connection to be established
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    ser = None

previous = []  # List to store previous readings

# Function to get the current time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to read data from the Arduino
def get_data():
    if ser is not None:
        try:
            data = ser.readline().decode('utf-8').strip()
            return data
        except Exception as e:
            print(f"Error reading from serial: {e}")
            return None
    return None

# Background thread for continuously reading data
def continuous_reading():
    while True:
        data = get_data()
        if data:
            current_time = get_current_time()
            try:
                # Assuming data format is: {"sensor_id": "1", "timestamp": "12:34:56", "temperature": "23", "humidity": "45", "light_level": "512"}
                json_data = json.loads(data)  # Parse JSON data
                previous.append({'time': current_time, **json_data})  # Combine timestamp with the data
                if len(previous) > 10:  # Limit to 10 previous readings
                    previous.pop(0)
            except json.JSONDecodeError:
                print("Error decoding JSON data")

# Start the continuous reading thread
threading.Thread(target=continuous_reading, daemon=True).start()

# Function to calculate statistics for the readings
def calculate_statistics(sensor_type):
    values = [float(entry[sensor_type]) for entry in previous if sensor_type in entry]
    if values:
        avg = sum(values) / len(values)
        max_value = max(values)
        min_value = min(values)
        return avg, max_value, min_value
    return None, None, None

# Route to render the HTML template
@app.route('/')
def index():
    latest_data = previous[-1] if previous else {"time": get_current_time(), "temperature": "No Data", "humidity": "No Data", "light_level": "No Data"}
    
    # Calculate statistics
    avg_temp, max_temp, min_temp = calculate_statistics("temperature")
    avg_humidity, max_humidity, min_humidity = calculate_statistics("humidity")
    avg_light, max_light, min_light = calculate_statistics("light_level")
    return render_template('index.html',latest_data=latest_data,previous=previous,avg_temp=avg_temp, max_temp=max_temp, min_temp=min_temp,avg_humidity=avg_humidity, max_humidity=max_humidity, min_humidity=min_humidity,avg_light=avg_light, max_light=max_light, min_light=min_light)

# API endpoint to receive sensor data
@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    if data:
        current_time = get_current_time()
        previous.append({'time': current_time, **data})  # Combine timestamp with data
        if len(previous) > 10:  # Limit to 10 previous readings
            previous.pop(0)


app.run(port=8080)
