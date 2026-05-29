# arc_table.py
# 88-Arc Harmonic Mapping with All Buckets
# Unified Payload Contract v1.0

ARC_88 = {}

# Base frequencies for 88 arcs (432 Hz cosmic standard)
# Each arc has: frequency, bucket, harmony score, function

arc_data = [
    # Arc 1-11: Root bucket (grounding, physical)
    (1, 432.00, 1, 0.95, "Grounding"),
    (2, 435.00, 1, 0.92, "Physical stability"),
    (3, 438.00, 1, 0.89, "Body awareness"),
    (4, 441.00, 1, 0.86, "Somatic release"),
    (5, 444.00, 1, 0.83, "Cellular reset"),
    (6, 447.00, 1, 0.80, "Nervous quiet"),
    (7, 450.00, 1, 0.77, "Earth connection"),
    (8, 453.00, 1, 0.74, "Ancestral clearing"),
    (9, 456.00, 1, 0.71, "Root lock"),
    (10, 459.00, 1, 0.68, "Physical coherence"),
    (11, 462.00, 1, 0.65, "Body harmony"),
    # Arc 12-22: Sacral bucket (creativity, flow)
    (12, 480.00, 2, 0.95, "Creative flow"),
    (13, 483.00, 2, 0.92, "Emotional release"),
    (14, 486.00, 2, 0.89, "Pleasure activation"),
    (15, 489.00, 2, 0.86, "Relationship harmony"),
    (16, 492.00, 2, 0.83, "Sensual awakening"),
    (17, 495.00, 2, 0.80, "Fluid movement"),
    (18, 498.00, 2, 0.77, "Emotional balance"),
    (19, 501.00, 2, 0.74, "Creativity unlock"),
    (20, 504.00, 2, 0.71, "Joy resonance"),
    (21, 507.00, 2, 0.68, "Passion ignition"),
    (22, 510.00, 2, 0.65, "Sacral coherence"),
    # Arc 23-33: Solar Plexus bucket (power, will)
    (23, 528.00, 3, 0.95, "Personal power"),
    (24, 531.00, 3, 0.92, "Will activation"),
    (25, 534.00, 3, 0.89, "Confidence boost"),
    (26, 537.00, 3, 0.86, "Action force"),
    (27, 540.00, 3, 0.83, "Manifestation"),
    (28, 543.00, 3, 0.80, "Self-esteem"),
    (29, 546.00, 3, 0.77, "Inner strength"),
    (30, 549.00, 3, 0.74, "Determination"),
    (31, 552.00, 3, 0.71, "Courage"),
    (32, 555.00, 3, 0.68, "Leadership"),
    (33, 558.00, 3, 0.65, "Solar coherence"),
    # Arc 34-44: Heart bucket (love, compassion)
    (34, 639.00, 4, 0.95, "Unconditional love"),
    (35, 642.00, 4, 0.92, "Compassion"),
    (36, 645.00, 4, 0.89, "Forgiveness"),
    (37, 648.00, 4, 0.86, "Gratitude"),
    (38, 651.00, 4, 0.83, "Heart opening"),
    (39, 654.00, 4, 0.80, "Empathy"),
    (40, 657.00, 4, 0.77, "Connection"),
    (41, 660.00, 4, 0.74, "Joy"),
    (42, 663.00, 4, 0.71, "Peace"),
    (43, 666.00, 4, 0.68, "Kindness"),
    (44, 669.00, 4, 0.65, "Heart coherence"),
    # Arc 45-55: Throat bucket (truth, expression)
    (45, 741.00, 5, 0.95, "Authentic voice"),
    (46, 744.00, 5, 0.92, "Truth speaking"),
    (47, 747.00, 5, 0.89, "Clear expression"),
    (48, 750.00, 5, 0.86, "Communication"),
    (49, 753.00, 5, 0.83, "Creative speech"),
    (50, 756.00, 5, 0.80, "Listening"),
    (51, 759.00, 5, 0.77, "Vocal release"),
    (52, 762.00, 5, 0.74, "Throat clearing"),
    (53, 765.00, 5, 0.71, "Self-expression"),
    (54, 768.00, 5, 0.68, "Honesty"),
    (55, 771.00, 5, 0.65, "Throat coherence"),
    # Arc 56-66: Third Eye bucket (intuition, vision)
    (56, 852.00, 6, 0.95, "Intuition"),
    (57, 855.00, 6, 0.92, "Inner vision"),
    (58, 858.00, 6, 0.89, "Clarity"),
    (59, 861.00, 6, 0.86, "Perception"),
    (60, 864.00, 6, 0.83, "Insight"),
    (61, 867.00, 6, 0.80, "Wisdom"),
    (62, 870.00, 6, 0.77, "Awareness"),
    (63, 873.00, 6, 0.74, "Focus"),
    (64, 876.00, 6, 0.71, "Concentration"),
    (65, 879.00, 6, 0.68, "Third eye opening"),
    (66, 882.00, 6, 0.65, "Third eye coherence"),
    # Arc 67-77: Crown bucket (spirit, transcendence)
    (67, 963.00, 7, 0.95, "Divine connection"),
    (68, 966.00, 7, 0.92, "Enlightenment"),
    (69, 969.00, 7, 0.89, "Transcendence"),
    (70, 972.00, 7, 0.86, "Unity"),
    (71, 975.00, 7, 0.83, "Bliss"),
    (72, 978.00, 7, 0.80, "Source connection"),
    (73, 981.00, 7, 0.77, "Oneness"),
    (74, 984.00, 7, 0.74, "Liberation"),
    (75, 987.00, 7, 0.71, "Ascension"),
    (76, 990.00, 7, 0.68, "Pure awareness"),
    (77, 993.00, 7, 0.65, "Crown coherence"),
    # Arc 78-88: Ether bucket (integration, all)
    (78, 432.00, 8, 0.95, "Integration"),
    (79, 528.00, 8, 0.92, "Harmonization"),
    (80, 639.00, 8, 0.89, "Synthesis"),
    (81, 741.00, 8, 0.86, "Wholeness"),
    (82, 852.00, 8, 0.83, "Unity field"),
    (83, 963.00, 8, 0.80, "Source return"),
    (84, 432.50, 8, 0.77, "Balance"),
    (85, 528.50, 8, 0.74, "Alignment"),
    (86, 639.50, 8, 0.71, "Coherence"),
    (87, 741.50, 8, 0.68, "Resonance"),
    (88, 852.50, 8, 0.65, "Omnipotence")
]

for arc_num, freq, bucket, harmony, function in arc_data:
    ARC_88[arc_num] = {
        'frequency': freq,
        'bucket': bucket,
        'harmony_score': harmony,
        'function': function,
        'digital_root': 1 + (int(freq) - 1) % 9 if int(freq) > 0 else 0
    }

BUCKET_NAMES = {
    1: 'Root - Grounding & Physical',
    2: 'Sacral - Creativity & Flow',
    3: 'Solar Plexus - Power & Will',
    4: 'Heart - Love & Compassion',
    5: 'Throat - Truth & Expression',
    6: 'Third Eye - Intuition & Vision',
    7: 'Crown - Spirit & Transcendence',
    8: 'Ether - Integration & All'
}

def get_arc(arc_num):
    return ARC_88.get(arc_num, None)

def get_bucket_arcs(bucket_num):
    return {k: v for k, v in ARC_88.items() if v['bucket'] == bucket_num}

def frequency_to_arc(freq):
    closest = min(ARC_88.items(), key=lambda x: abs(x[1]['frequency'] - freq))
    return closest[0], closest[1]