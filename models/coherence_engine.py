class CoherenceEngine:
    def __init__(self):
        self.hrv_low_threshold = 30
        self.eeg_low_threshold = 0.3
        self.safe_mode_intensity = 0.3
    
    def check_bio_override(self, inputs):
        hrv = inputs.get('L0_hrv', 65)
        eeg = inputs.get('L0_eeg_coherence', 0.7)
        return hrv < self.hrv_low_threshold or eeg < self.eeg_low_threshold
