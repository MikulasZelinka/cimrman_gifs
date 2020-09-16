import json
from collections import Counter

import requests
from tqdm import tqdm
from unidecode import unidecode

API_URL = 'api.giphy.com/v1/gifs/search'
API_KEY = open('API_KEY').read().strip()
LIMIT = 50
QUERY = 'cimrman'


def get_gif_keywords(giphy_url):
    r = requests.get(giphy_url)
    r.encoding = r.apparent_encoding
    for l in r.text.splitlines():
        if l.strip().startswith('<meta name="keywords"'):
            return [unidecode(x.strip().lower()) for x in l.split('"')[-2].split(',')]


def get_common_keywords(keywords, min_occurence=0.5):
    num_elements = len(keywords)
    keywords = [x for y in keywords for x in y]
    counter = Counter(keywords)
    return set(keyword for keyword, value in counter.items() if value >= min_occurence * num_elements)


def main():
    gifs = []
    offset = 0

    while True:
        r = requests.get(f'https://{API_URL}?api_key={API_KEY}&q={QUERY}&limit={LIMIT}&offset={offset}')
        response = r.json()

        for gif in tqdm(response['data']):
            gifs.append({
                'id': gif['id'],
                'url': gif['url'],
                'keywords': get_gif_keywords(gif['url']),
                'images': gif['images']
            })

        pagination = response['pagination']
        offset += pagination['count']
        if offset >= pagination['total_count']:
            print(f'Processed all {pagination["total_count"]} gifs.')
            break

    common_keywords = get_common_keywords([gif['keywords'] for gif in gifs])
    print(f'Removing common keywords: {", ".join(common_keywords)}.')
    for gif in gifs:
        gif['keywords'] = [keyword for keyword in gif['keywords'] if keyword not in common_keywords]

    with open(f'{QUERY}.json', 'w', encoding='utf-8') as f:
        json.dump(gifs, f, ensure_ascii=False)
    return gifs


if __name__ == '__main__':
    main()
