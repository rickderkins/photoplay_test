import internetarchive as ia

volumes_list = range(40, 50)

# download volume txts

for vol in volumes_list:
  ia.download(f'photo{vol}chic', verbose=True, formats='DjVuTXT', destdir='material/raw')
  readdoc = open(f'material/raw/photo{vol}chic/photo{vol}chic_djvu.txt', 'r').read()
  r_newlines = readdoc.replace('\n',' ')
  # close('material/photo40chic/photo40chic_djvu.txt', 'r')
  with open(f'material/cleaned/photo{vol}chic_cleaned', 'a') as f:
    print(r_newlines, file=f)