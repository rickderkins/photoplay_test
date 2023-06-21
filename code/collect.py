import internetarchive as ia
import pathlib as pl

# get list of available volumes for publisher (to be changed)

query = 'creator:Chicago, Photoplay Magazine Publishing Company'

volumes_list = []
for i in ia.search_items(query):
    volumes_list.append(i['identifier'])

# download txts

print('Downloading...')
for vol in volumes_list:
    ia.download(f'{vol}', verbose=True, formats='DjVuTXT', destdir='material/raw')
print('Download completed.')

# clean by removing line breaks

pl.Path('material/cleaned').mkdir(parents=True, exist_ok=True)

for vol in volumes_list:
    readdoc = open(f'material/raw/{vol}/{vol}_djvu.txt', 'r', encoding="utf8").read()
    r_newlines = readdoc.replace('\n', ' ')
    with open(f'material/cleaned/{vol}_cleaned', 'a', encoding="utf8") as f:
        print(r_newlines, file=f)

# clear raw folder?
print('Cleaning completed.')