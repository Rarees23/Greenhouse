from flask import Flask, render_template
from datetime import datetime
import random
import time
import threading

app = Flask(__name__)

previous = []  # List to store previous readings

# Function to get the current time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to generate random data
def generate_random_data():
    return random.randint(0, 100)  # Generate random numbers between 0 and 100

# Background thread for continuously generating random data
def continuous_reading():
        current_time = get_current_time()
        data = generate_random_data()
        previous.append({'time': current_time, 'data': data})
        if len(previous) > 10:  # Limit to 10 previous readings
            previous.pop(0)
        time.sleep(1)  # Wait for a second before the next read

# Start the continuous reading thread
threading.Thread(target=continuous_reading, daemon=True).start()

# Route to render the HTML template
@app.route('/')
def index():
    latest_data = previous[-1]['data'] if previous else "No Data"
    return render_template('index.html', latest_data=latest_data, previous=previous)

if __name__ == '__main__':
    app.run(debug=True)
