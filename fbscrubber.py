#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
import argparse
import getpass
import os
import shutil
import signal
import time

class FacebookPhotoScraper:

    month_str2num = { 'January': '01', 'February': '02', 'March': '03',
            'April': '04', 'May': '05', 'June': '06', 'July': '07',
            'August': '08', 'September': '09', 'October': '10',
            'November': '11', 'December': '12' }

    class PhotoType(Enum):
        PHOTOS_BY = 'photos_by'
        PHOTOS_OF = 'photos_of'

    def __init__(self, profile_url):
        self.driver = None
        self.download_dir = str(Path.home()) + '/Downloads/fbscrubber/tmp/'
        self.profile_url = profile_url
        if self.profile_url != '/':
            self.profile_url += '/'

        # Take inputs from the console
        self.input_email_id = input('Enter Username: ')
        self.input_pwd = getpass.getpass()

        # Disable notifications and set download directory
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values.notifications' : 2,
            'download.default_directory': self.download_dir
        }
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # Let user stop saving/deleting photos gracefully using interrupts
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.open_facebook()

    def exit_gracefully(self, *args):
        self.kill_now = True

    def open_facebook(self):
        class FacebookLoaded:
            def __call__(self, driver):
                return driver.find_element_by_tag_name('body') != None

        # Open the web browser
        self.driver.get('https://www.facebook.com')
        wait = ui.WebDriverWait(self.driver, 10)
        wait.until(FacebookLoaded())

        # Submit email and password
        email = self.driver.find_element_by_id('email')
        email.send_keys(self.input_email_id)
        pwd = self.driver.find_element_by_id('pass')
        pwd.send_keys(self.input_pwd)
        del self.input_pwd
        pwd.send_keys(Keys.RETURN)
        time.sleep(3)

    def navigate_to_first_photo(self, photo_type: PhotoType):
        self.driver.get(self.profile_url + photo_type.value + '/')
        anchors = self.driver.find_elements_by_tag_name('a')
        anchors = [a.get_attribute('href') for a in anchors]
        anchors = [a for a in anchors if str(a).startswith('https://www.facebook.com/photo')]
        self.driver.get(anchors[1])

    def navigate_to_next_photo(self):
        time.sleep(1)
        nextphoto = self.driver.find_element_by_css_selector('[aria-label=\"Next photo\"]')

        # Use Javascript to click hidden button as Selenium doesn't allow it
        self.driver.execute_script('(arguments[0]).click();', nextphoto)
        time.sleep(1.5)

    def click_menu(self):
        try:
            menu = self.driver.find_element_by_css_selector(
                    '[aria-label=\"Actions for this post\"]')
            menu.click()
            time.sleep(1.5)
        except:
            print('[WARNING] Did not find menu button')

    def save_photos(self):
        time.sleep(1)
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # Multiple photos could have been uploaded on the same day, meaning
        # these photos need to be named uniquely (name can't just be based on
        # the upload date). We name them uniquely by assigning an id
        # (corresponding to the number of photos we encountered so far with that
        # same date) to the photos. The hashmap keeps track of this information
        # efficiently.
        count = {}

        while not self.kill_now:

            # Get download link from menu
            anchors_found = False
            self.click_menu()

            anchors = self.driver.find_elements_by_tag_name('a')
            anchors = [a.get_attribute('href') for a in anchors]
            anchors = [a for a in anchors if str(a).startswith('https://scontent')]
            anchors_found = True

            # Get date photo was posted
            date = self.driver.find_element_by_css_selector('a.b1v8xokw').text
            date_numbered = FacebookPhotoScraper.get_numbered_date(date)

            # Determine photo id
            date_numbered_int = int(date_numbered)
            photo_id = 1
            if date_numbered_int not in count.keys():
                count[date_numbered_int] = 1
            else:
                count[date_numbered_int] += 1
                photo_id = count[date_numbered_int]
            photo_id_str = str(photo_id).zfill(4)

            # Ensure photo is downloadable; if not print which photo could not
            # be downloaded.
            if len(anchors) < 1 or not anchors_found:
                print('[WARNING] No download link for photo found')
                print('          Date of photo in question: ' + date)
                print('          Skipping this photo...')
                self.navigate_to_next_photo()
                continue
            if len(anchors) > 1:
                print('[WARNING] More than one download link (%d) for photo found' % (len(anchors)))
                print('          Date of photo in question: ' + date)
                print('          Using first download link...')

            # Download photo to temp directory
            self.driver.get(anchors[0])
            time.sleep(1)

            # Rename photo and move to final directory
            downloaded_files = os.listdir(self.download_dir)
            if len(downloaded_files) != 1:
                print('[WARNING] Content not found or too many found')
                print('          Found %d (not 1) downloaded files' % (len(downloaded_files)))
                print('          Date of photo in question: ' + date)
                print('          Skipping this photo...')
                self.navigate_to_next_photo()
                continue
            downloaded_file = downloaded_files[0]
            file_ext = downloaded_file[downloaded_file.rfind('.'):]
            final_filename = date_numbered + '_' + photo_id_str + file_ext
            shutil.move(self.download_dir + downloaded_file,
                    self.download_dir + '../' + final_filename)

            self.navigate_to_next_photo()

        # Remove temp directory
        os.rmdir(self.download_dir)

    def remove_tags(self):
        css_selector1 = 'div.oajrlxb2:nth-child(4)'
        css_selector2 = 'div.oajrlxb2:nth-child(5)'
        css_selector3 = 'div.g5ia77u1:nth-child(5)'
        css_selectors = [css_selector1, css_selector2, css_selector3]

        while not self.kill_now:
            selector_found = False

            for css_selector in css_selectors:
                self.click_menu()
                try:
                    self.driver.find_element_by_css_selector(css_selector).click()
                    time.sleep(1.5)
                    self.driver.find_element_by_css_selector('[aria-label=\"OK\"]').click()
                    time.sleep(1.5)
                    selector_found = True
                    break
                except NoSuchElementException:
                    continue

            if not selector_found:
                print('[WARNING] CSS selector to remove tag not found')
                print('          URL of photo: ', self.driver.current_url)
                print('          Skipping this photo...')

            self.navigate_to_next_photo()

    @staticmethod
    def get_numbered_date(date_str):    # ex. 'January 5, 2017' -> '20170105'
        date = date_str.split(' ')
        if len(date) != 3:
            print('[WARNING] Photo does not have a standard date')
            print('          Saving the photo with name %s for now...' % (date_str))
            return date_str

        year = date[2]

        try:
            month = FacebookPhotoScraper.month_str2num[date[0]]
        except KeyError:
            print('[ERROR] The month %s does not exist' % (date[0]))
            raise

        day = date[1][:-1]
        if len(day) == 1:
            day = '0' + day

        return year + month + day

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

