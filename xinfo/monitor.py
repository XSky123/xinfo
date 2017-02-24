#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import requests
from bs4 import BeautifulSoup as bs

class Session(object):
    def __init__(self):
        """ Initialization of basic session.
            add UA to session.
        """
        self.s = requests.session()
        self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

    def get_page(self, url):
        """ Return HTML and update to self.page
        :param url:
        :return:
        """
        self.page = self.s.get(url).content
        return self.page

class Parser(object):
    def __init__(self, content):
        self.content = content
        self.parse_all(self.cut_content(content))
    def cut_content(self, content):
        """ get identified area, cut full html into pieces."""
        pass

    def parse_all(self, content):
        """ read all pieces, recursively call parse()"""
        self.list = [self.parse(piece) for piece in content]
        return self.list
    def parse(self, piece):
        """ parse each 'line'(html)
        :param piece:
        :return: dict{'url','title','time'}
        """
        pass

    def get_json(self):
        """ get json format list.for deleting repeated.

        :return: json text
        """
        self.json = json.dumps(self.list)
        return self.json

class Filter(object):
    def check_update(self, origin, new):
        """ check update from json string
        :param origin:
        :param new:
        :return: list
        """
        origin_list = json.loads(origin)
        new_list = json.loads(new)
        update_list = list()
        for line in new_list:
            if line not in origin_list:
                update_list.append(line)
        return update_list

#TODO use independent file to save those overridden class
class SSDUT(Parser):
    """ Just for test."""
    def cut_content(self, content):
        soup = bs(content, "lxml")
        noti_area = soup.find(class_="c_hzjl_list1")
        return [piece for piece in noti_area.find_all("li", style="width:650px;")]

    def parse(self, piece):
        return {
            "url":piece.find("a")["href"][2:],
            "title":piece.find("a")["title"],
            "time":piece.find("span").get_text(strip=True)
        }

def test():
    s = Session()
    page = s.get_page("http://ssdut.dlut.edu.cn/index/bkstz.htm")
    p = SSDUT(page)
    print p.get_json()

test()
