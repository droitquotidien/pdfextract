import os

files = ['pourvoi_n_21-24.923_30_11_2023','pourvoi_n_22-81.985_13_12_2023','pourvoi_n_22-87.237_13_12_2023','pourvoi_n_23-81.811_13_12_2023','pourvoi_n_23-83.107_13_12_2023']
for file in files:
    os.system(r'python .\pdfextract\scripts\text2md.py ./exemples/'+file+r'.txt ./exemples/'+file+r'.md')
    os.system(r'python .\pdfextract\scripts\md2xml.py ./exemples/'+file+r'.md ./exemples/'+file+r'.xml')