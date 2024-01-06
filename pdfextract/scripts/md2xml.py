"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata_with_paragraphs = re.sub(r'\n([^\n]+)\n', r"\n<p>\1</p>\n", mddata)
    mddata_header = re.sub(r'(# Pourvoi \d{2}-\d{2}.\d{3} du \d{1,2}\D+\d{4}\n)', r"\1<div class='Entête'>", mddata_with_paragraphs)
    mddata_dispute = re.sub(r'(<p>Faits et procédure</p>)', r"</div>\n<div class='Exposé du litige'>\n\1", mddata_header)
    match = re.search(r'(EN CONSÉQUENCE, la Cour :|PAR CES MOTIFS,[^\n]* la Cour :)', mddata)
    # Special case for 21-24.923
    if match.group(1) == 'EN CONSÉQUENCE, la Cour :':
        mddata_motivation = re.sub(r'(\n<p>1.)', r"</div>\n<div class='Motivation'>\n\1", mddata_dispute)
    else:
        mddata_means = re.sub(r'(<p>Examen du moyen</p>|<p>Examen des moyens</p>)', r"</div>\n<div class='Moyens'>\n\1", mddata_dispute)
        mddata_means = re.sub(r'(<p>[^\n]+ème moyen[^\n]*</p>)', r"</div>\n<div class='Moyens'>\n\1", mddata_means)    
        mddata_motivation = re.sub(r'(<p>Réponse de la Cour</p>)', r"</div>\n<div class='Motivation'>\n\1", mddata_means)
        # Special case for 22-81.985
        mddata_motivation = re.sub(r"</div>\n<div class='Moyens'>\n<p>Sur le premier moyen, le deuxième moyen, pris en sa première branche, les quatrième,"
                                   " sixième et septième moyens et le neuvième moyen, pris en sa première branche</p>\n\n<p>10. Les griefs ne sont pas de "
                                   "nature à permettre l'admission du pourvoi au sens de l'article 567-1-1 du code de procédure pénale.</p>",
                                   r"<p>Sur le premier moyen, le deuxième moyen, pris en sa première branche, les quatrième,"
                                   " sixième et septième moyens et le neuvième moyen, pris en sa première branche</p>\n\n</div>\n<div class='Motivation'>\n"
                                   "<p>10. Les griefs ne sont pas de "
                                   "nature à permettre l'admission du pourvoi au sens de l'article 567-1-1 du code de procédure pénale.</p>",
                                    mddata_motivation)
    mddata_decision = re.sub(r'(<p>EN CONSÉQUENCE, la Cour :</p>|<p>PAR CES MOTIFS,[^\n]* la Cour :</p>)', r"</div>\n<div class='Dispositif'>\n\1", mddata_motivation)

    xmldata = mddata_decision

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</div>\n</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
