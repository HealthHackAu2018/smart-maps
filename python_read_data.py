import os 
from python_pdf_parser.smart_pdf_parser import process_pdf
import pandas as pd

if __name__ == '__main__':
    proc_pdfs = []
    for file in os.listdir("sample-data/"):
        if file.endswith(".pdf"):
            print(file)
            filepath = f"sample-data/{file}"
            proc_pdfs.append(process_pdf(filepath))

    # Save file
    pd.DataFrame(proc_pdfs).to_csv('output.csv', index=False)
