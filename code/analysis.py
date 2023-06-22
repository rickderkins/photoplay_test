import internetarchive as ia
import json
import pathlib as pl
import requests
from bs4 import BeautifulSoup
import os
import nltk
import csv
import matplotlib
import numpy
import openai

import pandas as pd
import collect_hocr

"""
if __name__ == "__main__":
    ans = collect_hocr.func(2, 3)
    print(ans)
"""


# Read combined.csv into a dataframe
combined_file_path = 'material/combined.csv'
df = pd.read_csv(combined_file_path)

# Display the dataframe
print(df)
