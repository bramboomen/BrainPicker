from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup

bp = "https://www.brainpickings.org/2017/03/01/mary-ruefle-madness-rack-and-honey-prayer/"


def getLinks(url):
    print("started")
    links = []
    # Remember the base URL which will be important when creating
    # absolute URLs
    baseUrl = url
    # Use the urlopen function from the standard Python 3 library
    response = urlopen(url)
    # Make sure that we are looking at HTML and not other things that
    # are floating around on the internet (such as
    # JavaScript files, CSS, or .PDFs for example)
    if response.getheader('Content-Type') == "text/html; charset=UTF-8":
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
        htmlString = bp_preprocessor(htmlString)
        print("crawling " + url)
        #links = findurls(htmlString)
        return links
    else:
        print(url + "not crawlable")
        return "",[]


def bptest():
    print("visiting: " + bp)
    links = getLinks(bp)
    # links = bp_afterprocessor(links)
    for l in links:
        print(l)


def bp_preprocessor(html):
    soup = BeautifulSoup(html, "html.parser")
    r = soup.findAll('div', { "class" : "entry_content" })
    return r


def findurls(html):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll('href')


def bp_afterprocessor(links):
    newlinks = []
    for link in links:
        if "brainpickings.org/20" in link and link not in newlinks:
            newlinks.append(link)

    return newlinks