import json
from collections import Counter

import requests
from tqdm import tqdm
from unidecode import unidecode

API_URL = 'api.giphy.com/v1/gifs/search'
API_KEY = open('API_KEY').read().strip()
LIMIT = 50
QUERY = 'cimrman'
USERNAME = 'ceska_televize'
RESOURCES_PATH = 'resources'
IGNORE_LIST = set(open(f'{RESOURCES_PATH}/ignore_list.csv').read().strip().split())
WEBP_URL = 'https://i.giphy.com/media/{id}/200w.webp'
MP4_URL = 'https://i.giphy.com/media/{id}/200w.mp4'


def get_gif_keywords(giphy_url):
    r = requests.get(giphy_url)
    r.encoding = r.apparent_encoding
    for l in r.text.splitlines():
        if l.strip().startswith('<meta name="keywords"'):
            return [unidecode(x.strip().lower()) for x in l.split('"')[-2].split(',')]


def get_common_list_elements(lists, min_occurence=0.5):
    """Returns elements that appear in at least min_occurence (ratio) of all lists.

    Assumes that each sublist is a set (i.e., that no item is more than once in a sublist).
    """
    elements_flattened = [x for y in lists for x in y]
    counter = Counter(elements_flattened)
    return set(item for item, count in counter.items() if count >= (min_occurence * len(lists)))


def main():
    gifs = []
    offset = 0

    # there should be 416 cimrman gifs (2021-09-10)
    # https://giphy.com/ceska_televize/cimrmani
    # however, that page is dynamic and not accessible by the Giphy API
    # and we search using that instead

    # alternatively, it would be possible (better?) to use selenium
    # or to simply load the webpage manually, scroll down and extract the IDs and links from the source

    # for now, since giphy search appears to be broken (finds ~390 of those 416 gifs)
    # we use get_gifs_from_historical_gif_ids.py instead

    while True:
        # USERNAME filtering doesn't really solve everything,
        # as some of the Česká televze gifs have no username set, e.g.:
        # - https://giphy.com/gifs/ceskatelevize-ceska-czechtv-lmjBfMEhPiHteN58cD
        r = requests.get(f'https://{API_URL}?api_key={API_KEY}&q={QUERY}@{USERNAME}&limit={LIMIT}&offset={offset}')

        response = r.json()

        with tqdm(response['data']) as bar:
            for gif in tqdm(response['data']):
                if gif['id'] in IGNORE_LIST:
                    bar.write(f'Skipping ignored gif {gif["id"]}: {gif["url"]}')
                    continue

                gifs.append({
                    # 'id': gif['id'],
                    'url': gif['url'],
                    'keywords': get_gif_keywords(gif['url']),
                    # contains a lot of redundant links:
                    # 'images': gif['images'],
                    # instead, we only select the one we need
                    # 'webp': WEBP_URL.format(id=gif['id']),
                    'mp4': MP4_URL.format(id=gif['id']),
                })

            pagination = response['pagination']
            offset += pagination['count']
            if offset >= pagination['total_count']:
                print(f'{QUERY}@{USERNAME} filter – processed all {pagination["total_count"]} gifs.')
                break
    print(f'Total gifs for {QUERY}@{USERNAME}: {len(gifs)}.')

    # on top of that, giphy search is a bit broken and doesn't find a subset on the 'cimrman' query
    # we thus have to join both approaches
    existing_urls = set(gif['url'] for gif in gifs)
    offset = 0
    while True:
        r = requests.get(f'https://{API_URL}?api_key={API_KEY}&q={QUERY}&limit={LIMIT}&offset={offset}')

        response = r.json()

        with tqdm(response['data']) as bar:
            for gif in tqdm(response['data']):

                if gif['id'] in IGNORE_LIST:
                    bar.write(f'Skipping ignored gif {gif["id"]}: {gif["url"]}')
                    continue

                if gif['url'] in existing_urls:
                    continue

                tqdm.write(f'New gif without {USERNAME} filter: {gif["url"]}')

                gifs.append({
                    # 'id': gif['id'],
                    'url': gif['url'],
                    'keywords': get_gif_keywords(gif['url']),
                    # contains a lot of redundant links:
                    # 'images': gif['images'],
                    # instead, we only select the one we need
                    # 'webp': WEBP_URL.format(id=gif['id']),
                    'mp4': MP4_URL.format(id=gif['id']),
                })

            pagination = response['pagination']
            offset += pagination['count']
            if offset >= pagination['total_count']:
                print(f'{QUERY} filter – processed all {pagination["total_count"]} gifs.')
                break

    print(f'New gifs for {QUERY} without {USERNAME} filter: {len(gifs) - len(existing_urls)}.')
    print(f'Total final gifs for {QUERY}[@{USERNAME}]: {len(gifs)}.')

    common_keywords = get_common_list_elements([gif['keywords'] for gif in gifs])
    print(f'Removing common keywords: {", ".join(common_keywords)}.')
    for gif in gifs:
        gif['keywords'] = [keyword for keyword in gif['keywords'] if keyword not in common_keywords]

    # minimal output for web
    with open(f'{RESOURCES_PATH}/{QUERY}.json', 'w', encoding='utf-8') as f:
        json.dump(gifs, f, ensure_ascii=False, separators=(',', ':'))

    # readable output for humans and diffs
    with open(f'{QUERY}_readable.json', 'w', encoding='utf-8') as f:
        json.dump({gif['url']: sorted(gif['keywords']) for gif in gifs}, f, ensure_ascii=False, indent=2,
                  sort_keys=True)
    return gifs


if __name__ == '__main__':
    main()
