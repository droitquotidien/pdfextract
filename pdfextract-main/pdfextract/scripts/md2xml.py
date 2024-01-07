"""
Transforme un document md transformé avec text2md en XML découpé avec le "zonage" de la cour de cassation.
"""
import argparse
import re
import sys
import pdb

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

    # Split the file into several paragraphs, thus we could label the functionality for each paragraph.
    paragraphs = xmldata.split('\n')

    #pdb.set_trace()
    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')

    xml.append('<root>')
    # Entête
    Entete = 'Not found'
    for p in paragraphs:
        Entete_search = re.search(r'DE LA COUR DE CASSATION',p)
        if Entete_search is not None:
            Entete = p
            break
    xml.append('<Entete>')
    xml.append(Entete)
    xml.append('</Entete>')

    # Exposé du litige
    Expose = 'Not found'
    for p in paragraphs:
        Expose_search = re.search(r'a formé le pourvoi',p)
        if Expose_search is not None:
            Expose = p
            break
    xml.append('<Expose>')
    xml.append(Expose)
    xml.append('</Expose>')

    # Motivation
    Motif = 'Not found'
    for p in paragraphs:
        Motif_search = re.search(r'Sur le rapport',p)
        if Motif_search is not None:
            Motif = p
            break
    xml.append('<Motif>')
    xml.append(Motif)
    xml.append('</Motif>')

    # Moyens
    Moyens = 'Not found'
    Moyens_search = re.search(r'\d\.\s(.*?EN CONSÉQUENCE)',mddata,re.DOTALL)
    if Moyens_search is not None:
        Moyens = Moyens_search.group(0)
        
    xml.append('<Moyens>')
    xml.append(Moyens)
    xml.append('</Moyens>')

    # Dispositif
    Dispositif = 'Not found'
    Disp_search = re.search(r'EN CONSÉQUENCE.*\.',mddata,re.DOTALL)
    if Disp_search is not None:
        Dispositif = Disp_search.group(0)

    xml.append('<Disposition>')
    xml.append(Dispositif)
    xml.append('</Disposition>')

    xml.append('</root>')
    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
