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
    #lines = re.split('\n+', textdata)
    #print(textdata.split()[:50])
    date = re.search('([0-3]\d)\s[A-Za-zÀ-ÖØ-öø-ÿ]{4,12}\s(20[0-2]\d)', textdata, re.MULTILINE).group()
    pourvoi = re.search('\d{2}-\d{2}.\d{3}', textdata, re.MULTILINE).group()
    textdata = re.sub('\n{2,}\s{1,}Page\s\d+\s\/\s\d+|(\f).{1,}\n', '\n', textdata)
    textdata = re.sub('\n{3,}|(?<=[;:!?.])\s(?=[A-Z])', '\n\n', textdata)

    index = textdata.find("DU " + date.upper())
    index_split = index + len(date) + 3
    beginning = textdata[:index_split]
    end = re.sub('(?<![;:!?.])\n\n|(?<=M\.)\n\n|(?<=\d\.)\n\n', ' ', textdata[index_split:]) 
    textdata = beginning + '\n\n' + end

    mddata = textdata

    md = list()
    md.append(f"# Pourvoi {pourvoi} du {date}")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

main()