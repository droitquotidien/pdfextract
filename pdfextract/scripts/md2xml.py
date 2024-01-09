"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys

def treat_data(xmldata):
    # Entête
    paras = xmldata.split('\n')
    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<root>')
    Entete = 'None'
    for p in paras:
        Entete_search = re.search(r'DE LA COUR DE CASSATION',p)
        if Entete_search is not None:
            Entete = p
            break
    xml.append('<Entete>')
    xml.append(Entete)
    xml.append('</Entete>')

    # Exposé du litige
    Expose = 'None'
    for p in paras:
        Expose_search = re.search(r'a formé le pourvoi',p)
        if Expose_search is not None:
            Expose = p
            break
    xml.append('<Expose>')
    xml.append(Expose)
    xml.append('</Expose>')

    # Motivation
    Motif = 'None'
    for p in paras:
        Motif_search = re.search(r'Sur le rapport',p)
        if Motif_search is not None:
            Motif = p
            break
    xml.append('<Motif>')
    xml.append(Motif)
    xml.append('</Motif>')

    # Moyens
    Moyens = 'None'
    Moyens_search = re.search(r'\d\.\s(.*?EN CONSÉQUENCE)',xmldata,re.DOTALL)
    if Moyens_search is not None:
        Moyens = Moyens_search.group(0)
    xml.append('<Moyens>')
    xml.append(Moyens)
    xml.append('</Moyens>')

    # Dispositif
    Dispositif = 'None'
    Disp_search = re.search(r'EN CONSÉQUENCE.*\.',xmldata,re.DOTALL)
    if Disp_search is not None:
        Dispositif = Disp_search.group(0)
    xml.append('<Disposition>')
    xml.append(Dispositif)
    xml.append('</Disposition>')
    xml.append('</root>')

    return xml
    

def main():
    parser = argparse.ArgumentParser("Markdown to XML")
    parser.add_argument('in_file', help="Markdown file")
    parser.add_argument('out_file', help="XML file")
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        xmldata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    xml = treat_data(xmldata)
    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
