#!/bin/python
from  lxml  import etree


class Parser:
    def __init__(self):
        self.mName = 'Parser'
    def read_from_configbean(self):

        return  None

    def extract_urls(self, html):
        print("******************begin parser link******************")
        page = etree.HTML(html)
        hrefs = page.xpath(u"//a")
        urls = []
        for href in hrefs:
            # print("href.text=>",href.text)
            if 'href' in href.attrib.keys():
                url = href.attrib['href']
                urls.append(url)
        if (len(urls) > 0):
            return urls
        else:
            return None
