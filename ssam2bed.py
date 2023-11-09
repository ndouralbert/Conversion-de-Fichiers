# sam_to_bed.py
from utils import sam_to_bed
import sys

try:
    input_sam = sys.argv[1]
    output_bed = sys.argv[2] if len(sys.argv) > 2 else None

    sam_to_bed(input_sam, output_bed)

except Exception as e:
    print(f"Erreur lors de la conversion SAM vers BED : {e}")
