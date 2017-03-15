from utils import read_url, dts
from bs4 import BeautifulSoup # Library for parsing html-tags ao.
import datetime as dt


class Indexer:

    def __init__(self, start_year, start_month, start_day):
        self.baseurl = "https://www.brainpickings.org"
        self.start_date = dt.date(start_year, start_month, start_day)
        self.end_date = dt.date.today()


    def bp_index(self):
        print("Indexing from: " +
              str(self.start_date) +
              " to: " +
              str(self.end_date)
              )

        urllist = []
        delta = dt.timedelta(days=1)

        while self.start_date <= self.end_date:
            page = self.fetch_page(self.start_date.year,
                                   self.start_date.month,
                                   self.start_date.day)
            if (page != "empty"):
                for url in page:
                    urllist.append(url)
                    print("added: " + url)
            self.start_date += delta
        return urllist


    def fetch_page(self, y, m, d):
        url = self.baseurl + "/" + dts(y) + "/" + dts(m) + "/" + dts(d) + "/"
        response = read_url(url)

        if (response == "empty"):
            return response
        else:
            print("visiting: " + url)
            urls = self.fetch_articles(response)
            return urls


    def fetch_articles(self, html):
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find("div", { "id": "recent_archives" })

        urls = []
        for url in r.find_all(href=True):
            if "brainpickings.org/20" in url['href'] and url['href'] not in urls:
                urls.append(url['href'])
        return urls
