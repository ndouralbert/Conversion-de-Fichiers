import argparse
import os
from FormatLibrairie import FormatConverter

def convert_command(source_file, target_file):
    try:
        source_file = os.path.abspath(source_file)
        target_file = os.path.abspath(target_file)

        if not os.path.exists(source_file):
            raise FileNotFoundError(f"Source file not found: {source_file}")

        print(f"Source File: {source_file}")
        print(f"Target File: {target_file}")

        converter = FormatConverter()

        source_extension = os.path.splitext(source_file)[1]
        target_extension = os.path.splitext(target_file)[1]

        print(f"Source Extension: {source_extension}")
        print(f"Target Extension: {target_extension}")

        formats = {"bed": ".bed", "ssam": ".ssam", "gmf": ".gmf"}
        source_format = [format for format, extension in formats.items() if source_extension == extension]
        target_format = [format for format, extension in formats.items() if target_extension == extension]

        print(f"Source Format: {source_format}")
        print(f"Target Format: {target_format}")

        if len(source_format) == 1 and len(target_format) == 1:
            source_format = source_format[0]
            target_format = target_format[0]

            if source_format == "ssam":
                print("Converting from ssam to bed...")
                with open(source_file, 'r') as src_file, open(target_file, 'w') as tgt_file:
                    for line in src_file:
                        seq = converter.ssam2bed(line)
                        bed_entry = f"{seq.Chrom}\t{seq.ChromStart}\t{seq.ChromEnd}\t{seq.ID}\t{seq.Strand}\n"
                        tgt_file.write(bed_entry)
                print("Conversion successful.")
            elif source_format == "bed" and target_format == "gmf":
                print("Converting from bed to gmf...")
                with open(source_file, 'r') as input_bed, open(target_file, 'w') as output_gmf:
                    bed_lines = input_bed.readlines()
                    sequences = converter.bed2gmf(bed_lines)
                    for key, data in sequences.items():
                        output_gmf.write(f"Seq\t{key}\n")
                        output_gmf.write('\n'.join(data) + '\n')
                print("Conversion successful.")
            elif source_format == "gmf" and target_format == "bed":
                print("Converting from gmf to bed...")
                with open(source_file, 'r') as input_gmf, open(target_file, 'w') as output_bed:
                    gmf_lines = input_gmf.readlines()
                    bed_lines = converter.gmf2bed(gmf_lines)
                    for bed_entry in bed_lines:
                        output_bed.write(bed_entry)
                print("Conversion successful.")
            elif source_format == "bed" and target_format == "ssam":
                print("Converting from bed to sam...")
                with open(source_file, 'r') as input_bed, open(target_file, 'w') as output_sam:
                    bed_lines = input_bed.readlines()
                    for bed_line in bed_lines:
                        seq = converter.bed2ssam(bed_line)
                        sam_entry = f"{seq.ID}\t{seq.Strand}\t{seq.Chrom}\t{seq.ChromStart}\t{seq.CIGAR}\n"
                        output_sam.write(sam_entry)
                print("Conversion successful.")
            # Ajouter d'autres cas de conversion au besoin
            else:
                raise ValueError("Conversion not supported for the given formats.")

            print(f"Conversion from {source_format} to {target_format} successful.")
        else:
            raise ValueError("Les extensions de fichiers ne correspondent à aucun format pris en charge.")
    except FileNotFoundError as e:
        print(f"Erreur lors de la conversion : {e}")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Convert between BED, SAM, and GMF formats.")
        parser.add_argument("command", choices=["convert"], help="Conversion command")
        parser.add_argument("source_file", help="Source file name")
        parser.add_argument("target_file", help="Target file name")

        args = parser.parse_args()

        if args.command == "convert":
            convert_command(args.source_file, args.target_file)
        else:
            print("Commande non prise en charge.")
    except Exception as e:
        print(f"Erreur lors de l'exécution du script : {e}")
