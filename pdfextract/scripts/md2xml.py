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
    
    var = re.split(r'(DU \d+ \w* 2023)',mddata)     # on remplit l'entete si on a la mention de la date
    if len(var)==3:
        entete, exp_reg , txt_suite = var
        entete = entete + exp_reg
        mddata = txt_suite
    else:
        entete = ''
    
    var = re.split(r'(Sur le rapport)',mddata)      # on remplit l'expose si on a la mention "sur le rapport", début de la partie motivation
    if len(var)==3:
        expose, exp_reg , txt_suite = var
        expose = expose 
        mddata = exp_reg + txt_suite 
    else:
        expose = ''
    
    var = re.split(r'(Examen d.*moyens?)',mddata)   # on teste si on a examen des moyens, si oui la motiv est rempli jusqu'à la section moyen, sinon on n'a pas de moyens
    if len(var)==3:
        motiv, exp_reg , txt_suite = var
        motiv = motiv 
        mddata = exp_reg + txt_suite 
        moyens = 'en attente'
    else:
        moyens = ''
    
    var = re.split(r'(PAR CES MOTIFS.*la Cour :|EN CONSÉQUENCE.*la Cour :)',mddata) # on rempli la section d'après (moyens s'il y en a, motiv s'il n'y en a pas) jus'qu'au début de la desction dispositif commençant par 'par ces motifs' ou 'en conséquences'
    print(len(var))
    if len(var)==3:
        if moyens == '':
            motiv, exp_reg , txt_suite = var
            motiv = motiv 
            mddata = exp_reg + txt_suite 
        else:
            moyens, exp_reg , txt_suite = var
            moyens = moyens 
            mddata = exp_reg + txt_suite 
    else:
        motiv = ''

    
    
    dispo = mddata          # la partie dispositif correspond à ce qui reste

    xml = list() # on rempli iterativement le fichier xml
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append('<Entête>')
    xml.append(entete)
    xml.append('</Entête>')
    xml.append('<Exposé du litige>')
    xml.append(expose)
    xml.append('</Exposé du litige>')
    xml.append('<Motivation>')
    xml.append(motiv)
    xml.append('</Motivation>')
    xml.append('<Moyens>')
    xml.append(moyens)
    xml.append('</Moyens>')
    xml.append('<Dispositif>')
    xml.append(dispo)
    xml.append('</Dispositif>')
    xml.append('</decision>')
    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 
