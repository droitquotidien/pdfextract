import os

all_files = ['pourvoi_n_21-24.923_30_11_2023','pourvoi_n_22-81.985_13_12_2023','pourvoi_n_22-87.237_13_12_2023','pourvoi_n_23-81.811_13_12_2023','pourvoi_n_23-83.107_13_12_2023']
for file in all_files:
    os.system(f"python text2md.py ../../exemples/{file}.txt ../../exemples/{file}.md")
    print("Text converted to Markdown successfully!")
    os.system(f"python md2xml.py ../../exemples/{file}.md ../../exemples/{file}.xml")
    print("Markdown converted to XML successfully!")