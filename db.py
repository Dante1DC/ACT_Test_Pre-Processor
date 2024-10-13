import psycopg2
import sys
import config
import os

def db_connection():
    """
    Logs you into the db based on some constants and returns a connection object.
    """
    return psycopg2.connect(database=config.DB_NAME, 
                            user=config.DB_USER, 
                            password=config.DB_PASSWORD, 
                            host=config.DB_HOST,
                            port=config.DB_PORT)

def questions_from_file(file):
    conn = db_connection()
    cur = conn.cursor()

    with open(file, 'r') as f:
        lines = [line.strip() for line in f]

    questions = []
    current_block = []
    for line in lines:
        if line == '-':
            if current_block:
                questions.append(current_block)
                current_block = []
        else:
            current_block.append(line)
    if current_block:
        questions.append(current_block)

    for block_num, block in enumerate(questions, start=1):
        if len(block) < 4:
            print(f"Block {block_num} is too short (less than 4 lines), skipping.")
            continue
        category = block[0]
        reference_text = block[1]
        question_text = block[2]
        choices = []
        choice_id = 0
        for choice_line in block[3:]:
            if not choice_line.strip():
                continue
            if choice_line.startswith('T '):
                is_correct = True
                choice_text = choice_line[2:].strip()
            elif choice_line.startswith('F '):
                is_correct = False
                choice_text = choice_line[2:].strip()
            else:
                print(f"Invalid choice format in block {block_num}: '{choice_line}'")
                continue
            choice_instance = (choice_id, choice_text, is_correct)
            choices.append(choice_instance)
            choice_id += 1

        if not choices:
            print(f"No valid choices found in block {block_num}, skipping.")
            continue

        cur.execute('''INSERT INTO Question (category, reference_text, question_text, choices) VALUES (%s, %s, %s, %s::choice_type[])''',
                    (category, reference_text, question_text, choices))
    conn.commit()
    cur.close()
    conn.close()
    print("Questions added from file.")

def questions_from_dir(dir):
    print(os.listdir(f"{dir}"))
    for txt in os.listdir(f"{dir}"):
        questions_from_file(f"{dir}/{txt}")
