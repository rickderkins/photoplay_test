import internetarchive as ia
import json
import pathlib as pl
import requests
from bs4 import BeautifulSoup
import os
import nltk

# Set up NLTK
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')

# get list of available volumes for publisher (updated query)
query = 'creator:"Chicago, Photoplay Magazine Publishing Company"'
# volumes_list = []
# for item in ia.search_items(query):
#    volumes_list.append(item['identifier'])

# TESTING: small sample, delete old files
volumes_list = ['pho1314chic', 'photo42chic']
for vol in volumes_list:
    #if os.path.exists(f'material/extracted/hocr_{vol}_extract.txt'):
        #os.remove(f'material/extracted/hocr_{vol}_extract.txt')
    #else:
        #print("The file does not exist")
    if os.path.exists(f'material/cleaned/hocr_{vol}_cleaned.txt'):
        os.remove(f'material/cleaned/hocr_{vol}_cleaned.txt')
    else:
        print("The file does not exist")
    if os.path.exists(f'material/tagged/hocr_{vol}cleaned.txt'):
        os.remove(f'material/tagged/hocr_{vol}_cleaned.txt')
    else:
        print("The file does not exist")

# Retrieve metadata for volumes and save to JSON file
metadata_list = []
print('Retrieving metadata...')
for vol in volumes_list:
    item = ia.get_item(vol)
    metadata = {
        'identifier': vol,
        'title': item.metadata['title'],
        'year': item.metadata['year']
    }
    metadata_list.append(metadata)

# Save metadata to a JSON file
with open('material/metadata.json', 'w') as json_file:
    json.dump(metadata_list, json_file, indent=4)
print('Metadata saved to metadata.json.')

# Download HOCR files
pl.Path('material/hocr').mkdir(parents=True, exist_ok=True)
for vol in volumes_list:
    hocr_file_path = f'material/hocr/{vol}_hocr.html'
    if pl.Path(hocr_file_path).is_file():
        print(f'HOCR file for {vol} already exists. Skipping download.')
    else:
        print(f'Downloading HOCR file for {vol}...')
        url = f'https://archive.org/download/{vol}/{vol}_hocr.html'
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'material/hocr/{vol}_hocr.html', 'w', encoding='utf-8') as file:
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


# Extract captions and text from downloaded HOCR files

pl.Path('material/extracted').mkdir(parents=True, exist_ok=True)
for vol in volumes_list:
    print(f'Extracting text for {vol}...')
    hocr_file_path = f'material/hocr/{vol}_hocr.html'
    extract_file_path = f'material/extracted/hocr_{vol}_extract.txt'
    text = extract_text_from_hocr(hocr_file_path)
    with open(extract_file_path, 'w', encoding='utf-8') as extract_file:
        extract_file.write(' '.join(text))
    print(f'Extracted text for {vol} and saved to {extract_file_path}.')
print('Extraction complete.')

# clean files
pl.Path('material/cleaned').mkdir(parents=True, exist_ok=True)
for vol in volumes_list:
    print(f'Cleaning text for {vol}...')
    clean_file_path = f'material/extracted/hocr_{vol}_extract.txt'
    with open(clean_file_path, 'r', encoding="utf8") as f:
        readdoc = f.read()
        r_newlines = readdoc.replace('- ', '')
        with open(f'material/cleaned/hocr_{vol}_cleaned.txt', 'w', encoding="utf8") as output_file:
            output_file.write(r_newlines)
        print(f'Cleaned text for {vol} and saved to {clean_file_path}.')


# Tokenize and filter the text
def tokenize_and_filter_text(text):
    tokens = nltk.word_tokenize(text)
    tagged_tokens = nltk.pos_tag(tokens)
    filtered_tokens = [token for token, pos in tagged_tokens if
                       pos.startswith('N') or pos.startswith('NNP') or pos.startswith('V') or pos.startswith('J')]
    return ' '.join(filtered_tokens)


# Tokenize and filter files in the "material/cleaned" directory
pl.Path('material/tagged').mkdir(parents=True, exist_ok=True)
cleaned_dir = 'material/cleaned'
tagged_dir = 'material/tagged'

for file_name in pl.Path(cleaned_dir).glob('*.txt'):
    with open(file_name, 'r', encoding='utf-8') as input_file:
        text = input_file.read()
        filtered_text = tokenize_and_filter_text(text)

        tagged_file_path = pl.Path(tagged_dir) / file_name.name
        with open(tagged_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(filtered_text)

        print(f'Filtered text file saved: {tagged_file_path}')

print('Filtering complete.')

# Combine metadata and tagged files into a new JSON file
combined_data = []
for metadata, file_name in zip(metadata_list, pl.Path(tagged_dir).glob('*.txt')):
    with open(file_name, 'r', encoding='utf-8') as input_file:
        tagged_text = input_file.read()
        combined_data.append({
            'metadata': metadata,
            'tagged_text': tagged_text
        })

combined_file_path = 'material/combined.json'
with open(combined_file_path, 'w') as json_file:
    json.dump(combined_data, json_file, indent=4)
print('Combined data saved to combined.json.')
