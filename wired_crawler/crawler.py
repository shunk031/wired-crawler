# -*- coding: utf-8 -*-

from __future__ import print_function
from wired_crawler.scraper import WiredScraper
from bs4 import BeautifulSoup

import time
import traceback
import json

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError


class WiredCrawler:

    FINISH_CRAWL = "Finish crawl!"

    def __init__(self, target_url, save_dir="./data", page_count=1):
        self.target_url = target_url
        self.before_url = None
        self.save_dir = save_dir
        self.page_count = page_count

    def _make_soup(self, url):

        max_retries = 3
        retries = 0

        while True:
            try:
                with urlopen(url) as res:
                    html = res.read()
                return BeautifulSoup(html, "lxml")

            except HTTPError as err:
                print("[ EXCEPTION ] in {}#make_soup: {}".format(self.__class__.__name__, err))

                retries += 1
                if retries >= max_retries:
                    raise Exception("Too many retries.")

                wait = 2 ** (retries - 1)
                print("[ RETRY ] Waiting {} seconds...".format(wai))
                time.sleep(wait)

    def get_next_page_link(self, url):

        self.before_url = url
        soup = self._make_soup(self.target_url)
        div_pagination = soup.find("div", {"class": "pagination"})
        a_next = div_pagination.find("a", {"class": "next"})

        if a_next is not None and "href" in a_next.attrs:
            next_page_url = a_next["href"]

            if self.before_url != next_page_url:
                print("[ DEBUG ] Next article list page: {}".format(url))
                return next_page_url

        return None

    def crawl(self):

        while True:
            start = time.time()
            print("[ DEBUG ] Now page {} PROCESSING".format(self.page_count))
            scraper = WiredScraper(self.target_url, self.save_dir)
            scraper.scrap()
            self.target_url = self.get_next_page_link(self.target_url)

            if self.target_url is None:
                break

            self.page_count += 1
            time.sleep(2)

            end = time.time()
            print("[ DEBUG ] Elapsed time: {:.2f} [min]".format((end - start) / 60))

        return self.FINISH_CRAWL
