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

    mddata='<introduction>\n' + mddata + r'</reponse>'
    mddata=re.sub('Faits et procédure',r'</introduction>\n<faits>',mddata)
    mddata=re.sub('Examen (.)+ moyen(s)?','</faits>',mddata)
    mddata=re.sub('Enoncé (.)+ moyen(s)?','</reponse>\n<moyen>',mddata)
    mddata=re.sub('Réponse de la Cour','</moyen>\n<reponse>',mddata)
    mddata=re.sub(r'((.)+)?(S|s)ur(.)+moyen((.)+)?\n','',mddata)
    mddata=re.sub(r'</reponse>\n<moyen>','<moyen>',mddata, count=1)


    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(xmldata)
    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
