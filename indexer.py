from utils import read_url, dts
from bs4 import BeautifulSoup # Library for parsing html-tags ao.
import datetime as dt


class Indexer:

    def __init__(self, start_year, start_month, start_day):
        self.baseurl = "https://www.brainpickings.org"
        self.start_date = dt.date(start_year, start_month, start_day)
        self.end_date = dt.date.today()


    def bp_index(self):
        """
        Main index method, iterates all dates within a range
        :return: a list of dicts { 'url': url, 'title': title, 'date': date object }
        """
        print("Indexing from: " +
              str(self.start_date) +
              " to: " +
              str(self.end_date)
              )

        articlelist = []
        delta = dt.timedelta(days=1)

        while self.start_date <= self.end_date:
            page = self.fetch_page(self.start_date.year,
                                   self.start_date.month,
                                   self.start_date.day)
            if (page != "empty"):
                for article in page:
                    articlelist.append(article)
                    print("added: " + article['title'])
            self.start_date += delta
        self.fetch_text_list(urllist)


        #return urllist
        return articlelist


    def fetch_page(self, y, m, d):
        """
        Constructs an url and checks if it contains a page.
        :param y: year
        :param m: month
        :param d: day
        :return: a list of dicts { 'url': url, 'title': title, 'date': date object }
        """

        url = self.baseurl + "/" + dts(y) + "/" + dts(m) + "/" + dts(d) + "/"
        response = read_url(url)
        if (response == "empty"):
            return response
        else:
            print("visiting: " + url)
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
        r = soup.find("div", { "id": "recent_archives" })

        urls = []
        for article in r.find_all(href=True):
            if ("brainpickings.org/20" in article['href']
                    and article['href'] not in urls
                    and ['yellow'] in article.attrs.values()):
                url = article['href']
                title = article.contents[0]
                urls.append({'url': url, 'title': title})
        return urls

    def fetch_text(self, url):
        html = read_url(url)
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find("div", {"id": "posts"})
        return r

    #zet een list van urls om in een dictionary waarin elke url naar zijn tekst + tags verwijst
    def fetch_text_list(self, urllist):
        htmldict = {}
        for url in urllist:
            html = read_url(url)
            soup = BeautifulSoup(html, "html.parser")
            #r = text van de post, a = tags van de post
            r = soup.find("div", {"id": "posts"})
            a = soup.find("h4", {"class": "tags"})
            htmldict[url] = str(r) + str(a)
            self.fetch_tags(htmldict[url])
        return htmldict

    #returned de title als losse string uit een html bestand
    def fetch_title(self, html):
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find("h1", {"class": "entry-title"})
        return r.string

    #returned de tags als losse string uit een html bestand
    def fetch_tags(self, html):
        tags = []
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find_all("a", {"rel": "tag"})
        for tag in r:
            tags.append(tag.string)
        return tags



