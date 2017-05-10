from bs4 import BeautifulSoup # Library for parsing html-tags ao.
from utils import read, save_html, Logger
from database_utils import DBSession
from database import Article
from ner import NameFinder


def scrape(start, end, local, save, what_to_do):
    db = DBSession()
    urls = get_ordered_articles()
    if "all" in what_to_do:
        what_to_do = "references, people, organisations, locations"
    if end < 0:
        end = urls.__len__()
    for x in range(start, end+1):
        url = urls[x]
        print("crawling index: " + str(x))
        crawler = Scraper(url[0], local, save)
        if "references" in what_to_do:
            references = crawler.get_internal_links()
            for reference in references:
                ref = {'url': url[0],
                       'ref': reference}
                db.insert_reference(ref)
        if "people" in what_to_do:
            people = crawler.get_people()
            for person in people:
                db.insert_person({"name": person['name']})
                db.insert_person_rel(
                    {'article': url[0],
                     'person': person['name'],
                     'count': person['count'],
                     'main': person['am_i_main']
                     })
        if "organisations" in what_to_do:
            orgs = crawler.get_organisations()
            for org in orgs:
                db.insert_organisation({"name": org["name"]})
                db.insert_organisation_rel({
                    "article": url[0],
                    "organisation": org["name"],
                    "count": org["count"]
                })
        if "locations" in what_to_do:
            locations = crawler.get_locations()
            for loc in locations:
                db.insert_location({"name": loc["name"]})
                db.insert_location_rel({
                    "article": url[0],
                    "location": loc["name"],
                    "count": loc["count"]
                })


def get_ordered_articles():
    db = DBSession()
    urls = db.session.query(Article.url).all()
    url_list = []
    for url in urls:
        url_list.append(url)
    return url_list


class Scraper:

    def __init__(self, url, local, save):
        self.url = url
        self.local = local
        self.save = save
        self.log = Logger()
        self.entry = self.bp_preprocessor()
        self.ner = NameFinder(self.entry)

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

    def get_people(self):
        print("getting people from: " + self.url)
        persons = self.ner.get_persons()
        main = 0
        if persons:
            for pers in persons:
                pers['am_i_main'] = False
                if pers['count'] > persons[main]['count']:
                    main = persons.index(pers)
            persons[main]['am_i_main'] = True
        return persons

    def get_organisations(self):
        print("getting orginisations from: " + self.url)
        return self.ner.get_organisations()

    def get_locations(self):
        print("getting locations from: " + self.url)
        return self.ner.get_locations()

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
