"""
check_digital_pdf

Script that takes a folder of pdf files and parses
thorugh each one page by page trying to identify if
that page contains digital text or is a scanned
image.
"""

import time
import csv
import sys
from pathlib import Path
from pdfminer.pdfpage import PDFPage
from contextlib import suppress


def find_pdf_serchable_pages(fname):
    """Function to parse a pdf doc page by page to
    identify if that page is digitally searchable or an image.
    A document is classed as serchable if it has more than 10%
    of its pages as digital.

    INPUT: str: path to file folder
    RETURNS: str: str of seachable document name and writes
            to two csv files, digital_pdf_list.csv and
            non_digital_pdf_list.csv
    """

    searchable_pages = []
    non_searchable_pages = []
    page_num = 0

    with suppress(ValueError, TypeError):
        with open(fname, "rb") as infile:
            for page in PDFPage.get_pages(infile):
                page_num += 1
                if "Font" in page.resources.keys():
                    searchable_pages.append(page_num)
                else:
                    non_searchable_pages.append(page_num)

    if page_num > 0:
        if len(searchable_pages) == 0:
            print(
                f"Document '{fname.name}' has {page_num} pages."
                f" Complete doc is non-searchable"
            )
            with open("non_digital_pdf_list.csv", "a+", newline="") as f:
                write = csv.writer(f)
                write.writerow([fname.name])
            return None
        elif len(non_searchable_pages) == 0:
            print(
                f"Document '{fname.name}' has {page_num} pages."
                f" Complete doc is searchable"
            )
            with open("digital_pdf_list.csv", "a+", newline="") as f:
                write = csv.writer(f)
                write.writerow([fname.name])
            return fname.name
        else:
            print(
                f"Document '{fname.name}' is partially searchable. It has: \
                {len(searchable_pages)} searchable pages and: \
                {len(non_searchable_pages)} non searchable pages"
            )
            if len(searchable_pages) / page_num > 0.1:
                with open("digital_pdf_list.csv", "a+", newline="") as f:
                    write = csv.writer(f)
                    write.writerow([fname.name])
                return fname.name
            else:
                with open("non_digital_pdf_list.csv", "a+", newline="") as f:
                    write = csv.writer(f)
                    write.writerow([fname.name])
                return None

    else:
        print(f"{fname} is not a valid pdf doc")


def get_digital_pdfs(path):
    """Function to parse a directory of pdf files and return a list of digital
    documents, and csv lists of digital and non digital documents.

    INPUT: str: path to folder
    RETURNS: list: a list of searchable document file names
    """

    path = Path(path)
    pdf_glob = [p for p in path.glob("*.pdf")]
    print(f"There are {len(pdf_glob)} files to process")

    start = time.time()
    digital_pdfs = list(
        filter(None, [find_pdf_serchable_pages(pdf) for pdf in pdf_glob])
    )
    end = time.time()
    print("\n")
    print(f"Took {(end-start)/60} minutes to process {len(pdf_glob)} files")
    return digital_pdfs


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_digital_pdfs(sys.argv[1])
    else:
        raise SystemExit("usage: python3 check_digital_pdf.py <'path_to_folder'>")
