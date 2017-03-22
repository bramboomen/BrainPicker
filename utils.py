from urllib.request import urlopen
import urllib.error
import os.path


def read(url, local):
    if local:
        return read_file(url)
    else:
        return read_url(url)


def read_url(url):
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        return "empty"
    except urllib.error.URLError as e:
        return "empty"
    if response.getheader('Content-Type') == "text/html; charset=UTF-8":  # Make sure that page is HTML
        html_bytes = response.read()
        html_string = html_bytes.decode("utf-8")
    else:
        print(url + "not crawlable")
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


def dts(x):
    if (x < 10 and x > 0):
        return "0" + (str(x))
    else:
        return str(x)
