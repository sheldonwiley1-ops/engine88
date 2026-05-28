class ArcTable:
    def __init__(self):
        self.arcs = {}
        for i in range(1, 89):
            freq = 432 * (2 ** ((i - 49) / 12))
            notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
            self.arcs[i] = {
                'frequency_hz': round(freq, 2),
                'note': notes[(i-1)%12] + str(4 + ((i-1)//12)),
                'mirror_arc': 89 - i,
                'key_index': (i-1)%12
            }
    
    def get_frequency(self, arc_index): return self.arcs.get(arc_index, self.arcs[1])['frequency_hz']
    def get_mirror_arc(self, arc_index): return self.arcs.get(arc_index, self.arcs[1])['mirror_arc']
    def get_note(self, arc_index): return self.arcs.get(arc_index, self.arcs[1])['note']

arc_table = ArcTable()
