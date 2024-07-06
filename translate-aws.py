# import boto3

# translate = boto3.client('translate', region_name='us-east-1')

# def translate_text(text, source_lang='en', target_lang='he'):
#     result = translate.translate_text(Text=text, 
#                                       SourceLanguageCode=source_lang, 
#                                       TargetLanguageCode=target_lang)
#     return result['TranslatedText']

# # Example of translating a single sentence
# translated_text = translate_text("Hello, world!")
# print(translated_text)


import boto3
import json

# Initialize the Translate client
translate = boto3.client('translate', region_name='us-east-1')

def translate_text(text, source_lang='en', target_lang='he'):
    """Translate text from source language to target language."""
    result = translate.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return result['TranslatedText']

def translate_jsonl(input_path, output_path):
    """Translate the content of a JSONL file and save the result to a new JSONL file."""
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            item = json.loads(line)
            # Translate the 'premise' and 'hypothesis' fields
            item['premise'] = translate_text(item['premise'])
            item['hypothesis'] = translate_text(item['hypothesis'])
            # Write the translated item to the output file
            outfile.write(json.dumps(item, ensure_ascii=False) + '\n')
            break

def load_jsonl(file_path):
    """Load a JSONL file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Paths for input and output files
input_file_path = './data/src/train.jsonl'
output_file_path = './data/dest/train_translated.jsonl'

# Translate the JSONL file
translate_jsonl(input_file_path, output_file_path)

# Confirm the translation by loading and displaying the translated content
translated_data = load_jsonl(output_file_path)
print(translated_data[:2])
