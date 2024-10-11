from flask import Flask, render_template
from datetime import datetime
import serial
import time
import threading

app = Flask(__name__)

# Initialize serial connection (update the COM port as necessary)
ser = serial.Serial('COM3', 9600)
time.sleep(2)

previous = []  # List to store previous readings

# Function to get the current time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to read data from the Arduino
def get_data():
    try:
        data = ser.readline().decode('utf-8').strip()
        return data
    except Exception as e:
        print(f"Error reading from serial: {e}")
        return None

# Background thread for continuously reading data
def continuous_reading():
    while True:
        data = get_data()
        if data:
            current_time = get_current_time()
            previous.append({'time': current_time, 'data': data})
            if len(previous) > 10:  # Limit to 10 previous readings
                previous.pop(0)

# Start the continuous reading thread
threading.Thread(target=continuous_reading, daemon=True).start()

# Route to render the HTML template
@app.route('/')
def index():
    latest_data = previous[-1]['data'] if previous else "No Data"
    return render_template('index.html', latest_data=latest_data, previous=previous)
app.run(port=8080)
#if __name__ == '__main__':
    #app.run(debug=True)
