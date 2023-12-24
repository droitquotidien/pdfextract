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

    print(args.in_file)

    with open(args.in_file, "r", encoding="utf-8") as f:
        mddata = f.read()

    # Transform mddata with re here
    # see https://docs.python.org/fr/3/library/re.html
    # document must be a valid XML file
    xmldata = mddata

    # defining regexes for each section
    entete_re = re.compile(r"a\srendu\sle\sprésent\s(arrêt)|(décision)\.", re.IGNORECASE)
    faits_re = re.compile(r"\nFaits\set\sprocédure\n", re.IGNORECASE)
    # example for "mais sur": https://www.courdecassation.fr/decision/6584018a8704660008a29711?search_api_fulltext=&op=Rechercher&date_du=&date_au=&judilibre_juridiction=all&previousdecisionpage=0&previousdecisionindex=6&nextdecisionpage=0&nextdecisionindex=8
    moyens_re = re.compile(r"((mais\s)*sur le .*)*\n\nEnoncé\s(du|des)\smoyens*\n", re.IGNORECASE)
    examen_moyen_re = re.compile(r"\nExamen\s(du|des)\smoyens*\n", re.IGNORECASE)
    motivation_re = re.compile(r"\nRéponse\sde\sla\sCour\n", re.IGNORECASE)
    dispositif_re = re.compile(r"\n((par\sces\smotifs,)|(en\sconséquence,))", re.IGNORECASE)

    # finding indexes of each section
    idx_dispo = next(re.finditer(dispositif_re, xmldata)).start(0)
    idx_entete = next(re.finditer(entete_re, xmldata)).end(0)+1
    try:
        idx_examen = next(re.finditer(examen_moyen_re, xmldata)).start(0)
        idx_faits = next(re.finditer(faits_re, xmldata)).start(0)
    except:
        # no examen = no fait: we skip the faits and moyens sections
        idx_faits = idx_dispo
        idx_examen = None

    idxs_moyens = [m.start(0) for m in re.finditer(moyens_re, xmldata)] + [idx_dispo]
    idxs_motivations = [m.start(0) for m in re.finditer(motivation_re, xmldata)]

    # if no motivation 
    if len(idxs_motivations) == 0:
        idx_fin_faits = idx_dispo
    else:
        idx_fin_faits = idxs_motivations[0]

    assert len(idxs_moyens) == len(idxs_motivations) + 1, "Moyens and motivations are not matching"

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')

    # entete = jusqu'a rendu le present arret.
    xml.append('<div class="entete">')
    entete = xmldata[:idx_entete]
    xml.append(entete)
    xml.append('</div>')

    # si expose du litige (faits et procedure)
    if idx_faits != idx_dispo:
        # faits = entre rendu le present arret et faits et procedure
        xml.append('<div class="expose">')
        faits = xmldata[idx_faits:idx_examen if idx_examen is not None else idxs_moyens[0]]
        xml.append(faits)
        xml.append('</div>')
    else:
        # uniquement quand motivation SANS moyen
        # motivation = entre rendu le present arret et faits et procedure
        xml.append('<div class="motivation">')
        motivation = xmldata[idx_entete:idx_fin_faits]
        xml.append(motivation)
        xml.append('</div>')

    if idx_examen is not None:
        # examen des moyens = avant moyens
        moyens = xmldata[idx_examen:idxs_moyens[0]]
        moyens_split = moyens.split('\n\n')

        # si pas de motivation avant le traitement des moyens
        # on ne separe pas les sections
        if len(moyens_split) <= 2:
            idxs_moyens[0] = idx_examen
        else:
            # sinon on separe les sections
            xml.append('<div class="moyens">')
            xml.append(moyens_split[0] + ('\n\n' + moyens_split[1] if len(moyens_split) > 1 else ''))
            xml.append('</div>')
            if len(moyens_split) > 2:
                xml.append('<div class="motivation">')
                xml.append(moyens_split[2])
                xml.append('</div>')

    # moyens et motivations (qui vont de pair, sauf exception, qui est traite en amont)
    for i in range(len(idxs_moyens)-1):
        # moyen toujours precede de 'enonce du/des moyen(s)'
        xml.append('<div class="moyens">')
        moyens = xmldata[idxs_moyens[i]:idxs_motivations[i]]
        xml.append(moyens)
        xml.append('</div>')

        # motivation = entre reponse de la cour et reponse de la cour
        xml.append('<div class="motivation">')
        motivation = xmldata[idxs_motivations[i]:idxs_moyens[i+1]]
        xml.append(motivation)
        xml.append('</div>')

    # dispositif = par ces motifs, en consequence
    xml.append('<div class="dispositif">')
    dispositif = xmldata[idx_dispo:]
    xml.append(dispositif)
    xml.append('</div>')

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

if __name__ == "__main__":
    main()