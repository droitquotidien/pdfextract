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
    # document must be a valid XML file
    xmldata = mddata

    #On découpe notre texte en plusieurs parties
    mots_cles = ["Faits et procédure", "Examen des moyens", "Réponse de la Cour", "PAR CES MOTIFS"]
    pattern = re.compile('|'.join(map(re.escape, mots_cles)))
    parties = re.split(pattern, xmldata)

    print(len(parties))

    #On verifie que ca fonctione
    if len(parties) > 5:
        print("if")
        xml = list()
        xml.append('<?xml version="1.0" encoding="utf-8"?>')
        xml.append('<decision>')
        xml.append('<Entête>')
        xml.append('ENTETE')
        xml.append('')
        xml.append(parties[0])
        xml.append('</Entête>')
        xml.append('')
        xml.append('<Exposé_du_litige>')
        xml.append('Exposé du litige')
        xml.append('')
        xml.append(parties[1])
        xml.append('</Exposé_du_litige>')
        xml.append('')
        xml.append('<Motivation>')
        xml.append('Motivation')
        xml.append('')
        xml.append(parties[2])
        xml.append('</Motivation>')
        xml.append('')
        xml.append('<Moyens>')
        xml.append('Moyens')
        xml.append('')
        xml.append(parties[3])
        xml.append('</Moyens>')
        xml.append('')
        xml.append('<Dispositif>')
        xml.append('Dispositifs')
        xml.append('')
        xml.append(parties[4])
        xml.append('</Dispositif>')
        xml.append('')
        xml.append('</decision>')
    
    else:
        print("else")
        xml = list()
        xml.append('<?xml version="1.0" encoding="utf-8"?>')
        xml.append('<decision>')
        xml.append(xmldata)
        xml.append('</decision>')
       
    
    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
