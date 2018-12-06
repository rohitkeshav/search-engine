from collections import defaultdict, Counter
from itertools import chain

from string import punctuation

from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

import requests


MAIN_MAP = defaultdict(list)


def clean_html(html_data):
    """
        Clean html
    """
    soup = BeautifulSoup(html_data, 'lxml')

    # remove all javascript and stylesheet code
    for ss_tag in soup(["script", "style"]):
        ss_tag.extract()

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())

    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def hit_urls(url_list):

    return [clean_html(requests.get(url).text) for url in url_list]


# tokenize doc - removes stopwords and punctuations
def tokenizer(sentence):
    swords = stopwords.words('english')
    tokens = []

    for word in word_tokenize(sentence):
        lw = word.lower()

        if word not in punctuation and lw not in swords and word != '':
            tokens.append(lw)

    return tokens


# map of word to doc occurrence
def inverse_index(data):
    d_map = defaultdict(list)

    for idx, val in enumerate(data):
        for word in tokenizer(val):
            d_map[word].append(idx)

    return d_map


# compressed trie nodes
class Node:

    def __init__(self, children=None, is_leaf=False, visited=0):
        if children is None:
            self.children = {}
        else:
            self.children = children

        self.is_leaf = is_leaf
        self.visited = visited
        self.occurrences = []


# compressed trie implementation
# add node to the trie
def add(root, name):
    node = root

    node.visited += 1

    for key in node.children:
        pre, _key, _name = extract_prefix(key, name)

        if _key == '':
            # there is a match of a part of the key
            child = node.children[key]
            return add(child, _name)

        if pre != '':
            child = node.children[key]

            # need to split
            _node = Node(children={_key: child}, visited=child.visited)

            del node.children[key]
            node.children[pre] = _node

            return add(_node, _name)

    node.children[name] = Node(is_leaf=True, visited=1)

    # add here
    # print(MAIN_MAP[name.lower()])
    # import time
    # time.sleep(10)

    # node.children[name].occurrences.extend(MAIN_MAP[name.lower()])


# find word in trie
def find(root, name):
    node = root

    for key in node.children:

        pre, _key, _name = extract_prefix(key, name)

        if _name == '':
                return node.children[key].visited

        if _key == '':
            return find(node.children[key], _name)

    return 0


def extract_prefix(str1, str2):
    n = 0
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            break
        n += 1
    return str1[:n], str1[n:], str2[n:]


def ranking(search_result):
    # simple function to rank the output
    check = chain(*[search_result[k] for k in search_result])

    cobj = Counter(check)

    return [top[0] for top in cobj.most_common(n=5)]


def run(sq):
    url_list = [
        "https://mitpress.mit.edu/blog/brain-awareness-week-digital-mind",
        "https://mitpress.mit.edu/blog/elections-and-patriotism-midcentury-vinyl",
        "https://mitpress.mit.edu/blog/happy-25th-birthday-hal",
        "https://mitpress.mit.edu/blog/how-entrepreneurship-good-economic-growth",
        "https://mitpress.mit.edu/blog/video-games-around-world",
        "https://mitpress.mit.edu/blog/transgender-day-remembrance-celebrating-dr-ben-barres"
    ]

    data = inverse_index(hit_urls(url_list))

    # update main map with words from the html pages, with their occurrences
    MAIN_MAP.update(data)

    query = tokenizer(sq)

    root = Node()
    ignore = ['©', '—', '’', '“', '”', "''"]

    for word in MAIN_MAP:
        if word not in ignore:
            add(root, word)

    retval = {}

    # search the compressed trie using the find function
    for key in query:
        if find(root, key):
            retval.update({key: MAIN_MAP[key]})

    resulting_idx = ranking(retval)

    if not resulting_idx:
        print(f'\n No results for your search query - {sq}')
        print('\n  Modify the query and try again, listed below are the searched URLs')

        for idx, ul in enumerate(url_list):
            print(f'{idx+1}. {ul}')

        return

    print("\n Search results, in decreasing order of relevance \n")
    for idx, val in enumerate(resulting_idx):
        print(f'{idx+1}: {url_list[val]}')
