import internetarchive as ia
import os
from pathlib import Path

volumes_list = range(40, 50)

# download volume txts

for vol in volumes_list:
    ia.download(f'photo{vol}chic', verbose=True, formats='DjVuTXT', destdir='material/raw')

list_raw = list(os.listdir('material/raw'))
print(list_raw)

# clean them removing line breaks

for vol_raw in list_raw:
    Path('/material/cleaned').mkdir(parents=True, exist_ok=True)
    # readdoc = open(f'material/raw/photo{vol}chic/photo{vol}chic_djvu.txt', 'r').read()
    readdoc = open(f'material/raw/{vol_raw}/{vol_raw}_djvu.txt', 'r').read()
    r_newlines = readdoc.replace('\n', ' ')
    # close('material/raw/photo40chic/photo40chic_djvu.txt', 'r')
    with open(f'material/cleaned/{vol_raw}_cleaned', 'a') as f:
        print(r_newlines, file=f)

print('Download and cleaning completed.')