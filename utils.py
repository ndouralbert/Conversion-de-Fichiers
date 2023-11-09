# utils.py

import re
import sys

def bed_to_gmf(fic_bed, fic_gmf=None):
    sequences = {}
    try:
        with open(fic_bed, 'r') as bed_file:
            for line in bed_file:
                line = line.strip()

                if not line:
                    continue

                fields = line.split('\t')
                if len(fields) < 4:
                    continue

                key, chrom, chrom_start, chrom_end, Strand = fields[3], fields[0], fields[1], fields[2], fields[4]

                if key not in sequences:
                    sequences[key] = []

                sequences[key].append(f"Align\t{chrom}\t{chrom_start}\t{chrom_end}\t{Strand}")

            # Write the data to the specified file or standard output
            output_file = sys.stdout if fic_gmf is None else open(fic_gmf, 'w')
            for key, data in sequences.items():
                output_file.write(f"Seq\t{key}\n")
                output_file.write('\n'.join(data) + '\n')

            # Close the file if it was opened
            if fic_gmf is not None:
                output_file.close()

    except (IOError, ValueError, IndexError) as e:
        sys.stderr.write(f"Error during conversion BED to GMF: {e}\n")


def bed_to_sam(fic_bed, fic_sam=None):
    try:
        with open(fic_bed, 'r') as bed_file:
            output_file = sys.stdout if fic_sam is None else open(fic_sam, 'w')

            for line in bed_file:
                fields = line.strip().split('\t')
                Rname = fields[0]
                Pos = int(fields[1])
                start = int(fields[1]) + 1
                end = int(fields[2])
                length = end - start + 1
                cigar = f"{length}M"
                QName = fields[3]
                Strand = "1" if fields[4] == "+" else "0"

                sam_line = f"{QName}\t{Strand}\t{Rname}\t{Pos}\t{cigar}"
                output_file.write(sam_line + '\n')

            # Close the file if it was opened
            if fic_sam is not None:
                output_file.close()

    except (IOError, ValueError, IndexError) as e:
        sys.stderr.write(f"Error during conversion BED to SAM: {e}\n")


def gmf_to_bed(fic_gmf, fic_bed=None):
    try:
        with open(fic_gmf, 'r') as gmf_file:
            seq_name = None
            output_file = sys.stdout if fic_bed is None else open(fic_bed, 'w')

            for line in gmf_file:
                line = line.strip()

                if line.startswith("Seq"):
                    seq_name = line.split('\t')[1]
                elif line.startswith("Align"):
                    fields = line.split('\t')
                    chrom = fields[1]
                    chrom_start = int(fields[2])
                    chrom_end = int(fields[3])
                    strand = fields[4]
                    output_file.write(f"{chrom}\t{chrom_start}\t{chrom_end}\t{seq_name}\t{strand}\n")

            # Close the file if it was opened
            if fic_bed is not None:
                output_file.close()

    except (IOError, ValueError, IndexError) as e:
        sys.stderr.write(f"Error during conversion GMF to BED: {e}\n")


def calculate_End(mot):
    try:
        # Use a regular expression to find all numbers in the string
        nombres = [int(match.group(0)) for match in re.finditer(r'\d+', mot)]
        # Use another regular expression to find "I" preceded by a number
        chiffres_precedant_I = [int(match.group(1)) for match in re.finditer(r'(\d+)I', mot)]
        somme_nombres = sum(nombres)
        somme_chiffres_precedants_I = sum(chiffres_precedant_I)
        resultat = somme_nombres - somme_chiffres_precedants_I - 1
        return resultat

    except (ValueError, IndexError) as e:
        sys.stderr.write(f"Error during calculation: {e}\n")


def sam_to_bed(fic_sam, fic_bed=None):
    try:
        with open(fic_sam, 'r') as same_file:
            output_file = sys.stdout if fic_bed is None else open(fic_bed, 'w')

            for line in same_file:
                fields = line.strip().split('\t')
                Chrom = fields[2]
                ChromStart = int(fields[3])
                CIGAR = fields[4]
                End = calculate_End(CIGAR)
                ChromEnd = ChromStart + End
                Name = fields[0]
                Strand = "+" if fields[1] == "1" else "-"
                bed_line = f"{Chrom}\t{ChromStart}\t{ChromEnd}\t{Name}\t{Strand}"
                output_file.write(bed_line + '\n')

            # Close the file if it was opened
            if fic_bed is not None:
                output_file.close()

    except (IOError, ValueError, IndexError) as e:
        sys.stderr.write(f"Error during conversion SAM to BED: {e}\n")
