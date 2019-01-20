#!/usr/bin/env python
import sys
import json
from InstagramAPI import InstagramAPI
from warnings import warn
from pprint import pformat

from wip import login, password

def get_media_locations(api, mediaId):
    api.mediaInfo(mediaId)
    locations = []
    for i in api.LastJson['items']:
        if 'location' in i:
            locations.append(i['location'])
        # else:
        #     print('skipped ' + i['id'])
    return locations


def get_items_locations(api, items):
    return sum((get_media_locations(api, i['id']) for i in items), [])
    # locations = []
    # for i in items:
    #     locations += get_locations(api, i['id'])


def get_locations():
    api = InstagramAPI(login, password)
    if not api.login():
        warn(pformat(api.LastJson()))
        sys.exit(1)

    api.getLikedMedia()
    liked = get_items_locations(api, api.LastJson['items'])
    # names = {l['name'] for l in locations}
    # locations = []
    # for i in api.LastJson['items']:
    #     locations += get_locations(api, i['id'])
    # print('Found {} liked locations: {}'.format(len(locations), names))

    api.getSelfUserFeed()
    own = get_items_locations(api, api.LastJson['items'])
    # names = {l['name'] for l in locations}
    # print('Found {} self locations: {}'.format(len(locations), names))

    return own, liked

def main():
    own, liked = get_locations()
    with open('locations.json', 'w') as f:
        json.dump({'own': own, 'liked': liked}, f)

main()
