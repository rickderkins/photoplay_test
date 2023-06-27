import spacy
import pandas as pd

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')
nlp.max_length = 4000000


# This function filters out the stop words and the punctuation. It also applies Lemmatization
def filter_and_lemmatize(document):
    filtered_tokens = []
    for token in document:
        if not token.is_stop and not token.is_punct and token.text != '\n':
            filtered_tokens.append(token)
    lemmas = [token.lemma_ for token in filtered_tokens]
    return lemmas


# Filter tokens based on their POS
def filter_pos_tags(document):
    allowed_postags = ['NOUN', 'ADJ', 'ADV']
    return [tok.text for tok in document if tok.pos_ in allowed_postags]


# Function to perform NER on a list of tokens
def perform_ner(tokens):
    text = ' '.join(tokens)  # Convert list of tokens to a string
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


# Read the JSON file into a pandas DataFrame
combined_file_path = 'material/combined.json'
print('Reading JSON file...')
df = pd.read_json(combined_file_path)

# Process the text and save the results
print('Processing texts...')
doc = nlp(df['text'][0])
data = []
for token in doc:
    data.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop])

# Create the pandas DataFrame for token details
tokens_details = pd.DataFrame(data, columns=['Text', 'Lemma', 'coarse POS', 'fine POS', 'Dependency', 'Shape', 'is Alpha', 'is Stop'])

# Apply spaCy model to all documents
print('Applying spaCy model to all documents...')
df['spacy_document'] = df['text'].apply(nlp)

# Process files: Filter and lemmatize, POS tag, NER
print('Processing files...')
df['clean_text'] = df['spacy_document'].apply(filter_and_lemmatize)
print(df)
df['pos_filtered_text'] = df['spacy_document'].apply(filter_pos_tags)
df['ner'] = df['pos_filtered_text'].apply(perform_ner)

# Print the DataFrame
print('DataFrame:')
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df)

# Save the DataFrame to a new JSON file
output_file_path = 'material/data.json'
df['spacy_document'] = df['spacy_document'].apply(lambda doc: [{'text': token.text,
                                                                'lemma': token.lemma_,
                                                                'pos': token.pos_} for token in doc])

df.to_json(output_file_path, orient='records')

print('DataFrame saved to:', output_file_path)

