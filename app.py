import argparse

from trie import run


def search(query):
    run(query)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-q', '--query', required=True, help='Enter the search query')
    arg_val = vars(ap.parse_args())

    search(query=arg_val['query'])
