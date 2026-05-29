# payload_builder.py
# Unified Payload Contract Compliance

import json
import hashlib
from datetime import datetime
from collections import OrderedDict

# Payload contract version
PAYLOAD_VERSION = "1.0.0"
CONTRACT_ID = "ENGINE88_UNIFIED_v1"

class PayloadBuilder:
    """Builds compliant payloads for the unified contract"""
    
    def __init__(self):
        self.schema = {
            "version": PAYLOAD_VERSION,
            "contract_id": CONTRACT_ID,
            "timestamp": None,
            "deterministic_root": 432,
            "phi": 1.618033988749895,
            "inputs": [],
            "scores": [],
            "buckets": [],
            "harmony": None,
            "selected_arc": None,
            "signature": None
        }
    
    def build(self, inputs_1650, scores_110, buckets_22, harmony, selected_arc):
        """Build a compliant payload"""
        payload = OrderedDict()
        payload['version'] = self.schema['version']
        payload['contract_id'] = self.schema['contract_id']
        payload['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        payload['deterministic_root'] = self.schema['deterministic_root']
        payload['phi'] = self.schema['phi']
        
        # Inputs (1650 values)
        payload['inputs'] = inputs_1650[:1650] if len(inputs_1650) >= 1650 else inputs_1650
        
        # Scores (110 values)
        payload['scores'] = scores_110[:110] if len(scores_110) >= 110 else scores_110
        
        # Buckets (22 values)
        payload['buckets'] = buckets_22[:22] if len(buckets_22) >= 22 else buckets_22
        
        payload['harmony'] = harmony
        payload['selected_arc'] = selected_arc
        
        # Generate signature for integrity
        payload_str = json.dumps(payload, separators=(',', ':'))
        payload['signature'] = hashlib.sha256(payload_str.encode()).hexdigest()
        
        return payload
    
    def validate(self, payload):
        """Validate a payload against the contract"""
        required_fields = ['version', 'contract_id', 'timestamp', 'deterministic_root', 
                          'phi', 'inputs', 'scores', 'buckets', 'harmony', 'selected_arc', 'signature']
        
        # Check all required fields present
        for field in required_fields:
            if field not in payload:
                return False, f"Missing field: {field}"
        
        # Check version
        if payload['version'] != PAYLOAD_VERSION:
            return False, f"Version mismatch: {payload['version']} != {PAYLOAD_VERSION}"
        
        # Check deterministic root
        if payload['deterministic_root'] != 432:
            return False, f"Invalid deterministic root: {payload['deterministic_root']}"
        
        # Verify signature
        payload_copy = payload.copy()
        sig = payload_copy.pop('signature')
        payload_str = json.dumps(payload_copy, separators=(',', ':'))
        expected_sig = hashlib.sha256(payload_str.encode()).hexdigest()
        
        if sig != expected_sig:
            return False, "Signature mismatch"
        
        # Check input count (flexible, allow partial)
        if len(payload['inputs']) < 100:
            return False, f"Insufficient inputs: {len(payload['inputs'])}"
        
        return True, "Valid"
    
    def compress(self, payload):
        """Compress payload for transmission"""
        # Remove unnecessary whitespace and sort keys
        return json.dumps(payload, separators=(',', ':'), sort_keys=True)
    
    def expand(self, compressed):
        """Expand compressed payload"""
        return json.loads(compressed)

# Contract compliance checker
def verify_compliance(payload_or_dict):
    """Verify that a payload meets the unified contract"""
    pb = PayloadBuilder()
    if isinstance(payload_or_dict, str):
        payload_or_dict = json.loads(payload_or_dict)
    return pb.validate(payload_or_dict)

# Example usage
if __name__ == "__main__":
    pb = PayloadBuilder()
    test_payload = pb.build(
        inputs_1650=[0.5] * 1650,
        scores_110=[0.5] * 110,
        buckets_22=[0.5] * 22,
        harmony=0.618,
        selected_arc=42
    )
    valid, msg = pb.validate(test_payload)
    print(f"Payload valid: {valid} - {msg}")