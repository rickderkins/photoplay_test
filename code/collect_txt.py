import internetarchive as ia
import json
import pathlib as pl

# get list of available volumes for publisher (updated query)

query = 'creator:"Chicago, Photoplay Magazine Publishing Company"'

volumes_list = []
for item in ia.search_items(query):
    volumes_list.append(item['identifier'])

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
with open('../material/metadata.json', 'w') as json_file:
    json.dump(metadata_list, json_file, indent=4)
print('Metadata saved to metadata.json.')

# download txts directly to 'material/raw' directory

print('Downloading...')
for vol in volumes_list:
    ia.download(vol, verbose=True, formats='DjVuTXT', destdir='material/raw')
print('Download completed.')

# clean by removing line breaks

pl.Path('../material/cleaned').mkdir(parents=True, exist_ok=True)

for vol in volumes_list:
    with open(f'material/raw/{vol}/{vol}_djvu.txt', 'r', encoding="utf8") as f:
        readdoc = f.read()
        r_newlines = readdoc.replace('\n', ' ')
        with open(f'material/cleaned/{vol}_cleaned.txt', 'w', encoding="utf8") as output_file:
            output_file.write(r_newlines)

# clear raw folder?
print('Cleaning completed.')