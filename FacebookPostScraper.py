#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from FacebookLauncher import FacebookLauncher

class FacebookPostScraper(FacebookLauncher):

    def __init__(self, profile_url):
        super(FacebookPostScraper, self).__init__(profile_url)

    def navigate_to_timeline(self):
        self.driver.get(self.profile_url)

    def scroll_to_timeline_bottom(self):
        scroll_script = 'window.scrollTo(0, document.body.scrollHeight);'
        get_height_script = 'return document.body.scrollHeight;'

        reached_end = False
        past_page_height = 0
        while not reached_end and not self.kill_now:
            self.driver.execute_script(scroll_script)
            time.sleep(1)
            current_page_height = self.driver.execute_script(get_height_script)
            if past_page_height == current_page_height:
                time.sleep(3)
                current_page_height = self.driver.execute_script(get_height_script)
                if past_page_height == current_page_height:     # Check again
                    reached_end = True
            else:
                past_page_height = current_page_height

    def get_menu_buttons(self):
        selector = '[aria-label=\"Actions for this post\"]'
        menu_buttons = self.driver.find_elements_by_css_selector(selector)
        return menu_buttons

    def delete_posts(self):
        self.scroll_to_timeline_bottom()
        menu_buttons = self.get_menu_buttons()
        for menu_button in menu_buttons:
            if self.kill_now:
                break
            try:
                menu.click()
                time.sleep(1)
            except:
                time.sleep(0.1)
                continue

