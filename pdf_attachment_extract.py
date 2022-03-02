#!/usr/bin/env python3

import os
import PyPDF2
from PyPDF2.utils import PdfReadError
import csv
from tqdm import tqdm

directory = "/home/rian/Python_scripts/env_s3_downloader/envelope_pdf"
file_errors = []
# Original code from https://gist.github.com/kevinl95/29a9e18d474eb6e23372074deff2df38
def getAttachments(reader):
    """
    Retrieves the file attachments of the PDF as a dictionary of file names
    and the file data as a bytestring.
    :return: dictionary of filenames and bytestrings
    """
    try:
        catalog = reader.trailer["/Root"]
        fileNames = catalog["/Names"]["/EmbeddedFiles"]["/Names"]
        attachments = {}
        for f in fileNames:
            if isinstance(f, str):
                name = f
                dataIndex = fileNames.index(f) + 1
                fDict = fileNames[dataIndex].getObject()
                fData = fDict["/EF"]["/F"].getData()
                attachments[name] = fData

        return attachments
    except:
        print("No attachments in file")
        attachments = {}
        return attachments


# Loop through all pdf files in directory
for root, direc, files in os.walk(directory):
    print("working on files")
    for filename in tqdm(files):
        if filename.endswith(".pdf"):
            print(filename)
            with open(os.path.join(root, filename), "rb") as handler:
                try:
                    reader = PyPDF2.PdfFileReader(handler)
                    dictionary = getAttachments(reader)
                except (TypeError, PdfReadError):
                    file_errors.append([handler])
                    continue
                # print(dictionary)
                for fName, fData in dictionary.items():
                    newFile = os.path.join(
                        root, "attachments", os.path.splitext(filename)[0], fName
                    )
                    os.makedirs(os.path.dirname(newFile), exist_ok=True)
                    with open(newFile, "wb") as outfile:
                        outfile.write(fData)

    print("working on sub-directories")
    for filename in tqdm(direc):
        if filename.endswith(".pdf"):
            print(filename)
            with open(os.path.join(root, filename), "rb") as handler:
                try:
                    reader = PyPDF2.PdfFileReader(handler)
                    dictionary = getAttachments(reader)
                except (TypeError, PdfReadError):
                    file_errors.append([handler])
                    continue
                # print(dictionary)
                for fName, fData in dictionary.items():
                    newFile = os.path.join(
                        root, "attachments", os.path.splitext(filename)[0], fName
                    )
                    os.makedirs(os.path.dirname(newFile), exist_ok=True)
                    with open(newFile, "wb") as outfile:
                        outfile.write(fData)

with open(os.path.join(os.getcwd(), "file_errors.csv"), "w") as e:
    writer = csv.writer(e)
    writer.writerows(file_errors)
