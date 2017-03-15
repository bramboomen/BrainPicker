from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup # Library for parsing html-tags ao.

bp = "https://www.brainpickings.org/2017/03/01/mary-ruefle-madness-rack-and-honey-prayer/"


def bptest():
    print("visiting: " + bp)
    links = getLinks(bp)
    # links = bp_afterprocessor(links)
    for l in links:
        print(l)


# Main Crawler function
def getLinks(url):
    print("started")
    links = []
    baseUrl = url
    response = urlopen(url)
    if response.getheader('Content-Type') == "text/html; charset=UTF-8": # Make sure that page is HTML
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        entry = bp_preprocessor(htmlString)
        print("crawling " + url)
        links = findurls(entry)
        return links
    else:
        print(url + "not crawlable")
        return "",[]


def bp_preprocessor(html):
    soup = BeautifulSoup(html, "html.parser")
    r = soup.find('div', { "class" : "entry_content" })

    return r


def findurls(html):
    links = []
    for link in html.find_all(href=True):
        links.append(link['href'])
    return links


def bp_afterprocessor(links):
    newlinks = []
    for link in links:
        if "brainpickings.org/20" in link and link not in newlinks:
            newlinks.append(link)

    return newlinks