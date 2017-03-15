from urllib.request import urlopen
from bs4 import BeautifulSoup # Library for parsing html-tags ao.
import time

baseurl = "https://www.brainpickings.org/"
start_year = 2017
start_month = 1
start_day = 1
# Brainpicking uses format: baseurl/yyyy/mm/dd
end_year = int(time.strftime('%Y'))
end_month = int(time.strftime('%m'))
end_day = int(time.strftime('%d'))

def bp_index():
    print("Indexing from: " +
          dts(start_year) + "/" +
          dts(start_month) + "/" +
          dts(start_day) +
          " to: " +
          dts(end_year) + "/" +
          dts(end_month) + "/" +
          dts(end_day)
          )

    curr_year = start_year
    curr_month = start_month
    curr_day = start_day

    while (curr_year != end_year and
           curr_month != end_month and
           curr_day != end_day):
        for y in range (start_year, end_year+1):
            for m in range (start_month, 13):
                for d in range (start_day, 31):
                    curr_year = y
                    curr_month = m
                    curr_day = d
                    fetch_page(y, m, d)


def fetch_page(y, m, d):
    url = baseurl + "/" + dts(y) + "/" + dts(m) + "/" + dts(d) + "/"


def dts(x):
    if (x < 10 and x > 0):
        return "0" + (str(x))
    else:
        return str(x)
