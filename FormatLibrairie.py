import re
#FormatLibrairie.py
class Sequence:
    def __init__(self, ID: str, Strand: str, Chrom: str, ChromStart: int, ChromEnd: int, CIGAR: str):
        self.ID = ID
        self.Strand = Strand
        self.Chrom = Chrom
        self.ChromStart = ChromStart
        self.ChromEnd = ChromEnd
        self.CIGAR = CIGAR

    def __str__(self):
        return f"""Les informations de la séquence sont :
        Son Identifiant : {self.ID}
        Son Brin : {self.Strand}
        Son chromosome : {self.Chrom}
        Son début : {self.ChromStart}
        Sa fin : {self.ChromEnd}
        Son code CIGAR : {self.CIGAR}"""

    def __repr__(self):
        return self.__str__()

class FormatConverter:
    def calculate_End(self, mot):
        nombres = [int(match.group(0)) for match in re.finditer(r'\d+', mot)]
        chiffres_precedant_I = [int(match.group(1)) for match in re.finditer(r'(\d+)I', mot)]
        somme_nombres = sum(nombres)
        somme_chiffres_precedants_I = sum(chiffres_precedant_I)
        resultat = somme_nombres - somme_chiffres_precedants_I - 1
        return resultat

    def bed2ssam(self, bed_line):
        fields = bed_line.strip().split('\t')
        Rname, Pos, QName, Strand = fields[0], int(fields[1]), fields[3], "1" if fields[4] == "+" else "0"
        start = Pos + 1
        end = int(fields[2])
        length = end - start + 1
        cigar = f"{length}M"
        return Sequence(QName, Strand, Rname, Pos, end, cigar)


    def ssam2bed(self, sam_line):
        fields = sam_line.strip().split('\t')
        Chrom, ChromStart, CIGAR, ID, Strand = fields[2], int(fields[3]), fields[4], fields[0], "+" if fields[1] == "1" else "-"
        length = self.calculate_End(CIGAR)
        ChromEnd = ChromStart + length
        return Sequence(ID, Strand, Chrom, ChromStart, ChromEnd, CIGAR)

    def bed2gmf(self, bed_lines):
        sequences = {}
        for line in bed_lines:
            try:
                fields = line.strip().split('\t')
                if len(fields) >= 5:
                    ID, chrom, chrom_start, chrom_end, Strand = fields[3], fields[0], int(fields[1]), int(fields[2]), fields[4]
                    sequences.setdefault(ID, []).append(f"Align\t{chrom}\t{chrom_start}\t{chrom_end}\t{Strand}")
            except (ValueError, IndexError) as e:
                print(f"Erreur lors de la conversion BED vers GMF : {e}")

        return sequences

    def gmf2bed(self, gmf_lines):
        try:
            output_bed_lines = []
            seq_name = None
            for line in gmf_lines:
                fields = line.strip().split('\t')

                if fields[0] == "Seq":
                    seq_name = fields[1]
                elif fields[0] == "Align":
                    chrom, chrom_start, chrom_end, strand = fields[1], int(fields[2]), int(fields[3]), fields[4]
                    output_bed_lines.append(f"{chrom}\t{chrom_start}\t{chrom_end}\t{seq_name}\t{strand}\n")

            return output_bed_lines
        except (ValueError, IndexError) as e:
            print(f"Erreur lors de la conversion GMF vers BED : {e}")
