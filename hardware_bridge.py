# hardware_bridge.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models'))

from models.arc_table import arc_table
from models.coherence_engine import CoherenceEngine
from models.bucket_system import BucketSystem
from models.payload_builder import PayloadBuilder

app = Flask(__name__)
CORS(app)

coherence_engine = CoherenceEngine()
bucket_system = BucketSystem()
payload_builder = PayloadBuilder()

last_harmony = 50.0
last_payload = None
session_id = None
current_arc = 49
arc_direction = 1
last_arc_change_time = time.time()
ARC_CHANGE_INTERVAL = 30

DEFAULT_INPUTS = {
    'L0_hrv': 65, 'L0_heart_rate': 72, 'L0_sleep_stage': 3,
    'L0_nervous_system': 0.7, 'L0_recovery_index': 0.8, 'L0_eeg_coherence': 0.6,
    'L1_breath_rate': 12, 'L1_breath_depth': 0.7, 'L1_co2_tolerance': 45,
    'L1_rhythm_consistency': 0.8, 'L1_control_duration': 120
}


@app.route('/state', methods=['GET', 'POST'])
def get_state():
    global last_harmony, last_payload, current_arc, arc_direction, last_arc_change_time, session_id

    if request.method == 'POST':
        inputs = request.json if request.json else DEFAULT_INPUTS.copy()
    else:
        inputs = DEFAULT_INPUTS.copy()

    for key, default in DEFAULT_INPUTS.items():
        if key not in inputs:
            inputs[key] = default

    scores = coherence_engine.calculate_scores(inputs)
    buckets = bucket_system.resolve_buckets(scores)
    current_harmony = bucket_system.calculate_harmony(buckets)
    delta_harmony = bucket_system.calculate_delta_harmony(current_harmony, last_harmony)
    spread = bucket_system.calculate_spread(buckets)
    lowest_bucket = bucket_system.find_lowest_bucket(buckets)
    state = bucket_system.determine_state(current_harmony, delta_harmony)

    now = time.time()
    if now - last_arc_change_time >= ARC_CHANGE_INTERVAL:
        current_arc += arc_direction
        if current_arc >= 88:
            current_arc = 88
            arc_direction = -1
        elif current_arc <= 1:
            current_arc = 1
            arc_direction = 1
        last_arc_change_time = now

    payload = payload_builder.build_payload(
        arc_index=current_arc, state=state, harmony=current_harmony,
        delta_harmony=delta_harmony, spread=spread, lowest_bucket=lowest_bucket,
        buckets=buckets, previous_payload=last_payload
    )

    if coherence_engine.check_bio_override(inputs):
        payload = coherence_engine.apply_bio_override(payload)

    if not session_id:
        session_id = f"S_{int(time.time())}"
    payload['session_id'] = session_id
    payload['timestamp'] = datetime.now().isoformat()
    payload['bucket_scores'] = {k: v['score'] for k, v in buckets.items()}

    last_harmony = current_harmony
    last_payload = payload

    return jsonify(payload), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online', 'version': 'ENGINE88_v1.0',
        'timestamp': datetime.now().isoformat(),
        'current_arc': current_arc,
        'frequency_hz': arc_table.get_frequency(current_arc)
    }), 200


@app.route('/arcs', methods=['GET'])
def get_arcs():
    arcs = [{'arc': i, 'note': arc_table.get_note(i),
             'frequency_hz': arc_table.get_frequency(i),
             'mirror_arc': arc_table.get_mirror_arc(i)} for i in range(1, 89)]
    return jsonify({'arcs': arcs, 'total': 88}), 200


@app.route('/arc/<int:arc_id>', methods=['GET', 'POST'])
def set_arc(arc_id):
    global current_arc
    if 1 <= arc_id <= 88:
        current_arc = arc_id
        return jsonify({'status': 'ok', 'message': f'Arc set to {arc_id}',
                        'arc': current_arc, 'frequency_hz': arc_table.get_frequency(current_arc),
                        'note': arc_table.get_note(current_arc)}), 200
    return jsonify({'error': 'Arc must be between 1 and 88'}), 400


@app.route('/input', methods=['POST'])
def receive_input():
    if not request.json:
        return jsonify({'error': 'No input data provided'}), 400
    return get_state()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8890, debug=False)
