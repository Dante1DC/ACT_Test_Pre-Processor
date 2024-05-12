import config

import os 

from PIL import Image, ImageOps

from pdf2image import convert_from_path

import pytesseract

pytesseract.pytesseract.tesseract_cmd = config.PATH + config.MODEL

def save_pdf_as_images(pdf_path, out, **kwargs):
    pages = convert_from_path(pdf_path, dpi=300)
    for index, page in enumerate(pages):
        if "name" in kwargs:
            img_path = os.path.join(out, f'{kwargs["name"]}_{index+1}.png')
        else: 
            img_path = os.path.join(out, f"page_{index+1}.png")
        page.save(img_path, "PNG")

def folder_to_text(folder_path):
    text = ""
    for file in os.listdir(folder_path):
        if file.endswith(".png"):
            page_text = pytesseract.image_to_string(Image.open(os.path.join(folder_path, file)))
            text += f"Page {file.split('_')[1].split('.')[0]}:\n{page_text}\n\n"
    return text

def pdf_to_text(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    text = ""
    for page_num, page in enumerate(pages, start=1):
        page_text = pytesseract.image_to_string(page)
        text += f"Page {page_num}:\n{page_text}\n\n"   
    return text

# # gotta invert? ImageOps.invert()
# print("oh brother: " + pytesseract.image_to_string(Image.open('test.png')))
# print(extract("ACT 200112 Form 58E.pdf"))

# save_pdf_as_images("./raw_tests/ACT 200112 Form 58E.pdf", "cleaned_tests", name=1)
