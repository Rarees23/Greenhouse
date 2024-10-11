from datetime import datetime
import serial
import time
import threading

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
            
            # Display the latest reading and previous readings on the terminal
            print(f"Current Time: {current_time}, Data: {data}")
            print("Previous Readings:")
            for reading in previous:
                print(f"Time: {reading['time']}, Data: {reading['data']}")
            print("-" * 50)
        
        time.sleep(1)  # Wait for a second before the next read

# Start the continuous reading thread
threading.Thread(target=continuous_reading, daemon=True).start()

# Keep the program running
while True:
    time.sleep(1)
