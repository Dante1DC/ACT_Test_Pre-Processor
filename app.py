import ocr
import db
import chat
import os
import sys

print(sys.argv[1])
print(sys.argv[2])

try:
    match sys.argv[1]:
        case "ocr":
            if len(sys.argv) > 2:
                ocr.process_dir(str(sys.argv[2]))
            else:
                print("Please provide a directory to process.")
        case "chat":
            if len(sys.argv) > 2:
                chat.format_dir(str(sys.argv[2]))
            else:
                print("Please provide a directory to format.")
        case "db":
            if len(sys.argv) > 2:
                db.questions_from_dir(str(sys.argv[2]))
            else:
                print("Please provide a file to import.")
except IndexError:
    print("oops.")
    sys.exit(1)
