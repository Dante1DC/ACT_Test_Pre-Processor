import openai
import os
import tiktoken

import timer

timer = timer.IterationTimer()

openai.api_key = os.getenv('OPENAI_API_KEY')

def format(input, example="example.txt", target="processed_tests", max_tokens=4096, reserved_tokens=1500, overlap_size=200):

    print(input)
    with open(input, 'r', encoding='utf-8') as f:
        input_text = f.read()

    with open(example, 'r', encoding='utf-8') as f:
        example_text = f.read()

    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

    chunk_size = max_tokens - reserved_tokens

    input_tokens = encoding.encode(input_text)

    chunks = []
    start = 0
    while start < len(input_tokens):
        end = start + chunk_size
        chunk = input_tokens[start:end]
        chunks.append(chunk)
        start = end - overlap_size  

    formatted_texts = []
    for idx, chunk_tokens in enumerate(chunks):
        print(f"Processing {len(chunk_tokens)} tokens")
        timer.start(f"Time to complete chunk {idx}/{len(chunks)}")
        chunk_text = encoding.decode(chunk_tokens)
        

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that formats text according to a given example. When you format the text, ensure you only include the reference text, the question text, the category, and the choices. Do not include any additional information. Remove all text that doesn't fit those descriptions, including page numbers, category instructions, etc. No choices should start with A., B., C., D., etc., but should start with either F or T, depending on whether or not the choice is true or false. Fix any spelling mistakes, or strange formatting artefacts."
            },
            {
                "role": "user",
                "content": f"""
    Format the following text to match the style of the example provided.

    ### Example:

    {example_text}

    ### Text to be formatted:

    {chunk_text}

    ### Formatted Text:
    """
            }
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=reserved_tokens, 
            temperature=0,
            top_p=1,
            n=1,
            stop=None,
        )
        
        formatted_chunk = response.choices[0].message['content'].strip()
        formatted_texts.append(formatted_chunk)

    final_formatted_text = ''.join(formatted_texts)

    print(input)

    with open(f'{target}/{os.path.splitext(os.path.basename(input))[0]}_output.txt', 'w', encoding='utf-8') as f:
        f.write(final_formatted_text)


def format_dir(dir, target="processed_tests"):
    for txt in os.listdir(f"{dir}"):
        format(f"{dir}/{os.path.splitext(txt)[0]}.txt")