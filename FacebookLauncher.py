#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
import getpass
import signal
import time

class FacebookLauncher:

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

