import config

from PIL import Image, ImageOps

from pdf2image import convert_from_path

import pytesseract

pytesseract.pytesseract.tesseract_cmd = config.PATH + config.MODEL

def extract(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    text = ""
    print("begin\n")
    for page_num, page in enumerate(pages, start=1):
        print("so far" + text)
        # Extract text using pytesseract
        page_text = pytesseract.image_to_string(page)
        text += f"Page {page_num}:\n{page_text}\n\n"
        
    return text

# gotta invert? ImageOps.invert()
print("oh brother: " + pytesseract.image_to_string(Image.open('test.png')))
print(extract("ACT 200112 Form 58E.pdf"))