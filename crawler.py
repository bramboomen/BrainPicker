from bs4 import BeautifulSoup # Library for parsing html-tags ao.
from utils import read, save_html, Logger
from database_utils import db_session

def crawl(local, save):
    db = db_session()
    urls = db.session.query(Article.url).all()
    for url in urls
        crawler = Crawler(url[0], local, save)


class Crawler:

    def __init__(self, url, local, save):
        self.url = url
        self.local = local
        self.save = save
        self.log = Logger()

    def get_page(self, url):
        html = read(url, self.local, self.log)
        if self.save:
            title = url.replace("https://", "")
            title = title.replace("/", ":")
            save_html(html, "html_pages/" + title, self.log)
        return html

    def get_links(self, html):
        print("started")
        entry = self.bp_preprocessor(html)

        links = []
        for link in entry.find_all(href=True):
            links.append(link['href'])
        return links

    def get_internal_links(self, html):
        links = self.get_links(html)
        internal_links = []
        for link in links:
            if "brainpickings.org/20" in link and link not in internal_links:
                internal_links.append(link)
        return internal_links

    def bp_preprocessor(self, html):
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find('div', {"class": "entry_content"})
        return r
