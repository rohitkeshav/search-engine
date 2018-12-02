import argparse

# TODO: remove stop words
# TODO: remove punctuations
# TODO: escape html tags, maybe not required since beautiful soup


def search(query):
    print(f'Search query : {query}')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-q', '--query', required=True, help='Enter the search query')
    arg_val = vars(ap.parse_args())

    search(query=arg_val['query'])
