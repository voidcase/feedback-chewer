import re

def build_wordset(dataset, text_fields):
    wordset = set()
    for row in dataset:
        for field in text_fields:
            words = re.findall('\w+', row[field])
            for word in words:
                wordset.add(word.lower())
    return wordset
