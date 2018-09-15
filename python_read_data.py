import os 
from multiprocessing import Pool
import logging

import pandas as pd
from tqdm import tqdm

from python_pdf_parser.smart_pdf_parser import process_pdf


if __name__ == '__main__':
    pdf_files = []
    for file in os.listdir("sample-data/"):
        if file.endswith(".pdf"):
            filepath = f"sample-data/{file}"
            pdf_files.append(filepath)

    with Pool(4) as p:
        proc_pdfs = list(tqdm(p.imap(process_pdf, pdf_files), desc='Processing PDF files', total=len(pdf_files)))

    # Save file
    pd.DataFrame(proc_pdfs).to_csv('output.csv', index=False)
