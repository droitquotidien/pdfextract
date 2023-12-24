#!/usr/bin/python3

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
    
    print("Traitement du fichier "+ args.in_file)

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # On découpe le texte selon 4 expressions délimitant 5 parties 
    parties = re.split(r'(Faits et procédure|Examen d.+ moyen.*|Réponse de la Cour|PAR CE.* MOTIF.*, la Cour :)',mddata)
    
    # Test que le texte à bien été découpé
    if len(parties) < 9:
        raise Exception(f"Echec de la découpe du texte en parties.")        
    
    # Pour chaque partie découpée (en-tête, exposé du litige,moyens, motivations, dispositifs) : on créé une balise et on découpe le texte venant en paragraphes au sein de la balise

    # En-tête
    # On commence au 2nd paragraphe pour retirer la ligne de titre ajoutée à l'étape markdown
    xmldata = '<div class="entete">\n'
    for s in re.split(r'\n+',parties[0])[1:]:
        if s == "": continue
        xmldata += "<p>" + s + "</p>"
    xmldata += "\n</div>\n"

    # Exposé du litige
    xmldata += '<div class="expose_litige">\n'
    # Première phrase
    xmldata += "<p>" + parties[1].replace("\n"," ") + "</p>"
    for s in re.split(r'\n+',parties[2]):
        if s == "": continue
        xmldata += "<p>" + s + "</p>"
    xmldata += "\n</div>\n" 

    # Motivation
    xmldata += '<div class="moyens">\n'
    # Première phrase
    xmldata += "<p>" + parties[3] + "</p>"
    for s in re.split(r'\n+',parties[4]):
        if s == "": continue
        xmldata += "<p>" + s + "</p>"
    xmldata += "\n</div>\n"

    # Moyens
    xmldata += '<div class="motivations">\n'
    # Première phrase
    xmldata += "<p>" + parties[5] + "</p>"
    for s in re.split(r'\n+',parties[6]):
        if s == "": continue
        xmldata += "<p>" + s + "</p>"
    xmldata += "\n</div>\n"

    # Dispositif
    xmldata += '<div class="dispositif">\n'
    # Première phrase
    xmldata += "<p>" + parties[7] + "</p>"
    for s in re.split(r'\n+',parties[8]):
        if s == "": continue
        xmldata += "<p>" + s + "</p>"
    xmldata += "\n</div>"
    
    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

    print("Résultats sauvegardés sous "+ args.out_file)
        
if __name__ == "__main__":
    main()
