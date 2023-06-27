import internetarchive as ia
import json
import pathlib as pl
import requests
from bs4 import BeautifulSoup
import nltk
import spacy

# Set up NLTK
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')

# create directories and set path variables
pl.Path('material/hocr').mkdir(parents=True, exist_ok=True)
pl.Path('material/ner').mkdir(parents=True, exist_ok=True)
cleaned_dir = 'material/cleaned'
# ner_dir = 'material/ner'

# get list of available volumes for publisher (updated query)
query = 'creator:"Chicago, Photoplay Magazine Publishing Company"'
# volumes_list = []
# for item in ia.search_items(query):
#    volumes_list.append(item['identifier'])

# TESTING: small sample, delete old files
volumes_list = ['pho1314chic', 'photo42chic', 'photoplay51chic', 'photoplayvolume222chic']

# Retrieve metadata for volumes
metadata_list = []
print('Retrieving metadata...')
for vol in volumes_list:
    item = ia.get_item(vol)
    metadata = {
        'identifier': item.metadata.get('identifier', 'N/A'),
        'title': item.metadata.get('title', 'N/A'),
        'journal-title': item.metadata.get('journal-title', 'N/A'),
        'volume': item.metadata.get('volume', 'N/A'),
        'year': item.metadata.get('year', 'N/A'),
        'date-string': item.metadata.get('date-string', 'N/A'),
        'publisher': item.metadata.get('creator', 'N/A')
    }
    metadata_list.append(metadata)

# Save metadata to a JSON file
with open('material/metadata.json', 'w') as json_file:
    json.dump(metadata_list, json_file, indent=4)
print('Metadata saved to metadata.json.')

# Download HOCR files
for vol in volumes_list:
    hocr_file_path = f'material/hocr/{vol}_hocr.html'
    if pl.Path(hocr_file_path).is_file():
        print(f'HOCR file for {vol} already exists. Skipping download.')
    else:
        print(f'Downloading HOCR file for {vol}...')
        url = f'https://archive.org/download/{vol}/{vol}_hocr.html'
        response = requests.get(url)
        if response.status_code == 200:
            with open(hocr_file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f'Downloaded HOCR file for {vol}.')
        else:
            print(f'Failed to download HOCR file for {vol}')
print('HOCR download completed.')


# Extract text from HOCR file
def extract_text_from_hocr(hocr_file_path):
    with open(hocr_file_path, 'r', encoding='utf-8') as hocr_file:
        soup = BeautifulSoup(hocr_file, 'html.parser')
        text = [word.get_text().strip() for word in soup.select('.ocrx_word')]
    return text


# Clean text
def clean_text(text):
    r_newlines = text.replace('- ', '')
    r_replaced = r_newlines.replace("\u25a0", " ")  # Replace "\u25a0" with a space
    r_replaced = r_replaced.replace("\u2014", " ")  # Replace "\u2014" with a space
    return r_replaced

"""
# Tokenize and filter the text
def tokenize_and_filter_text(text):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    filtered_tokens = [token for (token, pos) in pos_tags if pos.startswith(('NN', 'VB', 'JJ'))]
    return filtered_tokens


# Load the spacy NER model
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 4000000

# Perform Named Entity Recognition (NER) on text
def perform_ner(text):
    doc = nlp(text)
    ner_results = []
    for ent in doc.ents:
        ner_result = {
            'Text': ent.text,
            'Label': ent.label_
        }
        ner_results.append(ner_result)
    return ner_results
"""

# Combine metadata, filtered text, and NER results
combined_data = []
for metadata in metadata_list:
    identifier = metadata['identifier']
    cleaned_text_path = f'{cleaned_dir}/{identifier}_cleaned.txt'
    # filtered_text_path = f'{cleaned_dir}/{identifier}_filtered.txt'
    # ner_file_path = f'{ner_dir}/{identifier}_ner.json'

    print(f'Processing {identifier}...')

    # Extract text from HOCR file
    hocr_file_path = f'material/hocr/{identifier}_hocr.html'
    hocr_text = extract_text_from_hocr(hocr_file_path)

    # Clean text
    cleaned_text = clean_text(' '.join(hocr_text))
    metadata['text'] = cleaned_text

    # Tokenize and filter the text
    # filtered_text = tokenize_and_filter_text(cleaned_text)
    # metadata['filtered_text'] = filtered_text

    # Perform NER on the cleaned text # maybe change to filtered text?
    # ner_results = perform_ner(cleaned_text)
    # metadata['named_entities'] = ner_results

    combined_data.append(metadata)

# Save combined data to combined.json
with open('material/combined.json', 'w') as json_file:
    json.dump(combined_data, json_file, indent=4)

print('Processing completed. Combined data saved to combined.json.')
