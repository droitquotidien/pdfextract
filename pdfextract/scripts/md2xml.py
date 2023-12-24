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

    entete_re = re.compile(r"a\srendu\sle\sprésent\s(arrêt)|(décision)\.", re.IGNORECASE)
    dispositif_re = re.compile(r"\n((par\sces\smotifs,)|(en\sconséquence,))", re.IGNORECASE)
    faits_re = re.compile(r"\nFaits\set\sprocédure\n", re.IGNORECASE)
    motivation_re = re.compile(r"\nRéponse\sde\sla\sCour\n", re.IGNORECASE)
    moyens_re = re.compile(r"((mais\s)*sur le .*)*\n\nEnoncé\s(du|des)\smoyens*\n", re.IGNORECASE)
    examen_moyen_re = re.compile(r"\nExamen\s(du|des)\smoyens*\n", re.IGNORECASE)
    # https://www.courdecassation.fr/decision/6584018a8704660008a29711?search_api_fulltext=&op=Rechercher&date_du=&date_au=&judilibre_juridiction=all&previousdecisionpage=0&previousdecisionindex=6&nextdecisionpage=0&nextdecisionindex=8
    # mais sur

    idx_dispo = next(re.finditer(dispositif_re, xmldata)).start(0)
    idx_entete = next(re.finditer(entete_re, xmldata)).end(0)+1
    try:
        idx_examen = next(re.finditer(examen_moyen_re, xmldata)).start(0)
        idx_faits = next(re.finditer(faits_re, xmldata)).start(0)
    except:
        idx_faits = idx_dispo
        idx_examen = None

    idxs_moyens = [m.start(0) for m in re.finditer(moyens_re, xmldata)] + [idx_dispo]

    idxs_motivations = [m.start(0) for m in re.finditer(motivation_re, xmldata)]
    if len(idxs_motivations) == 0:
        idx_fin_faits = idx_dispo
    else:
        idx_fin_faits = idxs_motivations[0]

    print(idxs_moyens)
    print(idxs_motivations)
    assert len(idxs_moyens) == len(idxs_motivations) + 1

    xml = list()
    xml.append('<?xml version="1.0" encoding="utf-8"?>')
    xml.append('<decision>')

    xml.append('<div class="entete">')
    # entete = jusqu'a rendu le present arret.
    entete = xmldata[:idx_entete]
    xml.append(entete)
    xml.append('</div>')

    if idx_faits != idx_dispo:
        xml.append('<div class="expose">')
        # faits = entre rendu le present arret et faits et procedure
        faits = xmldata[idx_faits:idx_examen if idx_examen is not None else idxs_moyens[0]]
        xml.append(faits)
        xml.append('</div>')
    else:
        xml.append('<div class="motivation">')
        # motivation = entre rendu le present arret et faits et procedure
        motivation = xmldata[idx_entete:idx_fin_faits]
        xml.append(motivation)
        xml.append('</div>')

    if idx_examen is not None:
        # moyens = entre faits et procedure et examen des moyens
        moyens = xmldata[idx_examen:idxs_moyens[0]]
        moyens_split = moyens.split('\n\n')

        if len(moyens_split) <= 2:
            idxs_moyens[0] = idx_examen
        else:
            xml.append('<div class="moyens">')
            xml.append(moyens_split[0] + ('\n\n' + moyens_split[1] if len(moyens_split) > 1 else ''))
            xml.append('</div>')
            if len(moyens_split) > 2:
                xml.append('<div class="motivation">')
                xml.append(moyens_split[2])
                xml.append('</div>')

    for i in range(len(idxs_moyens)-1):
        xml.append('<div class="moyens">')
        moyens = xmldata[idxs_moyens[i]:idxs_motivations[i]]
        xml.append(moyens)
        xml.append('</div>')
        xml.append('<div class="motivation">')
        # motivation = entre reponse de la cour et reponse de la cour
        motivation = xmldata[idxs_motivations[i]:idxs_moyens[i+1]]
        xml.append(motivation)
        xml.append('</div>')
    # else:
    #     xml.append(xmldata[idx_faits:idx_dispo])

    xml.append('<div class="dispositif">')
    # dispositif = par ces motifs, en consequence
    dispositif = xmldata[idx_dispo:]
    xml.append(dispositif)

    xml.append('</div>')

    xml.append('</decision>')

    outdata = '\n'.join(xml)

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata) 

if __name__ == "__main__":
    main()