# hardware_bridge.py
# Real-time sensor integration at 127.0.0.1
# Feeds 1650 inputs → coherence_engine

import socket
import threading
import json
import time
import numpy as np
from collections import deque
from flask import Flask, request, jsonify

app = Flask(__name__)

# Constants
SENSOR_HOST = '127.0.0.1'
SENSOR_PORT = 5001
INPUT_BUFFER_SIZE = 1650
UPDATE_FREQUENCY = 10  # Hz

class HardwareBridge:
    def __init__(self):
        self.input_buffer = deque(maxlen=INPUT_BUFFER_SIZE)
        self.running = False
        self.socket = None
        self.hrv_score = 0.5
        self.eeg_score = 0.5
        
    def start_sensor_listener(self):
        """Listen for real-time sensor data on 127.0.0.1:5001"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SENSOR_HOST, SENSOR_PORT))
        self.socket.settimeout(0.1)
        self.running = True
        
        while self.running:
            try:
                data, addr = self.socket.recvfrom(4096)
                payload = json.loads(data.decode())
                
                # Extract sensor values
                if 'sensors' in payload:
                    for val in payload['sensors']:
                        self.input_buffer.append(float(val))
                
                # Extract bio metrics
                if 'hrv' in payload:
                    self.hrv_score = payload['hrv']
                if 'eeg' in payload:
                    self.eeg_score = payload['eeg']
                    
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Sensor error: {e}")
    
    def get_inputs_1650(self):
        """Return 1650 inputs (pad with zeros if needed)"""
        current = list(self.input_buffer)
        if len(current) < INPUT_BUFFER_SIZE:
            current.extend([0.0] * (INPUT_BUFFER_SIZE - len(current)))
        return current[:INPUT_BUFFER_SIZE]
    
    def get_bio_scores(self):
        """Return current HRV and EEG scores"""
        return self.hrv_score, self.eeg_score
    
    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

# Global bridge instance
bridge = HardwareBridge()

# Start listener thread
threading.Thread(target=bridge.start_sensor_listener, daemon=True).start()

# Flask endpoints
@app.route('/sensors/status', methods=['GET'])
def sensor_status():
    return jsonify({
        'status': 'listening' if bridge.running else 'stopped',
        'buffer_size': len(bridge.input_buffer),
        'host': SENSOR_HOST,
        'port': SENSOR_PORT
    })

@app.route('/sensors/inputs', methods=['GET'])
def get_inputs():
    inputs = bridge.get_inputs_1650()
    return jsonify({'inputs': inputs, 'count': len(inputs)})

@app.route('/sensors/bio', methods=['GET'])
def get_bio():
    hrv, eeg = bridge.get_bio_scores()
    return jsonify({'hrv': hrv, 'eeg': eeg})

@app.route('/process', methods=['POST'])
def process():
    """Process current sensor data through coherence engine"""
    from coherence_engine import engine
    
    inputs = bridge.get_inputs_1650()
    hrv, eeg = bridge.get_bio_scores()
    
    result = engine.full_pipeline(inputs, hrv, eeg)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)