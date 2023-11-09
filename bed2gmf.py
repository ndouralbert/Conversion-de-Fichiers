# bed_to_gmf.py
from utils import bed_to_gmf
import sys

try:
    input_bed = sys.argv[1]
    output_gmf = sys.argv[2] if len(sys.argv) > 2 else None

    bed_to_gmf(input_bed, output_gmf)

except Exception as e:
    print(f"Erreur lors de la conversion BED vers GMF : {e}")
