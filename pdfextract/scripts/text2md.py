"""
Transforme un document texte issu d'un PDF de la cour de cassation en Markdown.
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

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata = textdata

    md = list()
    NUM_POURVOI = re.search('(?<=Pourvoi N°)([0-9]|-)+.[0-9]+',mddata).group(0)
    DATE = re.search('(?<=DU )[0-9]+ [a-zA-ZéÉèÈàÀûÛ]+ [0-9]+',mddata).group(0)
    title = "# Pourvoi " + NUM_POURVOI + " du " + DATE
    md.append(title)
    md.append("")
    linestext = re.split('\n+',mddata)
    for line in linestext :
        test = re.search('^[^ \t\n\r\f\v\x0c]',line)
        try :
            if test.group(0)!=0:
                md.append(line)
        except:
            pass
    i = 1
    round = 0
    max = len(md)
    while round <= max:
        try:
            if re.search('^([a-z]|([0-9]+ [a-z]))',md[i]).group(0)!=0:
                md[i-1] = md[i-1] + " " + md[i]
                md.remove(md[i])
        except:
            i += 1
        round += 1
    for index, line in enumerate(md):
        md[index] = line + '\n'

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
