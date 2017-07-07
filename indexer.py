from __init__ import log as logger
from utils import read, dts, save_html
from bs4 import BeautifulSoup  # Library for parsing html-tags ao.
import datetime as dt
from database_utils import DBSession


class Indexer:
    def __init__(self, date, local=False, save=True):
        start_year, start_month, start_day = date.year, date.month, date.day
        self.baseurl = "https://www.brainpickings.org"
        self.start_date = dt.date(start_year, start_month, start_day)
        self.end_date = dt.date.today()
        self.local = local
        self.save = save

    def bp_index(self):
        """
        Main index method, iterates all dates within a range
        :return: a list of dicts { 'url': url, 'title': title, 'date': date object }
        """
        logger.write_log("Indexing from: " + str(self.start_date) +
                         " to: " + str(self.end_date))

        db = DBSession()
        articlelist = []
        delta = dt.timedelta(days=1)

        while self.start_date <= self.end_date:
            page = self.fetch_page(self.start_date.year,
                                   self.start_date.month,
                                   self.start_date.day)
            if (page != "empty"):
                for article in page:
                    articlelist.append(article)
                    db.insert_article(article)
            self.start_date += delta

    def fetch_page(self, y, m, d):
        """
        Constructs an url and checks if it contains a page.
        :param y: year
        :param m: month
        :param d: day
        :return: a list of dicts { 'url': url, 'title': title, 'date': date object }
        """

        url = self.baseurl + "/" + dts(y) + "/" + dts(m) + "/" + dts(d) + "/"
        response = read(url, self.local)
        if (response == "empty"):
            return response
        else:
            logger.write_log("visiting: " + url)
            title = url.replace("https://", "")
            title = title.replace("/", ":")
            # Save the article locally
            if self.save and not self.local:
                save_html(response, "html_collection_pages/" + title)
            articles = self.fetch_articles(response)
            for article in articles:
                article['date'] = dt.date(y, m, d)
            return articles

    def fetch_articles(self, html):
        """
        Gets the relevant info from the page
        :param html: The HTML page content
        :return: a list of dicts { 'url': url, 'title': title }
        """
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find("div", {"id": "recent_archives"})

        urls = []
        for article in r.find_all(href=True):
            if ("brainpickings.org/20" in article['href']
                and article['href'] not in urls
                and ['yellow'] in article.attrs.values()):
                url = article['href']
                title = str(article.contents[0])
                urls.append({'url': url, 'title': title})
        return urls
