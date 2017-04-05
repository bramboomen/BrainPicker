from sner import Ner
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree
from bs4 import BeautifulSoup


# set correct java runtime version because OSX stupid.
import os
java_path = "/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"
os.environ['JAVAHOME'] = java_path

file = "www.brainpickings.org/2017/03/10/elizabeth-bishop-efforts-of-affection-a-memoir-of-marianne-moore/.html"
file = file.replace("/", ":")
page = open("html_pages/" + file, "r")


class NameFinder:

    def __init__(self, html):
        # self.classifier = '/Users/bram/Documents/Universiteit/Onderzoeksproject/stanford-ner/classifiers/\
        #                    english.all.3class.distsim.crf.ser.gz'
        # self.jar = '/Users/bram/Documents/Universiteit/Onderzoeksproject/stanford-ner/stanford-ner-3.7.0.jar'
        # self.ner = StanfordNERTagger(self.classifier, self.jar, encoding='utf-8')
        self.sner = MyNer(host='localhost', port=8080)
        self.text = self.format_input(html)
        self.persons = []
        self.locations = []
        self.organisations = []
        self.scraped = False

    def get_persons(self):
        self.check()
        return self.persons

    def get_locations(self):
        self.check()
        return self.locations

    def get_organisations(self):
        self.check()
        return self.organisations

    def get_named_entities(self):
        entities = []
        entities.extend(self.persons)
        entities.extend(self.locations)
        entities.extend(self.organisations)
        return entities

    def scrape_named_entities(self):
        ne = self.sner.get_entities_chunked(self.text)
        persons, organisations, locations = self.format_output(ne)
        return persons, organisations, locations

    def count(self, ne_list):
        count_list = []
        for a in ne_list:
            a.append(1)
            for b in count_list:
                if a[0].lower() == b[0].lower() or a[0].lower() in b[0].lower():
                    b[2] += 1
                elif b[0].lower() in a[0].lower():
                    count_list.remove(b)
                    a[2] += 1
                    count_list.append(a)
            if not any(a[0] in sub[0] for sub in count_list):
                count_list.append(a)
        return count_list

    def format_input(self, input):
        """
        :param input: html
        :return: string
        """
        soup = BeautifulSoup(page.read(), "html.parser")
        r = soup.find('div', {"class": "entry_content"})
        return r.get_text(" ", strip=True).__str__()

    def format_output(self, output):
        """
        :param output: tuples
        :return: list
        """
        person_ne_list = []
        org_ne_list = []
        loc_ne_list = []
        for ne in output:
            ne = list(ne)
            ne[0] = ne[0].replace('\n', '')
            if ne[1] == 'PERSON':
                person_ne_list.append(ne)
            if ne[1] == 'ORGANISATION':
                org_ne_list.append(ne)
            if ne[1] == 'LOCATION':
                loc_ne_list.append(ne)
        return person_ne_list, org_ne_list, loc_ne_list

    def check(self):
        if not self.scraped:
            self.persons, self.organisations, self.locations = self.scrape_named_entities()
        self.scraped = True


class MyNer(Ner):

    def get_entities_chunked(self, text):
        tagged = self.get_entities(text)
        tree = self.make_ne_tree(tagged)
        ne_in_sent = []
        for subtree in tree:
            if type(subtree) == Tree:  # If subtree is a noun chunk, i.e. NE != "O"
                ne_label = subtree.label()
                ne_string = " ".join([token for token, pos in subtree.leaves()])
                ne_in_sent.append((ne_string, ne_label))
        return ne_in_sent

    # Courtesy of alvas on StackOverflow
    # http://stackoverflow.com/a/30666949
    def stanford_reformat(self, tagged_sent):
        bio_tagged_sent = []
        prev_tag = "O"
        for token, tag in tagged_sent:
            if tag == "O":  # O
                bio_tagged_sent.append((token, tag))
                prev_tag = tag
                continue
            if tag != "O" and prev_tag == "O":  # Begin NE
                bio_tagged_sent.append((token, "B-" + tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag == tag:  # Inside NE
                bio_tagged_sent.append((token, "I-" + tag))
                prev_tag = tag
            elif prev_tag != "O" and prev_tag != tag:  # Adjacent NE
                bio_tagged_sent.append((token, "B-" + tag))
                prev_tag = tag

        return bio_tagged_sent

    # Courtesy of alvas on StackOverflow
    # http://stackoverflow.com/a/30666949
    def make_ne_tree(self, tagged):
        bio_tagged_sent = self.stanford_reformat(tagged)
        sent_tokens, sent_ne_tags = zip(*bio_tagged_sent)
        sent_pos_tags = [pos for token, pos in pos_tag(sent_tokens)]

        sent_conlltags = [(token, pos, ne) for token, pos, ne in zip(sent_tokens, sent_pos_tags, sent_ne_tags)]
        ne_tree = conlltags2tree(sent_conlltags)
        return ne_tree
