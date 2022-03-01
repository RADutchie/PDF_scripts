import os
import csv
from pathlib import Path
import json

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import io


def create_file_list(path_to_list: str, path_to_docs: str) -> list:
    """Create a list of file paths from a csv input list of files
    INPUT:
    path_to_list: str: full path to csv file.
    path_to_docs: str: path to folder containing .pdf files for text extraction

    RETURNS: list: list of Path objects to documents
    """

    files = []
    with open(path_to_list, newline="") as f:
        read = csv.reader(f)
        for row in read:
            files.append(row[0])
    paths = [Path(path_to_docs + pdf) for pdf in files]
    print(f"list contains {len(files)} files for text extraction")
    return paths


def extract_text(fname: str) -> list:
    """Extract text as strings, page-by-page from a digital pdf document
    INPUT:
    fname: str: path to pdf document

    RETURNS: dict: python dictionary with page number, starting at 1:page text
    """
    # PDFminer.six boiler plate
    output = io.StringIO()
    manager = PDFResourceManager()
    codec = "utf-8"
    converter = TextConverter(manager, output, codec=codec, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    page_text = {}
    with open(fname, "rb") as infile:
        for i, page in enumerate(PDFPage.get_pages(infile, check_extractable=True)):
            interpreter.process_page(page)
            text = output.getvalue()
            no_text = "No extractable text on this page"
            if text == "\f":
                page_text[i + 1] = no_text
            else:
                page_text[i + 1] = text
            output.seek(0)
            output.truncate(0)

    converter.close()
    output.close()
    return page_text


def output_json(text: str) -> str:
    """Function to append new entry to json output file.
    Creates a new file called 'digital_text_extract.json' if it doesn't exist and
    then loads, appends new data and writes the file again.
    This is to allow for progressive writing to the file for large datasets.

    INPUT: str: input dict to add to json file
    RETURNS: None: writes to json file in current working directory
    """

    try:
        with open("digital_text_extract.json") as f:
            data = json.load(f)
    except IOError:
        data = {}

    data.update(text)
    print("writing updated entry to json file")

    with open("digital_text_extract.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def process_multiple_pdfs(path_to_list: str, path_to_docs: str):
    """Function to extract text from multiple digital pgf files and return both a
    json output file and python dictionary containing
    a structure; {report_no: {page_no:text}}
    INPUT:
    path_to_list: str: full path to csv file.
    path_to_docs: str: path to folder containing .pdf files for text extraction

    RETURNS: None: outputs json file to current working directory file path
    """
    path_list = create_file_list(path_to_list, path_to_docs)
    print(f"Json output to: {os.getcwd()}")
    # digital_text = {}
    for pdf in path_list:
        try:
            digital_text = {}
            print(f"extracting text from {pdf.stem}")
            text = extract_text(pdf)
            digital_text[pdf.stem] = text
            output_json(digital_text)

        except Exception as e:
            print(f"Error {e} in file {pdf.stem}")
            continue

    # print(f"Json output to: {os.getcwd()}")
    # with open("digital_text_extract.json", "w") as outfile:
    #    json.dump(digital_text, outfile, indent=' ')


if __name__ == "__main__":
    process_multiple_pdfs(
        "/home/rian/ML_Scripts/PDF_OCR/test_envs.csv",
        "/mnt/hgfs/Shared_VM/Envelopes/",
    )
