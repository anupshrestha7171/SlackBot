import spacy

# Load the Spacy English language model
nlp = spacy.load('en_core_web_sm')

# Read the text content from the file
with open('website_text.txt', 'r', encoding='utf-8') as f:
    website_text = f.read()

# Process the text content with Spacy
doc = nlp(website_text)

# Define the relationship labels to extract
relation_labels = ['nsubj', 'nsubjpass', 'dobj', 'pobj', 'attr']

# Iterate over the sentences and extract the subject, object, and relationship
for sentence in doc.sents:
    subject = None
    relation = None
    obj = None
    for token in sentence:
        # If the token is a subject or object
        if token.dep_ in ['nsubj', 'nsubjpass', 'dobj', 'pobj', 'attr']:
            # If the token has a modifier, add the modifier to the entity
            if token.head.pos_ == 'ADJ':
                if token.head.head.dep_ == 'nsubj':
                    subject = token.head.text + ' ' + token.text if subject is None else subject + ' ' + token.text
                elif token.head.head.dep_ == 'dobj' or token.head.head.dep_ == 'pobj':
                    obj = token.head.text + ' ' + token.text if obj is None else obj + ' ' + token.text
            # If the token has no modifier, use the token as the entity
            else:
                if token.dep_ in ['nsubj', 'nsubjpass']:
                    subject = token.text
                elif token.dep_ in ['dobj', 'pobj', 'attr']:
                    obj = token.text
        # If the token is a relationship
        elif token.dep_ == 'ROOT':
            relation = token.text

    # Print the extracted subject, object, and relationship
    if subject is not None and relation is not None and obj is not None:
        print('Subject:', subject)
        print('Relationship:', relation)
        print('Object:', obj)
        print('---')
