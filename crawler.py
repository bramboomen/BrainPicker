from bs4 import BeautifulSoup # Library for parsing html-tags ao.
from utils import read, save_html, Logger
from database_utils import DBSession
from database import Article


def crawl(start, end, local, save):
    db = DBSession()
    urls = get_ordered_articles()
    if end < 0:
        end = urls.__len__()
    for x in range(start, end+1):
        url = urls[x]
        print("crawling index: " + str(x))
        crawler = Crawler(url[0], local, save)
        references = crawler.get_internal_links()
        for reference in references:
            ref = {'url': url[0],
                   'ref': reference}
            db.insert_reference(ref)


def get_ordered_articles():
    db = DBSession()
    urls = db.session.query(Article.url).all()
    url_list = []
    for url in urls:
        url_list.append(url)
    return url_list


class Crawler:

    def __init__(self, url, local, save):
        self.url = url
        self.local = local
        self.save = save
        self.log = Logger()
        self.entry = self.bp_preprocessor()

    def get_links(self):
        links = []
        for link in self.entry.find_all(href=True):
            links.append(link['href'])
        return links

    def get_internal_links(self):
        print("visiting: " + self.url)
        links = self.get_links()
        internal_links = []
        for link in links:
            if "brainpickings.org/20" in link and link not in internal_links:
                internal_links.append(link)
                print("found internal: " + link)
        return internal_links

    def bp_preprocessor(self):
        html = read(self.url, self.local, self.log)
        # Save the article locally
        if self.save and not self.local:
            title = self.url.replace("https://", "")
            title = title.replace("/", ":")
            save_html(html, "html_pages/" + title, self.log)
        soup = BeautifulSoup(html, "html.parser")
        r = soup.find('div', {"class": "entry_content"})
        return r