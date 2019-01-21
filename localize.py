#!/usr/bin/env python
import sys
import json
from InstagramAPI import InstagramAPI
from warnings import warn
from pprint import pformat

from wip import login, password

def get_media(api, media_id):
    api.mediaInfo(media_id)
    media = [i for i in api.LastJson['items'] if 'location' in i]
    return media

def get_media_locations(api, items):
    location_media = {}
    # for i in items: m i
    for m in get_media(api, items[0]['id']):
        loc = m.pop('location')
        loc_id = loc['facebook_places_id']
        if loc_id in location_media:
            location_media[loc_id]['items'].append(m)
        else:
            location_media[loc_id] = loc
            location_media[loc_id]['items'] = [m]
    return location_media



# def get_media_locations(api, media_id):
#     api.mediaInfo(media_id)
#     locations = []
#     for i in api.LastJson['items']:
#         if 'location' in i:
#             locations.append(i['location'])
#         # else:
#         #     print('skipped ' + i['id'])
#     return locations


# def get_items_locations(api, items):
#     return sum((get_media_locations(api, i['id']) for i in items), [])
    # locations = []
    # for i in items:
    #     locations += get_locations(api, i['id'])


def get_locations():
    api = InstagramAPI(login, password)
    if not api.login():
        warn(pformat(api.LastJson()))
        sys.exit(1)

    api.getLikedMedia()
    liked = get_media_locations(api, api.LastJson['items'])
    # names = {l['name'] for l in locations}
    # locations = []
    # for i in api.LastJson['items']:
    #     locations += get_locations(api, i['id'])
    # print('Found {} liked locations: {}'.format(len(locations), names))

    api.getSelfUserFeed()
    own = get_media_locations(api, api.LastJson['items'])
    # names = {l['name'] for l in locations}
    # print('Found {} self locations: {}'.format(len(locations), names))

    return own, liked

def main():
    own, liked = get_locations()
    with open('static/js/locations.json', 'w') as f:
        json.dump({'own': own, 'liked': liked}, f)

if __name__ == '__main__':
    main()
