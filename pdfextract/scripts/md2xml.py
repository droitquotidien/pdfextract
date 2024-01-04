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
    """Extrait et numérote les moyens et les réponses de la cour associées."""
    moyen_et_reponse_xml = []

    # Trouver tous les "énoncé du moyen"
    moyens_matches = re.finditer(r"enoncé du moyen(.*?)(réponse de la cour)", mddata, re.DOTALL | re.IGNORECASE)

    for i, moyen_match in enumerate(moyens_matches, start=1):
        # Extraire le texte du moyen
        moyen_text = moyen_match.group(1)
        moyen_et_reponse_xml.append(f'<moyen{i}>{markdown_to_xml_paragraphs(moyen_text)}</moyen{i}>')

        # Trouver la "réponse de la cour" suivant immédiatement ce moyen
        end_pos = moyen_match.end(1)  # Fin du texte du moyen
        reponse_match = re.search(r"réponse de la cour(.*?)(?=enoncé du moyen|PAR CES MOTIFS)", mddata[end_pos:], re.DOTALL | re.IGNORECASE)
        if reponse_match:
            reponse_text = reponse_match.group(1)
            moyen_et_reponse_xml.append(f'<reponse{i}>{markdown_to_xml_paragraphs(reponse_text)}</reponse{i}>')

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
    entete_match = entete_pattern.search(mddata) if entete_pattern else None
    entete = markdown_to_xml_paragraphs(entete_match.group(0)) if entete_match else ""

    corps = ""
    if "deuxième chambre civile" in mddata.lower():
        # on extrait tout le corps dans le cas d'une décision de la deuxième chambre civile
        corps_pattern = re.compile(r"décision de la cour(.*?)en conséquence", re.DOTALL | re.IGNORECASE)
        corps_match = corps_pattern.search(mddata) if corps_pattern else None
        corps = markdown_to_xml_paragraphs(corps_match.group(0)) if corps_match else ""

    else:
        # 2. fait juridique: extraction du paragraphe associé
        fait_juridique_pattern = re.compile(r"(faits et procédure.+?)(?=examen (?:du moyen|des moyens))", re.DOTALL | re.IGNORECASE)
        fait_juridique_match = fait_juridique_pattern.search(mddata) if fait_juridique_pattern else None
        fait_juridique = markdown_to_xml_paragraphs(fait_juridique_match.group(0)) if fait_juridique_match else ""

        # 3. examnens des moyens: extraction du paragraphe associé 
        examen_moyens_pattern = re.compile(r"(examen (?:du moyen|des moyens).+?)(?=enoncé (?:du moyen|des moyens))", re.DOTALL | re.IGNORECASE)
        examen_moyens_match = examen_moyens_pattern.search(mddata) if examen_moyens_pattern else None
        examen_moyens = markdown_to_xml_paragraphs(examen_moyens_match.group(0)) if examen_moyens_match else ""

        # 4. Extraction et création de paragraphe pour autant d'énoncé et de réponse de la cour possible
        moyen_et_reponse = extract_moyen_et_reponse(mddata)
    
    # 5. décisions: toute la partie après "en conséquence" (chambre criminelle) ou "par ces motifs" (chambre civile)
    dispositif_pattern = re.compile(r"(EN CONSÉQUENCE|PAR CES MOTIFS).*", re.DOTALL)
    dispositif_match = dispositif_pattern.search(mddata) if dispositif_pattern else None
    dispositif = markdown_to_xml_paragraphs(dispositif_match.group(0)) if dispositif_match else ""

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
        if moyen_et_reponse:  # Vérifier si 'moyen_et_reponse' contient des données
            xml.append('<moyensEtReponses>' + moyen_et_reponse + '</moyensEtReponses>')
        xml.append('<dispositif>' + dispositif + '</dispositif>')
        xml.append('</decision>')


    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

if __name__ == '__main__':
    main()
