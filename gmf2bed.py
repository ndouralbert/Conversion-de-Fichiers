# gmf_to_bed.py
from utils import gmf_to_bed
import sys

try:
    input_gmf = sys.argv[1]
    output_bed = sys.argv[2] if len(sys.argv) > 2 else None

    gmf_to_bed(input_gmf, output_bed)

except Exception as e:
    print(f"Erreur lors de la conversion GMF vers BED : {e}")
