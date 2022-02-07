#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fbscrubber import FacebookPhotoScraper, FacebookPostScraper

profile_url = '' # PUT THE URL OF YOUR FACEBOOK PROFILE PAGE HERE
scraper = None
choice_invalid = True

while choice_invalid:
    print('\nEnter \'photo\' if you want to manipulate your Facebook photos or \
enter \'post\' if you want to manipulate your Facebook posts: ', end='')
    choice = input()
    if choice == 'photo':
        choice_invalid = False
        scraper = FacebookPhotoScraper(profile_url)
    elif choice == 'post':
        choice_invalid = False
        scraper = FacebookPostScraper(profile_url)
        scraper.navigate_to_timeline()
    else:
        print('Invalid choice. Try again.')

