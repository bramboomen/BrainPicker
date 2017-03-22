from urllib.request import urlopen
import urllib.error
import os.path
import datetime as dt


def read(url, local):
    if local:
        return read_file(url)
    else:
        return read_url(url)


def read_url(url):
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        log(url + " : " + e.__str__())
        return "empty"
    except urllib.error.URLError as e:
        log(url + " : " + e.__str__())
        return "empty"
    if response.getheader('Content-Type') == "text/html; charset=UTF-8":  # Make sure that page is HTML
        html_bytes = response.read()
        html_string = html_bytes.decode("utf-8")
        log(url + " : " + "Added to index")
    else:
        print(url + "not crawlable")
        log(url + " : " + "Page not html/utf-8")
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
    log(location + " written to file")


def log(content):
    now = dt.datetime.now()
    file = open("log/" +
                str(now.year) + "-" +
                str(now.month) + "-" +
                str(now.day) + ":" +
                str(now.hour) + "." +
                str(now.minute) + ".txt",
                "a")
    file.write(content + "\n")
    file.close()


def dts(x):
    if (x < 10 and x > 0):
        return "0" + (str(x))
    else:
        return str(x)
