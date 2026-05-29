# coherence_engine.py
# 110-Score Calculation System with Bio Override
# Inputs: 1650 → 110 scores → 22 buckets → harmony → arc (1-88)

import math
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Constants
PHI = 1.618033988749895
PI = 3.141592653589793
DETERMINISTIC_ROOT = 432

# 22 Bucket targets (based on 7 chakras + 15 sub-buckets)
BUCKET_TARGETS = {
    1: 432.00, 2: 441.00, 3: 450.00, 4: 459.00, 5: 468.00, 6: 477.00, 7: 486.00,
    8: 495.00, 9: 504.00, 10: 513.00, 11: 522.00, 12: 531.00, 13: 540.00, 14: 549.00,
    15: 558.00, 16: 567.00, 17: 576.00, 18: 585.00, 19: 594.00, 20: 603.00, 21: 612.00, 22: 621.00
}

# Bio override weights (70% HRV, 30% EEG)
BIO_WEIGHTS = {
    'hrv': 0.70,
    'eeg': 0.30
}

class CoherenceEngine:
    def __init__(self):
        self.input_buffer = []
        self.score_cache = {}
        self.bucket_scores = {i: 0.5 for i in range(1, 23)}
        self.harmony = 0.0
        self.selected_arc = 1
        
    def process_inputs(self, inputs):
        """Process 1650 inputs into 110 scores"""
        # inputs: list of 1650 float values (sensor data)
        if len(inputs) != 1650:
            raise ValueError(f"Expected 1650 inputs, got {len(inputs)}")
        
        # Group into 110 score groups (15 inputs per group)
        scores = []
        for i in range(110):
            group = inputs[i*15:(i+1)*15]
            score = np.mean(group) * PHI
            scores.append(score)
        
        return scores
    
    def bio_override(self, hrv_score, eeg_score):
        """Apply bio override: 70% HRV + 30% EEG"""
        return (hrv_score * BIO_WEIGHTS['hrv']) + (eeg_score * BIO_WEIGHTS['eeg'])
    
    def scores_to_buckets(self, scores, bio_factor=0.0):
        """Map 110 scores to 22 buckets"""
        bucket_scores = {}
        
        # Each bucket gets ~5 scores (110/22 = 5)
        for bucket in range(1, 23):
            start_idx = (bucket - 1) * 5
            end_idx = start_idx + 5
            bucket_scores[bucket] = np.mean(scores[start_idx:end_idx])
            
            # Apply bio override
            bucket_scores[bucket] = (bucket_scores[bucket] * 0.7) + (bio_factor * 0.3)
        
        return bucket_scores
    
    def calculate_harmony(self, bucket_scores):
        """Calculate overall harmony from bucket scores"""
        # Harmony is weighted by target proximity
        harmony = 0.0
        total_weight = 0.0
        
        for bucket, score in bucket_scores.items():
            target = BUCKET_TARGETS.get(bucket, 432)
            target_norm = target / DETERMINISTIC_ROOT
            proximity = 1.0 - abs(score - target_norm)
            weight = math.sin(bucket * PI / 44)  # sinusoidal weighting
            
            harmony += proximity * weight
            total_weight += weight
        
        return harmony / total_weight if total_weight > 0 else 0.5
    
    def harmony_to_arc(self, harmony):
        """Map harmony score (0-1) to arc number (1-88)"""
        # Arc selection based on harmony score
        # Higher harmony = higher arc (ascension)
        arc_num = max(1, min(88, int(harmony * 87) + 1))
        
        # Ensure 3-6-9 compliance
        dr = 1 + (arc_num - 1) % 9
        if dr not in [3, 6, 9]:
            # Adjust to nearest 3-6-9 arc
            adjustments = {2:3, 4:3, 5:6, 7:6, 8:9, 1:3}
            arc_num = adjustments.get(arc_num, arc_num)
        
        return arc_num
    
    def full_pipeline(self, inputs_1650, hrv_score=0.5, eeg_score=0.5):
        """Complete pipeline: 1650 inputs → 110 scores → 22 buckets → harmony → arc"""
        scores = self.process_inputs(inputs_1650)
        bio_factor = self.bio_override(hrv_score, eeg_score)
        bucket_scores = self.scores_to_buckets(scores, bio_factor)
        harmony = self.calculate_harmony(bucket_scores)
        arc_num = self.harmony_to_arc(harmony)
        
        self.score_cache = {'scores': scores, 'buckets': bucket_scores, 'harmony': harmony}
        self.selected_arc = arc_num
        
        return {
            'arc': arc_num,
            'harmony': harmony,
            'buckets': bucket_scores,
            'deterministic_root': DETERMINISTIC_ROOT,
            'phi': PHI
        }

# Flask endpoints
engine = CoherenceEngine()

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    inputs = data.get('inputs', [])
    hrv = data.get('hrv_score', 0.5)
    eeg = data.get('eeg_score', 0.5)
    
    if len(inputs) != 1650:
        return jsonify({'error': f'Expected 1650 inputs, got {len(inputs)}'}), 400
    
    result = engine.full_pipeline(inputs, hrv, eeg)
    return jsonify(result)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'engine': 'coherence_engine',
        'deterministic': True,
        'phi': PHI,
        'root': DETERMINISTIC_ROOT,
        'buckets': len(BUCKET_TARGETS),
        'arc_range': '1-88'
    })

@app.route('/arc/<int:arc_num>', methods=['GET'])
def get_arc(arc_num):
    from arc_table import get_arc
    arc = get_arc(arc_num)
    if arc:
        return jsonify(arc)
    return jsonify({'error': 'Arc not found'}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)