"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re

"""
Le fait d'avoir inclu une décision de la deuxième chambre civile avec 4 décisions de la
chambre criminelle rend plus difficile les expressions régulières. Il conviendrait à terme de faire une procédure d'extraction
par chambre de la cour de Cassation qui suit les mêmes règles de normalisation sur ses décisions et arrêts
"""

"""
Ce code sépare au minimum le markdown en 3 parties: entête - corps - dispositif
Si le markdown est un texte de la chambre criminelle, il séparera en : entête - fait juridique - examen moyens - moyen et réponse 1,2.. - dispositifs 

"""

def markdown_to_xml_paragraphs(text):
    """Convertit les paragraphes Markdown en éléments XML <p>."""
    paragraphs = text.split('\n\n')
    return '\n'.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())

def extract_moyen_et_reponse(mddata):
    """Extrait et numérote les parties entre 'énoncé du moyen' et 'réponse de la cour'."""
    moyen_et_reponse_pattern = re.compile(r"énoncé du moyen(.*?)réponse de la cour", re.DOTALL | re.IGNORECASE)
    matches = moyen_et_reponse_pattern.findall(mddata)
    moyen_et_reponse_xml = []

    for i, match in enumerate(matches, start=1):
        moyen_et_reponse_xml.append(f'<moyen{i}>{markdown_to_xml_paragraphs(match)}</moyen{i}>')

    return '\n'.join(moyen_et_reponse_xml)

def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Expressions régulières pour identifier les différentes sections
    # 1. entête: toute la partie avant "DECISION DE LA COUR" ou "ARRÊT DE LA COUR"    
    entete_pattern = re.compile(r"^(.+?)(?=décision de la cour|arrêt de la cour)", re.DOTALL | re.IGNORECASE)
    entete = markdown_to_xml_paragraphs(entete_pattern.group(0)) if entete_pattern else ""

    corps = ""
    if "deuxième chambre civile" in mddata.lower():
        # on extrait tout le corps dans le cas d'une décision de la deuxième chambre civile
        corps_pattern = re.compile(r"décision de la cour(.*?)en conséquence", re.DOTALL | re.IGNORECASE)
        corps = markdown_to_xml_paragraphs(corps_pattern.search(mddata).group(0)) if corps_pattern else ""

    else:
        # 2. fait juridique: extraction du paragraphe associé
        fait_juridique_pattern = re.compile(r"(faits et procédures.+?examen des moyens)", re.DOTALL | re.IGNORECASE)
        fait_juridique = markdown_to_xml_paragraphs(fait_juridique_pattern.search(mddata).group(0)) if fait_juridique_pattern else ""

        # 3. examnens des moyens: extraction du paragraphe associé
        examen_moyens_pattern = re.compile(r"(examens des moyens.+?énoncé des moyens)", re.DOTALL | re.IGNORECASE)
        examen_moyens = markdown_to_xml_paragraphs(examen_moyens_pattern.search(mddata).group(0)) if examen_moyens_pattern else ""

        # 4. Extraction et création de paragraphe pour autant d'énoncé et de réponse de la cour possible
        moyen_et_reponse = extract_moyen_et_reponse(mddata)
    
    # 5. décisions: toute la partie après "en conséquence" (chambre criminelle) ou "par ces motifs" (chambre civile)
    dispositif_pattern = re.compile(r"(en conséquence|par ces motifs).*", re.DOTALL | re.IGNORECASE)
    dispositif = markdown_to_xml_paragraphs(dispositif_pattern.search(mddata).group(0)) if dispositif_pattern else ""

    if "deuxième chambre civile" in mddata.lower():
        xml = list()
        xml.append('<?xml version="1.0" encoding="utf-8"?>')
        xml.append('<decision>')
        xml.append('<entete>' + entete + '</entete>')
        xml.append('<corps>' + corps + '</corps>')
        xml.append('<dispositif>' + dispositif + '</dispositif>')
        xml.append('</decision>')
    else:
        xml = list()
        xml.append('<?xml version="1.0" encoding="utf-8"?>')
        xml.append('<decision>')
        xml.append('<entete>' + entete + '</entete>')
        xml.append('<exposeLitige>' + fait_juridique + '</exposeLitige>')
        xml.append('<motivation>' + examen_moyens + '</motivation>')
        xml.append(moyen_et_reponse)  # Inclure les sections "moyen et réponse"
        xml.append('<dispositif>' + dispositif + '</dispositif>')
        xml.append('</decision>')


    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
