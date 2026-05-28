class BucketSystem:
    def calculate_overall_harmony(self, buckets):
        if not buckets: return 0
        scores = [data['score'] for data in buckets.values()]
        return sum(scores) / len(scores)
    
    def determine_state(self, harmony, delta_harmony):
        if harmony < 30: return 'RECOVERY'
        if harmony < 60: return 'STABILIZE'
        if harmony < 85: return 'OPTIMIZE'
        return 'PEAK'
    
    def calculate_delta_harmony(self, current, previous):
        if previous is None: return 0
        return current - previous
    
    def calculate_spread(self, buckets): return 0
    def find_lowest_bucket(self, buckets): return 'BODY'
