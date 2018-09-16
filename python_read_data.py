import os 
from multiprocessing import Pool
import logging
import argparse

import pandas as pd
from tqdm import tqdm

from python_pdf_parser.smart_pdf_parser import process_pdf

def parse_multiple_pdfs(file_dir):
    pdf_files = []
    for file in os.listdir(f"{file_dir}"):
        if file.endswith(".pdf"):
            filepath = f"{file_dir}/{file}"
            pdf_files.append(filepath)

    with Pool(2) as p:
        proc_pdfs = list(tqdm(p.imap(process_pdf, pdf_files), desc='Processing PDF files', total=len(pdf_files)))

    # Save file
    pd.DataFrame(proc_pdfs).to_csv('output.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process PDF files')
    parser.add_argument('--file-dir', type=str, help='Directory with multiple PDF files',
                        dest='file_dir', default='sample-data')
    args = parser.parse_args()

    file_dir = args.file_dir
    parse_multiple_pdfs(file_dir)
