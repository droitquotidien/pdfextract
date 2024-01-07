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

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html
    mddata = textdata

    # Find the title for the Md-file
    md_title = ""

    # Search the Pourvoi number
    pourvoi_search = re.compile(r'Pourvoi\s+[Nn]°\s+\w+\s*(\d+-\d+\.\d+)')
    pourvoi = pourvoi_search.search(mddata)

    if pourvoi:
        md_title += "Pourvoi " + pourvoi.group(1)
    else:
        md_title += "POURVOI NUM "
        print("No pourvoi found in the text.")

    # Search the decision data
    date_search = re.compile(r'Audience\s+publique\s+du\s+(\d+\s+\w+\s+\d+)')
    date = date_search.search(textdata)

    if date:
        md_title += " du " + date.group(1)
    else:
        md_title +=  "du DATE"
        print("No date found in the text.")


    # Delete headers and page numbers
    mddata = re.sub(r'Pourvoi.*\n','',mddata)
    mddata = re.sub(r'\n*\s*Page \d+ \/ \d+.*\n','',mddata)
    mddata = re.sub(r'\x0c.*\n','',mddata)

    # Reconstruct continuous paragraphs
    paragraphs = re.split(r'\n\n+',mddata)
    Reconstruct_para = '\n\n'.join(paragraphs)

    # Delete newline in same paragraph.
    Reconstruct_para = re.sub(r'\n(?!\s*\n)','',Reconstruct_para)

    # Use single newline between paragraphs.
    Reconstruct_para = re.sub(r'\n','\n\n',Reconstruct_para)

    md = list()
    md.append("# "+md_title)
    md.append("")  # Ligne vide
    md.append(Reconstruct_para)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

