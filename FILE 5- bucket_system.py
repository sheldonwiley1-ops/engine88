# bucket_system.py
# 22-Bucket Resolution with Harmony Calculation

import math
from collections import defaultdict

PHI = 1.618033988749895

# 22 buckets with their properties
BUCKETS_22 = {
    1: {'name': 'Root Base', 'frequency': 432.00, 'chakra': 'Root', 'harmony_weight': 0.95},
    2: {'name': 'Root Upper', 'frequency': 441.00, 'chakra': 'Root', 'harmony_weight': 0.92},
    3: {'name': 'Sacral Base', 'frequency': 450.00, 'chakra': 'Sacral', 'harmony_weight': 0.89},
    4: {'name': 'Sacral Upper', 'frequency': 459.00, 'chakra': 'Sacral', 'harmony_weight': 0.86},
    5: {'name': 'Solar Base', 'frequency': 468.00, 'chakra': 'Solar Plexus', 'harmony_weight': 0.83},
    6: {'name': 'Solar Upper', 'frequency': 477.00, 'chakra': 'Solar Plexus', 'harmony_weight': 0.80},
    7: {'name': 'Heart Lower', 'frequency': 486.00, 'chakra': 'Heart', 'harmony_weight': 0.77},
    8: {'name': 'Heart Middle', 'frequency': 495.00, 'chakra': 'Heart', 'harmony_weight': 0.74},
    9: {'name': 'Heart Upper', 'frequency': 504.00, 'chakra': 'Heart', 'harmony_weight': 0.71},
    10: {'name': 'Throat Base', 'frequency': 513.00, 'chakra': 'Throat', 'harmony_weight': 0.68},
    11: {'name': 'Throat Upper', 'frequency': 522.00, 'chakra': 'Throat', 'harmony_weight': 0.65},
    12: {'name': 'Third Eye Lower', 'frequency': 531.00, 'chakra': 'Third Eye', 'harmony_weight': 0.62},
    13: {'name': 'Third Eye Upper', 'frequency': 540.00, 'chakra': 'Third Eye', 'harmony_weight': 0.59},
    14: {'name': 'Crown Base', 'frequency': 549.00, 'chakra': 'Crown', 'harmony_weight': 0.56},
    15: {'name': 'Crown Upper', 'frequency': 558.00, 'chakra': 'Crown', 'harmony_weight': 0.53},
    16: {'name': 'Ether Gateway', 'frequency': 567.00, 'chakra': 'Ether', 'harmony_weight': 0.50},
    17: {'name': 'Soul Star', 'frequency': 576.00, 'chakra': 'Soul', 'harmony_weight': 0.47},
    18: {'name': 'Spirit Gate', 'frequency': 585.00, 'chakra': 'Spirit', 'harmony_weight': 0.44},
    19: {'name': 'Universal Heart', 'frequency': 594.00, 'chakra': 'Universal', 'harmony_weight': 0.41},
    20: {'name': 'Galactic Center', 'frequency': 603.00, 'chakra': 'Galactic', 'harmony_weight': 0.38},
    21: {'name': 'Cosmic Womb', 'frequency': 612.00, 'chakra': 'Cosmic', 'harmony_weight': 0.35},
    22: {'name': 'Source Field', 'frequency': 621.00, 'chakra': 'Source', 'harmony_weight': 0.32}
}

class BucketSystem:
    def __init__(self):
        self.bucket_scores = {i: 0.5 for i in range(1, 23)}
        self.harmony_history = []
    
    def update_bucket(self, bucket_num, score):
        """Update a single bucket score"""
        if 1 <= bucket_num <= 22:
            self.bucket_scores[bucket_num] = max(0.0, min(1.0, score))
    
    def calculate_harmony(self):
        """Calculate overall harmony from all buckets"""
        total = 0.0
        weight_sum = 0.0
        
        for bucket_num, score in self.bucket_scores.items():
            weight = BUCKETS_22[bucket_num]['harmony_weight']
            total += score * weight
            weight_sum += weight
        
        harmony = total / weight_sum if weight_sum > 0 else 0.5
        self.harmony_history.append(harmony)
        
        # Keep last 100 harmony readings
        if len(self.harmony_history) > 100:
            self.harmony_history.pop(0)
        
        return harmony
    
    def get_dominant_bucket(self):
        """Find bucket with highest score"""
        return max(self.bucket_scores, key=self.bucket_scores.get)
    
    def get_bucket_frequency(self, bucket_num):
        """Get resonant frequency for a bucket"""
        return BUCKETS_22.get(bucket_num, {}).get('frequency', 432)
    
    def get_target_arc(self):
        """Determine target arc based on bucket harmony"""
        harmony = self.calculate_harmony()
        # Arc 1-88 mapped from harmony 0-1
        arc = max(1, min(88, int(harmony * 87) + 1))
        
        # Ensure 3-6-9 compliance for critical arcs
        if arc % 9 == 0 or arc % 3 == 0:
            return arc
        else:
            # Adjust to nearest 3-6-9 arc
            adjustments = {1:3, 2:3, 4:3, 5:6, 7:6, 8:9}
            return adjustments.get(arc % 9, arc)
    
    def reset(self):
        """Reset all bucket scores to baseline"""
        self.bucket_scores = {i: 0.5 for i in range(1, 23)}
        self.harmony_history = []