#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbscrubber import FacebookPhotoScraper, FacebookPostScraper

profile_url = 'https://www.facebook.com/edwardahn999999999'
scraper = None

print('Type \'photo\' if you want to manipulate your Facebook photos, or type \
\'post\' if you want to manipulate your Facebook posts: ', end='')
choice = input()
if choice == 'photo':
    scraper = FacebookPhotoScraper(profile_url)
elif choice == 'post':
    scraper = FacebookPostScraper(profile_url)
    scraper.navigate_to_timeline()
else:
    print('Invalid choice. Try again.')

