#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FacebookLauncher import FacebookLauncher

class FacebookPostScraper(FacebookLauncher):

    def __init__(self, profile_url):
        super(FacebookPostScraper, self).__init__(profile_url)

