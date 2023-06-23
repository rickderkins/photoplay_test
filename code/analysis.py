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

# Read combined.csv into a dataframe
combined_file_path = 'material/combined.csv'
df = pd.read_csv(combined_file_path)

# Display the dataframe
print(df)
