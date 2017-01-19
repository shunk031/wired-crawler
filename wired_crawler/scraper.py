# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup

import os
import csv

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import HTTPError


class WiredScraper:

    none_count = 0

    def __init__(self, target_url, save_dir):
        self.target_url = target_url
        self.save_dir = save_dir

    def _make_soup(self, url):
        try:
            with urlopen(url) as response:
                html = response.read()

            return BeautifulSoup(html, "lxml")

        except HTTPError as e:
            print("[ DEBUG ] in WiredScraper#make_soup: {}".format(e))
            return None

    def scrap(self):

        article_detail_url_list = self.get_article_detail_urls()

        article_detail_info = []
        for article_url in article_detail_url_list:
            article_dict = self.get_article_detail_info_dict(article_url)
            article_detail_info.append(article_dict)

        self.save_article_detail_info_list(article_detail_info)

    def get_article_detail_urls(self):

        soup = self._make_soup(self.target_url)

        # 記事概要一覧を取得する
        ul_col = soup.find("ul", {"class": "col"})

        # 記事概要のそれぞれのデータを取得する
        li_articles = ul_col.find_all("li")

        # 記事詳細へのURLを取得する
        article_detail_url_list = []
        for li_article in li_articles:
            a_pad = li_article.find("a", {"class": "clearfix"})
            url = a_pad["href"]
            print("[ DEBUG ] Get URL: {}".format(url))
            article_detail_url_list.append(url)

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):
        article_dict = {}
        article_dict["url"] = article_url

        detail_soup = self._make_soup(article_url)
        h1_post_title = detail_soup.find("h1", {"class": "post-title"})
        try:
            title = h1_post_title.get_text()
        except AttributeError:
            title = str(self.none_count)
            self.none_count += 1

        print("[ DEBUG ] Title: {}".format(title))
        article_dict["title"] = title

        try:
            article_content = detail_soup.find("article", {"class": "content"})
            article_content = article_content.get_text()
        except AttributeError:
            article_content = None

        article_dict["article"] = article_content
        return article_dict

    def save_article_detail_info_list(self, article_detail_info_list):

        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        for article_detail_dict in article_detail_info_list:
            article_title = article_detail_dict["title"]
            csv_filename = self._convert_filename(article_title)
            csv_filename = "{}.csv".format(csv_filename)

            with open(os.path.join(self.save_dir, csv_filename), "w") as wf:
                writer = csv.writer(wf)
                writer.writerow([article_detail_dict["title"],
                                 article_detail_dict["url"],
                                 article_detail_dict["article"]])

    def _convert_filename(self, article_title):

        filename = article_title.replace(" ", "_")
        filename = filename.replace("/", "")
        return filename
