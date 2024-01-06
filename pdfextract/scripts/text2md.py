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
    # Get date and pourvoi number
    pattern_date = r"(\d+\s+\D+\s+\d{4})"
    pattern_pourvoi = r"n°\s+(\D+\s+\d{2}\-\d{2}.*)\n"
    DATE = re.findall(pattern_date, mddata)[0]
    NUM_POURVOI = re.findall(pattern_pourvoi, mddata)[0]
    
    # Delete lines composed with _ only
    mddata = re.sub(r"^_+$", r"", mddata, flags=re.MULTILINE)
    
    # Remove footers
    mddata = re.sub(r"\n\s*Page\s*\d+\s*/\s*\d+\n*\s*", r"\n", mddata)
    # Remove headers
    mddata = re.sub("\n\s*Pourvoi\s*N°.*{}\n".format(DATE), r"\n", mddata)
    
    # Remove empty lines at the beginning of the document (if there are any)
    mddata = re.sub(r"^\s*\n", r"", mddata)
    
    # Keep only one blank line between paragraphs
    mddata = re.sub(r"\n\s*\n", r"\n\n", mddata)

    # Remove return to line in paragraphs but keep them at the end of paragraphs
    mddata = re.sub(r"(?<!\n)\n(?!\n)", r" ", mddata)


    md = list()
    md.append("# Pourvoi {} du {}".format(NUM_POURVOI, DATE))
    md.append("")  # Ligne vide



    md.append(mddata)


    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == '__main__':
    main() 
