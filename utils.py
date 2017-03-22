from urllib.request import urlopen
import urllib.error


def read_url(url):
    try:
        response = urlopen(url)
    except urllib.error.HTTPError as e:
        return "empty"
    except urllib.error.URLError as e:
        return "empty"
    if response.getheader('Content-Type') == "text/html; charset=UTF-8":  # Make sure that page is HTML
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8")
    else:
        print(url + "not crawlable")
        return "empty"
    return htmlString


def dts(x):
    if (x < 10 and x > 0):
        return "0" + (str(x))
    else:
        return str(x)