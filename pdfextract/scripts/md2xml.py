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
    enete_re = re.compile(r"a\srendu\s((le\sprésent\sarrêt)|(la\sprésente\sdécision))\.")
    faits_procedure_re = re.compile(r"\nFaits\set\sprocédure\n")
    examen_moyens_re = re.compile(r"\nExamen\s(du|des)\smoyens*\n")
    enonce_moyens_re = re.compile(r"\nEnoncé\s(du|des)\smoyens*\n")
    reponse_re = re.compile(r"\nRéponse\sde\sla\sCour\n", re.IGNORECASE)
    verdict_re = re.compile(r"\n(PAR\sCES\sMOTIFS,)|(EN\sCONSÉQUENCE,)", re.IGNORECASE)

    # Get indices for each match
    idx_entete = next(enete_re.finditer(xmldata)).span()
    idxs_reponse =  [mtch.span() for mtch in reponse_re.finditer(xmldata)]
    idxs_moyens = [mtch.span() for mtch in enonce_moyens_re.finditer(xmldata)]
    idx_verdict = next(verdict_re.finditer(xmldata)).span()
    # If a section isn't in the report, act as if it were empty
    try:
        idx_faits = next(faits_procedure_re.finditer(xmldata)).span()
    except: # Procédure rejetté par la Cour
        idx_faits = idx_entete

    if len(idxs_moyens) == 0 and len(idxs_reponse) != 0:
        idxs_moyens = [[idx_faits[1], idxs_reponse[0][0]]]
    elif len(idxs_reponse) == 0 and len(idxs_moyens) !=0:
        idxs_reponse = [[idxs_moyens[-1][1], idx_verdict[0]]]
    elif len(idxs_reponse) == 0 and len(idxs_moyens) ==0:
        idxs_moyens = [[idx_faits[1], idx_verdict[0]]]
        idxs_reponse = idxs_moyens
    try:
        idx_examen = next(examen_moyens_re.finditer(xmldata)).span()
    except: # Procédure rejetté par la Cour
        idx_examen = [idx_faits[1], idxs_moyens[0][0]]


    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')
    xml.append(f'<div class="entête">{xmldata[:idx_entete[1]]}</div>')
    xml.append(f'<div class="exposé du litige">{xmldata[idx_faits[1]:idx_examen[0]]}</div>')
    xml.append(f'<div class="examen des moyens">{xmldata[idx_examen[0]:idxs_moyens[0][0]]}</div>')
    for i in range(len(idxs_moyens) -1):
        xml.append(f'<div class="énoncé du moyen">{xmldata[idxs_moyens[i][0]:idxs_moyens[i+1][0]]}</div>')
    xml.append(f'<div class="énoncé du moyen">{xmldata[idxs_moyens[-1][0]:idxs_reponse[0][0]]}</div>')
    for i in range(len(idxs_reponse) -1):
        xml.append(f'<div class="réponse de la cour">{xmldata[idxs_reponse[i][0]:idxs_reponse[i+1][0]]}</div>')
    xml.append(f'<div class="réponse de la cour">{xmldata[idxs_reponse[-1][0]:idx_verdict[0]]}</div>')
    xml.append(f'<div class="dispositif">{mddata[idx_verdict[0]:]}</div>')
    xml.append('</decision>')

    outdata = '\n'.join(xml)
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()