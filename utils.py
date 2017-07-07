from __init__ import log as logger
from urllib.request import urlopen
import urllib.error
import os.path
import datetime as dt
import sys


def read(url, local):
    if local:
        return read_file(url)
    else:
        return read_url(url)


def read_url(url):
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        logger.write_log(url + " : " + e.__str__())
        return "empty"
    except urllib.error.URLError as e:
        logger.write_log(url + " : " + e.__str__())
        return "empty"
    if response.getheader('Content-Type') == "text/html; charset=UTF-8":  # Make sure that page is HTML
        html_bytes = response.read()
        html_string = html_bytes.decode("utf-8")
        logger.write_log(url + " : " + "Added to index")
    else:
        print(url + "not crawlable")
        logger.write_log(url + " : " + "Page not html/utf-8")
        return "empty"
    return html_string


def read_file(url):
    file = url.replace("https://", "")
    file = file.replace("/", ":")
    if os.path.isfile("html_collection_pages/" + file + ".html"):
        with open("html_collection_pages/" + file + ".html", "r") as html_file:
            html_string = html_file.read().replace('\n', '')
    elif os.path.isfile("html_pages/" + file + ".html"):
        with open("html_pages/" + file + ".html", "r") as html_file:
            html_string = html_file.read().replace('\n', '')
    else:
        return "empty"
    return html_string


def save_html(html_string, location):
    location += ".html"
    file = open(location, "w")
    file.write(html_string)
    file.close()
    logger.write_log(location + " written to file")


def dts(x):
    if 0 < x < 10:
        return "0" + (str(x))
    else:
        return str(x)


class ProgressBar:

    def __init__(self, total, start=0, bar=True):
        self.total = total
        self.current = start
        self.bar = bar

    def update(self, current):
        self.current = current

    def print(self):
        percentage = int((self.current / self.total) * 100) + 1
        bar = self.gen_bar(percentage)
        sys.stdout.write("\r" + str(percentage) + "% " + bar)
        sys.stdout.flush()
        if self.current == self.total:
            print("\n")

    def update_print(self, current):
        self.update(current)
        self.print()

    def gen_bar(self, perc):
        bar = ""
        if self.bar:
            percentage = perc
            bar = "[" + "="*percentage + " "*(100-percentage) + "]"
        return bar
