"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

def process_lines(textdata):
    lines = textdata.split('\n')

    processed_lines = []
    current_line = ""

    for line in lines:
        if not line.strip():
            continue

        if re.match(r'^[A-Z]', line) or re.match(r'^\d', line):
            if current_line:
                processed_lines.append(current_line)
            current_line = line
        else:
            current_line += ' ' + line

    if current_line:
        processed_lines.append(current_line)

    result = '\n'.join(processed_lines)
    return result


def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    parser.add_argument('out_file', help="Markdown file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read()

    textdata = re.sub(r'Page \d+ / \d+\n(.*)', '', textdata)
    textdata = re.sub(r'Page \d+ / \d+', '', textdata)

    # deleting the line that starts with smth but ands with a date: 1st approach, a stupid one..
    # unwanted_pourvoi = re.compile(r'^.*?(\d{1,2} [^\s]+ \d{4})$', re.MULTILINE)
    # matches = unwanted_pourvoi.finditer(textdata)
    # unique_dates = set()

    # for match in matches:
    #     date = match.group(1)
    #     if date not in unique_dates:
    #         unique_dates.add(date)
    #     else:
    #         textdata = textdata.replace(match.group(0), '')

    processed_text = process_lines(textdata)

    mddata = processed_text

    # Transform textdata with re here
    # see https://docs.python.org/fr/3/library/re.html


    md = list()
    md.append("# Pourvoi NUM_POURVOI du DATE")
    md.append("")  # Ligne vide
    md.append(mddata)

    outdata = '\n'.join(md) 
    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write(outdata)
