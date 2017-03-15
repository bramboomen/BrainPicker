from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup # Library for parsing html-tags ao.
from utils import read_url


class Crawler:

    def get_links(self, url):
        html = read_url(url)
        print("started")
        entry = self.bp_preprocessor(html)

        links = []
        for link in entry.find_all(href=True):
            links.append(link['href'])
        return links

    def get_internal_links(self, url):
        links = self.get_links(url)
        internal_links = []
        for link in links:
            if "brainpickings.org/20" in link and link not in internal_links:
                internal_links.append(link)

        return internal_links


    def bp_preprocessor(self, html):
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find('div', { "class" : "entry_content" })

        return r