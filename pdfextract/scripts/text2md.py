"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re


def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    mddata = textdata

    #finding date and pourvoi number
    date = re.search('([0-3]\d)\s[A-Za-zÀ-ÖØ-öø-ÿ]{4,12}\s(20[0-2]\d)', mddata, re.MULTILINE).group()
    pourvoi = re.search('\d{2}-\d{2}.\d{3}', mddata, re.MULTILINE).group()
    
    #removing pages number
    mddata = re.sub('\n{1,}\s{1,}Page\s\d+\s\/\s\d+|(\f).{1,}|(\f){1,}', ' ', mddata)
   
   #removing unnecessary lines between paragraphs
    mddata = re.sub('\n{3,}|(?<=(!M|!\d)[;:!?.])\s', '\n\n', mddata)

    index = mddata.find("DU " + date.upper())
    index_split = index + len(date) + 3
    beginning = mddata[:index_split]

    find_linebreaks = re.compile("([^\n\s])\n([^\n\s])")
    def repair(matchobj):
        return matchobj.group(1) + " " + matchobj.group(2)
    end = re.sub(find_linebreaks, repair, mddata[index_split:])
    mddata = beginning + '\n\n' + end

    md = list()
    md.append(f"# Pourvoi {pourvoi} du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

main()