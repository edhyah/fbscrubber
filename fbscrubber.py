#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FacebookPhotoScraper import FacebookPhotoScraper
from FacebookPostScraper import FacebookPostScraper
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('profile_url', type=str, help='URL to profile page')
    parser.add_argument('action', choices=('save-uploaded-photos',
        'save-tagged-photos', 'remove-tagged-photos', 'delete-posts'))
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.action == 'save-uploaded-photos':
        scraper = FacebookPhotoScraper(args.profile_url)
        scraper.navigate_to_first_photo(photo_type=FacebookPhotoScraper.PhotoType.PHOTOS_BY)
        scraper.save_photos()
    elif args.action == 'save-tagged-photos':
        scraper = FacebookPhotoScraper(args.profile_url)
        scraper.navigate_to_first_photo(photo_type=FacebookPhotoScraper.PhotoType.PHOTOS_OF)
        scraper.save_photos()
    elif args.action == 'remove-tagged-photos':
        scraper = FacebookPhotoScraper(args.profile_url)
        scraper.navigate_to_first_photo(photo_type=FacebookPhotoScraper.PhotoType.PHOTOS_OF)
        scraper.remove_tags()
    elif args.action == 'delete-posts':
        scraper = FacebookPostScraper(args.profile_url)
        scraper.delete_posts()

if __name__ == '__main__':
    main()

