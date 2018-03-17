#!/usr/bin/env python 3.6
# Version 0.1.2018 - by TianqiW

# ScrapUrl is set to get all target courses urls from the calender of Ualberta for the year 2018-2019
# If there wouldn't be big changes on the calender itself
# Only parts that should be change are the pages and the root url

import requests
from bs4 import BeautifulSoup
import time


# Start is the first page, which is 1 by default. And end is the last page with is 72 (by default )for 2018-2019
# You can change the behaviour of the file r/w to only open once and write multiple times.
def scrapUrl(start=1, end=72):
    for page in range(start, end+1):
        file = open("url.txt", "a+")
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "http://calendar.ualberta.ca/content.php?catoid=28&navoid=7156"
        }
        url = "http://calendar.ualberta.ca/content.php?catoid=28&catoid=28&navoid=7156&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D="+str(page)+"#acalog_template_course_filter"
        req = session.get(url, headers=headers)
        bsObj = BeautifulSoup(req.text)
        temp = bsObj.find_all("a", {"href": True, "id": False, "onclick": True, "class": False})  # filter the tags, temp is a list of all useful <a> tags
        for i in temp:
            href = "http://calendar.ualberta.ca/"+str(i["href"]+"\n")  # combine the relative address and the root address
            file.write(href)
        file.close()
        print("Successful get page", page)
        time.sleep(3)  # you don't want to send the request to fast, or you can remove it
