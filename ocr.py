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

def pdf_to_text_low_memory(pdf_path):
    text = ""
    # Get the total number of pages
    from pdf2image import pdfinfo_from_path
    info = pdfinfo_from_path(pdf_path)
    total_pages = info["Pages"]
    # Process each page individually
    for page_num in range(1, total_pages + 1):
        pages = convert_from_path(
            pdf_path,
            dpi=150,  # Reduced DPI
            first_page=page_num,
            last_page=page_num
        )
        if pages:
            page = pages[0]
            page_text = pytesseract.image_to_string(page)
            print(page_text)
            text += f"Page {page_num}:\n{page_text}\n\n"
    return text

def process_dir(dir, target="cleaned_tests", low_memory=True):
    for pdf in os.listdir({dir}):
        with open(f"{target}/{os.path.splitext(pdf)[0]}.txt", 'w', encoding='utf-8') as file:
            if low_memory:
                file.write(pdf_to_text_low_memory(f"{dir}/{pdf}"))
            else:
                file.write(pdf_to_text(f"{dir}/{pdf}"))

# # gotta invert? ImageOps.invert()
# print("oh brother: " + pytesseract.image_to_string(Image.open('test.png')))
# print(extract("ACT 200112 Form 58E.pdf"))

# save_pdf_as_images("./raw_tests/ACT 200112 Form 58E.pdf", "cleaned_tests", name=1)
