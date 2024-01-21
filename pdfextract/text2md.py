"""
Transforme un document texte issu d'un PDF de la cours de cassation en Markdown.
"""
import argparse
import re

def format_pourvoi(args, textdata):
    #replace several spaces by one
    textdata = re.sub(r' {2,}', ' ', textdata)

    # Split the input file name on '_'
    split_name = args.in_file.split('_')

    # Extract the pourvoi number, day, month, and year
    pourvoi_num = split_name[2]
    day = split_name[3]
    month = split_name[4]
    year = split_name[5].split('.')[0]  # Remove the file extension

    # Map numbers to month names
    month_names = {
        '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
        '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Aout',
        '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Decembre'
    }

    # Convert the month number to a name
    month = month_names.get(month, 'Invalid month')

    # Format the date in text
    date_in_text = f"{day} {month} {year}"
    pourvoi = f"Pourvoi n°{pourvoi_num} du {date_in_text}"

    return pourvoi

def main():
    parser = argparse.ArgumentParser("text2md")
    parser.add_argument('in_file', help="Text file", type=str)
    args = parser.parse_args()

    with open(args.in_file, "r", encoding="utf-8") as f:
        textdata = f.read().replace('\x0c', '').replace('_', '')
        lines = textdata.split('\n')

        for line in lines:
            # if there are more than 4 spaces in a row delete the line
            if re.search(r' {4,}', line):
                textdata = textdata.replace(line, '')

        textdata = re.sub(r'\n(?!\n)', ' ', textdata)
        textdata = re.sub(r'\n\n+', '\n', textdata)

        #remove \n if there is one at the end of the text
        
        # if textdata[-2:] == '\n ':
        #     textdata = textdata[:-2]                  

    mddata = textdata
    md = list() 
    pourvoi = format_pourvoi(args, textdata)
    md.append("#"+pourvoi)
    md.append("")  # Add an empty line after the title
    md.append(mddata)



    outdata = '\n'.join(md) 

    print(args.in_file[:-4] + ".md")

    with open( args.in_file[:-4] + ".md", "w", encoding="utf-8") as f:
        f.write(outdata)

if __name__ == "__main__":
    main()