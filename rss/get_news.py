import feedparser
import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
import re


url_link = "http://fetchrss.com/rss/59549c628a93f872018b4567709026440.xml"

# get all the links of news title
links = []
rss = feedparser.parse(url_link)


# d['feed']['title'] gives title of page

# len(d['entries']) gives the total entries in array index [0]

# Loop for all the post
lemmatizer = WordNetLemmatizer()

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

#get news from republica
def get_rss_republica():
    url_link = "http://fetchrss.com/rss/59549c628a93f872018b4567677181163.xml"
    # get all the links of news title
    links = []
    news=[]
    data=[]
    rss = feedparser.parse(url_link)
    for post in rss.entries:
        links.append(post.link)
    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        # news = [pt.get_text() for pt in soup.select(".content-wrapper")]
        divTag = soup.find_all("div",{"class":"box recent-news-categories-details"})

        for tag in divTag:
            alltags = tag.find_all('p')

        del alltags[:3]


        #print(l[0])
        for tag in alltags:
            each = str(tag)
            # print(each.replace('<p>','').replace('</p>',''))
            news.append(each.replace('<p>','').replace('</p>',''))
        data.append(news)
    return data


# get_rss_republica()

#test news is traffic accident related or not
def testaccidentnews(headline):
    ans = False
    headline = headline.lower()
    testcases=['hit','die','injure','kill','plunge']
    #spit word with comma and space both
    wordlist = re.findall(r'\s|,|[^,\s]+', headline)
    lemword = []
    for word in wordlist:
        #lematize all words of the headline with reference to verb
        test = lemmatizer.lemmatize(word, 'v')
        lemword.append(test)

    #check wordlist with testcases for accident matching news
    for lem in lemword:
        if lem in testcases:
            ans = True
            print(lem)
    return ans
