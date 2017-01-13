# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.pardir)

from wired_crawler.crawler import WiredCrawler

if __name__ == '__main__':

    WIRED_URL = "https://www.wired.com/category/science/page/1"
    crawler = WiredCrawler(WIRED_URL)
    crawler.crawl()
