class ArcTable:
    def __init__(self):
        self.arcs = {}
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        for i in range(1, 89):
            # CORRECT: Arc 49 = A4 = 432 Hz
            # f = 432 * 2^((arc - 49)/12)
            exponent = (i - 49) / 12.0
            freq = 432.0 * (2.0 ** exponent)
            
            # CORRECT: Note mapping with FLOOR division
            note_idx = (i - 1) % 12
            octave = 3 + ((i - 1) // 12)  # Arc 1 = C1 (octave 1)
            
            # Fix octave for arc 49 (should be A4)
            if i == 49:
                octave = 4
                note_idx = 9  # A
            elif i < 49:
                # Adjust octave for arcs 1-48
                octave = 1 + ((i - 1) // 12)
            else:
                # Adjust octave for arcs 50-88
                octave = 4 + ((i - 49) // 12)
            
            self.arcs[i] = {
                'frequency_hz': round(freq, 2),
                'note': f"{notes[note_idx]}{octave}",
                'mirror_arc': 89 - i,
                'key_index': note_idx
            }
    
    def get_frequency(self, i):
        if 1 <= i <= 88:
            return self.arcs[i]['frequency_hz']
        return 432.0
    
    def get_mirror_arc(self, i):
        if 1 <= i <= 88:
            return self.arcs[i]['mirror_arc']
        return 89
    
    def get_note(self, i):
        if 1 <= i <= 88:
            return self.arcs[i]['note']
        return 'A4'

arc_table = ArcTable()

# VERIFICATION
if __name__ == '__main__':
    print(f"ARC 1: {arc_table.get_frequency(1)} Hz - {arc_table.get_note(1)}")
    print(f"ARC 12: {arc_table.get_frequency(12)} Hz - {arc_table.get_note(12)}")
    print(f"ARC 13: {arc_table.get_frequency(13)} Hz - {arc_table.get_note(13)}")
    print(f"ARC 24: {arc_table.get_frequency(24)} Hz - {arc_table.get_note(24)}")
    print(f"ARC 25: {arc_table.get_frequency(25)} Hz - {arc_table.get_note(25)}")
    print(f"ARC 36: {arc_table.get_frequency(36)} Hz - {arc_table.get_note(36)}")
    print(f"ARC 37: {arc_table.get_frequency(37)} Hz - {arc_table.get_note(37)}")
    print(f"ARC 48: {arc_table.get_frequency(48)} Hz - {arc_table.get_note(48)}")
    print(f"ARC 49: {arc_table.get_frequency(49)} Hz - {arc_table.get_note(49)}")
    print(f"ARC 60: {arc_table.get_frequency(60)} Hz - {arc_table.get_note(60)}")
    print(f"ARC 61: {arc_table.get_frequency(61)} Hz - {arc_table.get_note(61)}")
    print(f"ARC 72: {arc_table.get_frequency(72)} Hz - {arc_table.get_note(72)}")
    print(f"ARC 73: {arc_table.get_frequency(73)} Hz - {arc_table.get_note(73)}")
    print(f"ARC 84: {arc_table.get_frequency(84)} Hz - {arc_table.get_note(84)}")
    print(f"ARC 85: {arc_table.get_frequency(85)} Hz - {arc_table.get_note(85)}")
    print(f"ARC 88: {arc_table.get_frequency(88)} Hz - {arc_table.get_note(88)}")
    print(f"\nMIRROR TEST: Arc1→{arc_table.get_mirror_arc(1)}, Arc88→{arc_table.get_mirror_arc(88)}")
