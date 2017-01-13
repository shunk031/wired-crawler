# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.pardir)

from wired_crawler.scraper import WiredScraper

if __name__ == '__main__':

    WIRED_URL = "https://www.wired.com/category/science/page/1"
    scraper = WiredScraper(WIRED_URL, "./dump_files")
    scraper.scrap()
