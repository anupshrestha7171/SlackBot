import spacy

# Load the English language model
nlp = spacy.load('en_core_web_sm')

# Load the scraped text from the file
with open('website_text.txt', 'r') as f:
    text = f.read()

# Process the text with spaCy
doc = nlp(text)

# Extract the sentences
sentences = [sent.text.strip() for sent in doc.sents]
print(sentences)
