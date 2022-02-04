#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import time

from .FacebookLauncher import FacebookLauncher

class FacebookPostScraper(FacebookLauncher):

    def __init__(self, profile_url):
        super(FacebookPostScraper, self).__init__(profile_url)

    def navigate_to_timeline(self):
        self.driver.get(self.profile_url)

    def scroll_to_timeline_bottom(self):
        scroll_script = 'window.scrollTo(0, document.body.scrollHeight);'
        get_max_height_script = 'return document.body.scrollHeight;'

        reached_end = False
        prev_page_height = 0
        while not reached_end and not self.kill_now:
            self.driver.execute_script(scroll_script)
            time.sleep(1)
            current_page_height = self.driver.execute_script(get_max_height_script)
            if prev_page_height == current_page_height:
                time.sleep(3)
                current_page_height = self.driver.execute_script(get_max_height_script)
                if prev_page_height == current_page_height:     # Check again
                    reached_end = True
            else:
                prev_page_height = current_page_height

    def scroll_to_top(self):
        scroll_script = 'window.scrollTo(0, 0);'
        self.driver.execute_script(scroll_script)
        time.sleep(0.5)

    def scroll_down(self):
        scroll_script = 'window.scrollBy(0, window.innerHeight);'
        get_height_script = 'return window.pageYOffset;'
        prev_page_height = self.driver.execute_script(get_height_script)
        self.driver.execute_script(scroll_script)
        time.sleep(0.5)
        current_page_height = self.driver.execute_script(get_height_script)

        # Make sure scroll happened and data isn't just loading
        count = 0
        max_count = 5
        while prev_page_height == current_page_height:
            current_page_height = self.driver.execute_script(get_height_script)
            self.driver.execute_script(scroll_script)
            time.sleep(0.5)
            count += 1
            if count > max_count:       # Hack; probably reached the end
                break

    def get_menu_buttons(self):
        selector = '[aria-label=\"Actions for this post\"]'
        menu_buttons = self.driver.find_elements_by_css_selector(selector)
        return menu_buttons

    def delete_post(self):
        delete_selector = 'div.qu0x051f:nth-child(3)'
        confirm_selector = '[aria-label=\"Delete\"]'
        deleted = False
        try:
            delete = self.driver.find_element_by_css_selector(delete_selector)
            delete.click()
            time.sleep(1)
            confirm = self.driver.find_element_by_css_selector(confirm_selector)
            confirm.click()
            time.sleep(1)
            deleted = True
        except NoSuchElementException:
            pass
        return deleted

    def delete_posts(self):
        self.scroll_to_timeline_bottom()
        self.scroll_to_top()
        menu_buttons = self.get_menu_buttons()
        for menu_button in menu_buttons:
            if self.kill_now:
                break
            try:
                menu_button.click()
                time.sleep(2)
                if not self.delete_post():
                    menu_button.click()
            # Exception sometimes triggers when menu button not in view
            except ElementClickInterceptedException:
                self.scroll_down()
                time.sleep(2)
                try:
                    menu_button.click()
                    time.sleep(2)
                    if not self.delete_post():
                        menu_button.click()
                except:
                    continue

