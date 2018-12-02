from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

temp_docs = [
    "what is your name occurrence internal memory?",
    "which city do you belong to",
    "The reason for storing the occurrence lists outside the trie is to keep the size of the trie data structure "
    "sufficiently small to fit in internal memory.",
    "When multiple keywords are given and the desired output is the pages containing all the given keywords, "
    "we retrieve the occurrence list of each keyword using the trie and return their intersection."
]


# tokenize doc - removes stopwords and punctuations
def tokenizer(sentence):
    swords = stopwords.words('english')
    tokens = []

    for word in word_tokenize(sentence):
        lw = word.lower()

        if word not in punctuation and lw not in swords:
            tokens.append(lw)

    return tokens


# map of word to doc occurrence
def inverse_index(data):
    d_map = defaultdict(list)

    for idx, val in enumerate(data):
        for word in tokenizer(val):
            d_map[word].append(idx)

    return d_map
