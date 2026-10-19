import spacy

_nlp = spacy.load("en_core_web_sm")

def parse(text: str):
    return _nlp(text)