# Conversion-de-Fichiers
Les quatre scripts suivant permettent chacun une conversion :
#

— bed2ssam.py : Pour convertir un fichier au format bed en un fichier au
format ssam.<br>
— bed2gmf.py : Pour convertir un fichier au format bed en un fichier au
format gmf.<br>
— ssam2bed.py : Pour convertir un fichier au format ssam en un fichier au
format bed.<br>
— gmf2bed.py : Pour convertir un fichier au format gmf en un fichier au
format bed.<br>
#
Cas d'utilisation :<br>
python3 bed2gmf.py exemple.bed outputbed2gmf.gmf<br>
python3 bed2ssam.py exemple.bed outputbed2ssam.ssam<br>
python3 gmf2bed.py exemple.gmf outputgmf2bed.bed<br>
python3 ssam2bed.py exemple.ssam outputssam2bed.bed<br>
#
Cas d'utilisation de la librairie :<br>

FormatTools.py convert exemple.bed  convertbed2gmf.gmf<br>
FormatTools.py convert exemple.bed  convertbed2gmf.gmf<br>
FormatTools.py convert exemple.ssam  convertssam2bed.gmf<br>
FormatTools.py convert exemple.gmf  convertgmf2bed.gmf<br>
