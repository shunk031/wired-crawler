# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.pardir)

from wired_crawler.crawler import WiredCrawler
from slacker import Slacker
import json

HOME_DIR = os.path.expanduser("~")

if __name__ == '__main__':

    WIRED_URL = "https://www.wired.com/category/science/page/1"
    crawler = WiredCrawler(WIRED_URL)

    try:
        crawler.crawl()
    except Exception as e:

        slacker_config = os.path.join(HOME_DIR, ".slacker.config")
        with open(slacker_config, "r") as rf:
            config = json.load(rf)

        slacker = Slacker(config["token"])

        trial = 0
        while trial < 3:
            try:
                slacker.chat.post_message("#crawler", e)
            except Exception:
                trial += 1
            else:
                break
