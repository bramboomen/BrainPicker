import subprocess
import signal
import os
import time
from sner import Ner
from nltk import pos_tag
from nltk.chunk import conlltags2tree
from nltk.tree import Tree


class NameFinder:

    def __init__(self, html):
        self.sner = MyNer(host='localhost', port=8080)
        self.text = self.format_input(html)
        self.persons = []
        self.locations = []
        self.organisations = []
        self.scraped = False

    def get_persons(self):
        """
        :return: List of dicts
        {
            "name": 'Name of Person',
            "type": 'PERSON',
            "count": int
        }
        """
        self.check()
        return self.count(self.persons)

    def get_locations(self):
        self.check()
        return self.count(self.locations)

    def get_organisations(self):
        self.check()
        return self.count(self.organisations)

    def get_named_entities(self):
        entities = []
        entities.extend(self.persons)
        entities.extend(self.locations)
        entities.extend(self.organisations)
        return entities

    def scrape_named_entities(self):
        ne = self.sner.get_entities_chunked(self.text)
        return self.format_output(ne)

    def count(self, ne_list):
        count_list = []
        for a in ne_list:
            a['count'] = 1
            for b in count_list:
                if a['name'].lower() == b['name'].lower() or a['name'].lower() in b['name'].lower():
                    b['count'] += 1
                elif b['name'].lower() in a['name'].lower():
                    count_list.remove(b)
                    a['count'] += 1
                    count_list.append(a)
            if not any(a['name'] in sub['name'] for sub in count_list):
                count_list.append(a)
        return count_list

    def format_input(self, html):
        """
        :param html: html
        :return: string
        """
        # soup = BeautifulSoup(html, "html.parser")
        return html.get_text(" ", strip=True).__str__()

    def format_output(self, output):
        """
        :param output: tuples
        :return: list
        """
        person_ne_list = []
        org_ne_list = []
        loc_ne_list = []
        for ne in output:
            ne = {'name': ne[0].replace('\n', ''), 'type': ne[1]}
            if ne['type'] == 'PERSON':
                person_ne_list.append(ne)
            if ne['type'] == 'ORGANISATION':
                org_ne_list.append(ne)
            if ne['type'] == 'LOCATION':
                loc_ne_list.append(ne)
        return person_ne_list, org_ne_list, loc_ne_list

    def check(self):
        if not self.scraped:
            self.persons, self.organisations, self.locations = self.scrape_named_entities()
        self.scraped = True


class MyNer(Ner):

    def get_entities_chunked(self, text):
        tagged = self.get_entities(text)
        if not tagged:
            return []
        else:
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


class NERserver:

    def __init__(self):
        self.dr = os.path.dirname(__file__)
        self.process = None

    def start(self):
        if not self.process:
            self.process = subprocess.Popen("exec " + self.dr + '/stanfordnerserver.sh',
                                            stdout=subprocess.PIPE, shell=True)
            time.sleep(10)
        else:
            print("ner server already running")

    def stop(self):
        self.process.kill()
