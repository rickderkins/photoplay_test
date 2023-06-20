import internetarchive as ia
import pathlib as pl

# get list of available volumes for publisher

volumes_list = []
for i in ia.search_items('creator:Chicago, Photoplay Magazine Publishing Company'):
    volumes_list.append(i['identifier'])
# print(volumes_list)

# download txts

print('Downloading...')
for vol in volumes_list:
    ia.download(f'{vol}', verbose=False, formats='DjVuTXT', destdir='material/raw')
    print(f'{vol} downloaded')
print('Download completed.')

# clean by removing line breaks

pl.Path('material/cleaned').mkdir(parents=True, exist_ok=True)

for vol in volumes_list:
    readdoc = open(f'material/raw/{vol}/{vol}_djvu.txt', 'r', encoding="utf8").read()
    r_newlines = readdoc.replace('\n', ' ')
    with open(f'material/cleaned/{vol}_cleaned', 'a', encoding="utf8") as f:
        print(r_newlines, file=f)

print('Cleaning completed.')
