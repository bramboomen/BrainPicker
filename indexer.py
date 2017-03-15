from utils import read_url, dts
from bs4 import BeautifulSoup # Library for parsing html-tags ao.
import time


class Indexer:

    def __init__(self, start_year, start_month, start_day):
        self.baseurl = "https://www.brainpickings.org"
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        # Brainpicking uses format: baseurl/yyyy/mm/dd
        self.end_year = int(time.strftime('%Y'))
        self.end_month = int(time.strftime('%m'))
        self.end_day = int(time.strftime('%d'))

    def bp_index(self):
        print("Indexing from: " +
              dts(self.start_year) + "/" +
              dts(self.start_month) + "/" +
              dts(self.start_day) +
              " to: " +
              dts(self.end_year) + "/" +
              dts(self.end_month) + "/" +
              dts(self.end_day)
              )

        curr_year = self.start_year
        curr_month = self.start_month
        curr_day = self.start_day

        urllist = []

        while (curr_year != self.end_year or
               curr_month != self.end_month or
               curr_day != self.end_day):
            for y in range (self.start_year, self.end_year+1):
                for m in range (1, 13):
                    for d in range (1, 32):
                        curr_year = y
                        curr_month = m
                        curr_day = d
                        if (curr_year == self.end_year and
                            curr_month == self.end_month and
                            curr_day == self.end_day):
                            break
                        page = self.fetch_page(y, m, d)
                        if (page != "empty"):
                            for url in page:
                                urllist.append(url)
                                print("added: " + url)

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
                urls.append(url['href']) # This does not work
        return urls
