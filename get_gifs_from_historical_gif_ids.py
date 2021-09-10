import json

QUERY = 'cimrman'
RESOURCES_PATH = 'resources'
WEBP_URL = 'https://i.giphy.com/media/{id}/200w.webp'
MP4_URL = 'https://i.giphy.com/media/{id}/200w.mp4'


def bootstrap_ids():
    # replace [] with:
    # https://github.com/MikulasZelinka/cimrman_gifs/blob/5ae1d4370f5ee5dd73af0af9604a38e4cf9b8f83/cimrman.json
    gifs = []

    with open(f'{RESOURCES_PATH}/{QUERY}_id_url.json', 'w', encoding='utf-8') as f:
        json.dump(
            {gif['id']: {'url': gif['url'], 'keywords': gif['keywords']} for gif in gifs},
            f, ensure_ascii=False, indent=2, sort_keys=True
        )


def main(bootstrap=False):
    if bootstrap:
        bootstrap_ids()

    with open(f'{RESOURCES_PATH}/{QUERY}_id_url.json', encoding='utf-8') as f:
        gifs = json.load(f)

    gifs = [
        {
            'url': gif['url'],
            # 'mp4': MP4_URL.format(id=id),
            'webp': WEBP_URL.format(id=id),
            'keywords': gif['keywords'],
        }
        for id, gif in gifs.items()
    ]

    # minimal output for web
    with open(f'{RESOURCES_PATH}/{QUERY}.json', 'w', encoding='utf-8') as f:
        json.dump(gifs, f, ensure_ascii=False, separators=(',', ':'))

    # readable output for humans and diffs
    with open(f'{QUERY}_readable.json', 'w', encoding='utf-8') as f:
        json.dump(
            {gif['url']: sorted(gif['keywords']) for gif in gifs},
            f, ensure_ascii=False, indent=2, sort_keys=True
        )
    return gifs


if __name__ == '__main__':
    main(bootstrap=True)
