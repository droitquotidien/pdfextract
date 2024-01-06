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

    en_tete = re.compile('a\srendu\sle\sprésent\sarrêt\.', re.IGNORECASE)
    expose = re.compile("faits\set\sprocédure", re.IGNORECASE)
    moyens = re.compile("(examen\s(du|des)\smoyen(\n|s\n))|(enoncé\s(du|des)\smoyen(|s))", re.IGNORECASE)
    motivations = re.compile("réponse\sde\sla\scour\n", re.IGNORECASE)
    dispositifs = re.compile("par\s(ce|ces)\smotif(|s)", re.IGNORECASE)

    ind_en_tete = next(re.finditer(en_tete, xmldata)).start(0)
    ind_expose = next(re.finditer(expose, xmldata)).start(0)
    ind_dispositifs = next(re.finditer(dispositifs, xmldata)).start(0)

    ind_moyens, ind_motivations = [], []
    for i in  re.finditer(moyens, xmldata):
        ind_moyens.append(i.start(0))
    ind_moyens.remove(ind_moyens[1])
    for i in  re.finditer(motivations, xmldata):
        ind_motivations.append(i.start(0))

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    
    xml.append('<div class="EN TETE">')
    xml.append(xmldata[:ind_en_tete])
    xml.append('<\div>')

    xml.append('<div class="EXPOSE">')
    if ind_expose:
        xml.append(xmldata[ind_expose:ind_moyens[0]])
    xml.append('<\div>')
    
    #there might be more than 1 moyen/dispositif
    for i in range(len(ind_motivations)):
        xml.append(f'<div class="MOYENS {i}">')
        xml.append(xmldata[ind_moyens[i]:ind_motivations[i]])
        xml.append('<\div>')

        xml.append(f'<div class="MOTIVATIONS {i}">')
        if i < len(ind_motivations) - 1:
            xml.append(xmldata[ind_motivations[i]:ind_moyens[i+1]])
        else:
            xml.append(xmldata[ind_motivations[i]:ind_dispositifs])
        xml.append('<\div>')

    xml.append('<div class="DISPOSITIFS">')
    xml.append(xmldata[ind_dispositifs:])
    xml.append('<\div>')

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
