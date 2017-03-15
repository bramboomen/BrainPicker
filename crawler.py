from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup # Library for parsing html-tags ao.

bp = "https://www.brainpickings.org/2017/03/01/mary-ruefle-madness-rack-and-honey-prayer/"


def bptest():
    print("visiting: " + bp)
    crawler = Crawler()
    links = crawler.get_internal_links(bp)
    for l in links:
        print(l)


class Crawler:

    def get_links(self, url):
        html = self.read_url(url)
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



    def read_url(self, url):
        response = urlopen(url)
        if response.getheader('Content-Type') == "text/html; charset=UTF-8":  # Make sure that page is HTML
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
        else:
            print(url + "not crawlable")
            return "", []
        return htmlString


    def bp_preprocessor(self, html):
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find('div', { "class" : "entry_content" })

        return r