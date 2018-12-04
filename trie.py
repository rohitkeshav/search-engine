from collections import defaultdict
from string import punctuation

from nltk import word_tokenize
from nltk.corpus import stopwords

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


class Node:

    def __init__(self):
        self.next = defaultdict(Node)
        self.is_end = False
        self.occurrences = []


class Trie:

    def __init__(self):
        self.root = Node()
        self.v_map = inverse_index(temp_docs)

    def insert(self, word):
        if self.search(word):
            print(f'{word} already exists')

            return

        n_node = self.root

        for char in word:
            n_node = n_node.next[char]

        n_node.is_end = True

        # added this line
        n_node.occurrences.extend(self.v_map[word.lower()])

    def search(self, word):
        n_node = self.root

        # changed word instead of word.lower()
        for char in word.lower():
            n_node = n_node.next[char]

        # return n_node.is_end
        return n_node.occurrences


T = Trie()
T.insert('sufficiently')
T.insert('keshav')
T.insert('occurrence')
T.insert('wassup')
T.insert('doom')
T.insert('containing')


print(T.search('containing'))
print(T.search('mc'))
print(T.search('Occurrence'))
print(T.search('doo'))
