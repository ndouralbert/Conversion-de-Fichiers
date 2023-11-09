# bed_to_sam.py
from utils import bed_to_sam
import sys

try:
    input_bed = sys.argv[1]
    output_sam = sys.argv[2] if len(sys.argv) > 2 else None

    bed_to_sam(input_bed, output_sam)

except Exception as e:
    print(f"Erreur lors de la conversion BED vers SAM : {e}")
