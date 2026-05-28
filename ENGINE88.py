from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from models.arc_table import arc_table
from models.coherence_engine import CoherenceEngine
from models.bucket_system import BucketSystem
from models.payload_builder import PayloadBuilder

app = Flask(__name__)
CORS(app)

current_arc = 42
coherence_engine = CoherenceEngine()
bucket_system = BucketSystem()
payload_builder = PayloadBuilder()
last_harmony = None
last_payload = None

@app.route('/state', methods=['GET', 'POST'])
def get_state():
    global last_harmony, last_payload, current_arc
    
    if request.method == 'POST' and request.json:
        inputs = request.json
    else:
        inputs = {}
    
    hrv = inputs.get('hrv', 65)
    eeg = inputs.get('eeg_coherence', 0.7)
    breath_rate = inputs.get('breath_rate', 12)
    breath_depth = inputs.get('breath_depth', 0.7)
    co2_tolerance = inputs.get('co2_tolerance', 30)
    rhythm = inputs.get('rhythm_consistency', 0.8)
    control = inputs.get('control_duration', 150)
    
    bio_override = coherence_engine.check_bio_override({'L0_hrv': hrv, 'L0_eeg_coherence': eeg})
    
    if bio_override:
        harmony = 15
    else:
        harmony = (hrv / 100 * 30) + (eeg * 30) + ((12 - abs(breath_rate - 12)) / 12 * 20) + (breath_depth * 10) + (rhythm * 10)
        harmony = min(100, max(0, harmony))
    
    delta_harmony = bucket_system.calculate_delta_harmony(harmony, last_harmony)
    spread = 0
    lowest_bucket = 'BODY'
    state = bucket_system.determine_state(harmony, delta_harmony)
    
    if bio_override:
        state = 'RECOVERY'
    
    payload = payload_builder.build_payload(
        harmony=harmony, state=state, spread=spread,
        lowest_bucket=lowest_bucket, current_arc=current_arc,
        bio_override=bio_override, previous_payload=last_payload
    )
    
    last_harmony = harmony
    last_payload = payload
    
    return jsonify(payload), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'version': 'ENGINE88_v1.0',
        'timestamp': datetime.now().isoformat(),
        'current_arc': current_arc,
        'frequency_hz': arc_table.get_frequency(current_arc),
        'note': arc_table.get_note(current_arc)
    }), 200

@app.route('/arc/<int:arc_id>', methods=['GET', 'POST'])
def set_arc(arc_id):
    global current_arc
    if 1 <= arc_id <= 88:
        current_arc = arc_id
        return jsonify({
            'status': 'ok',
            'message': f'Arc set to {arc_id}',
            'arc': current_arc,
            'frequency_hz': arc_table.get_frequency(current_arc),
            'note': arc_table.get_note(current_arc)
        }), 200
    return jsonify({'error': 'Arc must be between 1 and 88'}), 400

@app.route('/arcs', methods=['GET'])
def get_arcs():
    arcs = [{'arc': i, 'note': arc_table.get_note(i),
             'frequency_hz': arc_table.get_frequency(i),
             'mirror_arc': arc_table.get_mirror_arc(i)} for i in range(1, 89)]
    return jsonify({'arcs': arcs, 'total': 88}), 200

@app.route('/input', methods=['POST'])
def receive_input():
    if not request.json:
        return jsonify({'error': 'No input data provided'}), 400
    return get_state()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 ENGINE88 RUNNING")
    print("="*50)
    print("📍 http://127.0.0.1:8000")
    print("📊 http://127.0.0.1:8000/health")
    print("="*50 + "\n")
    app.run(host='127.0.0.1', port=8000, debug=False)
