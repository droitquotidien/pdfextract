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
    
    # on insère les balises de paragraphe
    mddata = re.sub('\n\n', '</p>\n<p>', mddata)
    mddata = '<p>' + mddata + '</p>'
    mddata = re.sub('\n*</p>', '</p>', mddata)

    entete = re.search('.*présent[e]* [a-zéê]*.</p>', mddata, flags = re.DOTALL).group()
    mddata = re.sub('.*présent[e]* [a-zéê]*.</p>', '', mddata, flags = re.DOTALL)

    expose = re.search('<p>Faits et procédure.*(?=\n<p>Examen d[ues]+ moyen[s]*)', mddata, flags = re.DOTALL)
    if expose != None:
        mddata = re.sub('<p>Faits et procédure.*(?=\n<p>Examen d[ues]+ moyen[s]*)', '', mddata, flags = re.DOTALL)
    
    dispositif = re.search('(?<=\n)<p>[a-zé, ]*la Cour :</p>\n.*', mddata, flags = re.IGNORECASE | re.DOTALL).group()
    mddata = re.sub('(?<=\n)<p>[a-zé, ]*la Cour :</p>\n.*', '', mddata, flags = re.IGNORECASE | re.DOTALL)

    moymotiv = re.split('<p>Réponse de la Cour', mddata, flags = re.DOTALL)
    moymotiv_list = []
    for i, splitstring in enumerate(moymotiv) :
        if i != 0 :
            splitstring = '<p>Réponse de la Cour' + splitstring
        if i < len(moymotiv) - 1:
            motiv = re.search('.*?</p>(?=\n<p>[a-zàâéèêçïîôùû, ]* moyen.*moyen)', splitstring, flags = re.DOTALL | re.IGNORECASE)
            if motiv != None:
                moymotiv_list.append('<div class="MOTIVATION">')
                moymotiv_list.append(motiv.group())
                moymotiv_list.append('</div>')
                splitstring = re.sub('.*?</p>(?=\n<p>[a-zàâéèêçïîôùû, ]* moyen)', '', splitstring, flags = re.DOTALL | re.IGNORECASE)
        moymotiv_list.append('<div class="MOYEN">')
        moymotiv_list.append(splitstring)
        moymotiv_list.append('</div>')

    motivation = re.search('motivation', mddata, re.DOTALL)


    xmldata = mddata

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append('<div class="ENTETE">')
    xml.append(entete)
    xml.append('</div>')
    if expose != None:
        expose = expose.group()
        xml.append('<div class="EXPOSE">')
        xml.append(expose)
        xml.append('</div>')
    for strg in moymotiv_list:
        xml.append(strg)
    xml.append('<div class="DISPOSITIF">')
    xml.append(dispositif)
    xml.append('</div>')
    xml.append('</decision>')

    outdata = '\n'.join(xml)
    outdata = re.sub('\n\n+', '\n', outdata) # supprime les sauts de ligne

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

