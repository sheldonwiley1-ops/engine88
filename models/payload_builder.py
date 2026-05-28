from datetime import datetime

class PayloadBuilder:
    def build_payload(self, harmony, state, spread, lowest_bucket, current_arc, bio_override, previous_payload):
        from models.arc_table import arc_table
        return {
            'harmony': round(harmony, 2),
            'state': state,
            'spread': round(spread, 2),
            'lowest_bucket': lowest_bucket,
            'current_arc': current_arc,
            'frequency_hz': arc_table.get_frequency(current_arc),
            'note': arc_table.get_note(current_arc),
            'mirror_arc': arc_table.get_mirror_arc(current_arc),
            'bio_override': bio_override,
            'timestamp': datetime.now().isoformat(),
            'tick_id': (previous_payload.get('tick_id', 0) + 1) if previous_payload else 1
        }
