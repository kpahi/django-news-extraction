import feedparser
import requests
from bs4 import BeautifulSoup

url_link = "http://fetchrss.com/rss/59549c628a93f872018b4567709026440.xml"

# get all the links of news title
links = []
rss = feedparser.parse(url_link)


# d['feed']['title'] gives title of page

# len(d['entries']) gives the total entries in array index [0]

# Loop for all the post
for post in rss.entries:
    links.append(post.link)


def get_data_from_rss():
    data = []
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        news = [pt.get_text() for pt in soup.select(".content-wrapper")]
        data.append(news)
        # print(data)
    return data


# print(links)
