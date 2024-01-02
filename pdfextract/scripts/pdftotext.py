import PyPDF2
import sys


def main(pdf_path, txt_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        textdata = ""
        for page_num in range(len(reader.pages)):
            textdata += reader.pages[page_num].extract_text()
    with open(txt_path, "w", encoding="utf-8") as output:
        output.write(textdata)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_text.py [pdf_path] [txt_path]")
    else:
        pdf_path = sys.argv[1]
        txt_path = sys.argv[2]
        main(pdf_path, txt_path)