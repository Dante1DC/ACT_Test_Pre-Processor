# Set-Up
This particular repo requires a couple big external packages that need manual set up. First, is Tesseract-OCR. It's a tool used to take images with text and extract that text. This repo interfaces with it via pytesseract, but you must install the Tesseract tool separately. 
Do so here if you have a Windows computer: https://github.com/UB-Mannheim/tesseract/wiki
However, Tesseract works best with images, so this repo uses pdf2image. That requires Poppler, which can be downloaded here: https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.02.0-0

Poppler should be on PATH. 

There's a file not included in this repo called "config.py" where you can configure your Tesseract model to your specifications. You specifically need to use config.py to configure these global variables:
- PATH = "C:\\path\\to\\tesseract\\"
- MODEL = "tesseract.exe"
- DB_NAME = 'db_name'
- DB_USER = 'db_user'
- DB_PASSWORD = 'db_pass'
- DB_HOST = 'host_alias'
- DB_PORT = '0000'
For full functionality. 

# Usage
You must run this code with administrator privileges on Windows. 
In the terminal, you can run `python app.py` and provide several arguments:
- `python app.py ocr "directory"`
    - This reads an entire directory full of images, and turns each into text with the Tesseract OCR
- `python app.py chat "directory"`
    - This reads an entire directory full of text files, and formats them based on an example 
- `python app.py db "directory"`
    - This reads an entire directory full of text files, and uploads them to the database as Question objects
