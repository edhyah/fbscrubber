#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FacebookPhotoScraper import FacebookPhotoScraper
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('profile_url', type=str, help='URL to profile page')
    parser.add_argument('action', choices=('save-uploaded-photos',
        'save-tagged-photos', 'remove-tagged-photos', 'delete-posts'))
    return parser.parse_args()

def main():
    args = parse_arguments()

    scraper = FacebookPhotoScraper(args.profile_url)

    if args.action == 'save-uploaded-photos':
        scraper.navigate_to_first_photo(photo_type=FacebookPhotoScraper.PhotoType.PHOTOS_BY)
        scraper.save_photos()
    elif args.action == 'save-tagged-photos':
        scraper.navigate_to_first_photo(photo_type=FacebookPhotoScraper.PhotoType.PHOTOS_OF)
        scraper.save_photos()
    elif args.action == 'remove-tagged-photos':
        scraper.navigate_to_first_photo(photo_type=FacebookPhotoScraper.PhotoType.PHOTOS_OF)
        scraper.remove_tags()
    elif args.action == 'delete-posts':
        raise NotImplementedError

if __name__ == '__main__':
    main()

