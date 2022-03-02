
import ocrmypdf
import logging
from pathlib import Path
import time


logging.basicConfig(filename='ocr.log',level=logging.ERROR)

def ocr(file_path, out_path):
    ocrmypdf.ocr(file_path, out_path, output_type='pdf', skip_text=True, skip_big=300, max_image_mpixels=300)#,               clean=True, oversample=200,  deskew=True)


path = Path('/home/rian/Scanned')
out_path = path / "OCR"

scanned = [p.stem for p in out_path.glob('*.pdf')]

pdf_glob1 = [p for p in path.glob('*.pdf') if not (p.stem+"_OCR") in scanned]

pdf_glob = [p for p in path.glob('*.pdf')]

print(len(pdf_glob))
print(len(pdf_glob1))


def ocr_script():
    
    for pdf in pdf_glob1:
        start = time.time()
        fname = str(pdf.stem)+"_OCR.pdf"
        out = out_path / fname
        print('')
        print(fname)
        print('')
        try:
            ocr(pdf,out)
        except Exception as e:
            print(f'something went wrong with {fname}')
            logging.exception(f"{e} occured in {fname}")
            continue
        end = time.time()
        print(f"It took {(end-start)/60} minutes to run file{fname}")

    


if __name__=="__main__":
    ocr_script()

