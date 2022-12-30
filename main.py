from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template, url_for
import requests
import random
import string
import re


# cleanup the text
def cleanup(text): 
    text = re.sub("\n", "",text)
    text = re.sub(" +", " ",text)
    text = re.sub(" \r", "",text)
    text = text.lstrip()
    text = text.rstrip()
    return text

# get list sites and pages
def getSites(page):
    
    content = requests.get(f'https://neocities.org/browse?page={page}')
    soup = BeautifulSoup(content.text, 'html.parser')
    link = soup.find('ul', class_="row website-Gallery content int-Gall")
    
    array = []
    for site in link.find_all('li'):

        usr = site.find('div', class_="username")

        data = {
            "url": site.find('a', class_='neo-Screen-Shot').get("href"),
            "title": cleanup(site.find('div', class_="title").text),
            "info": {
                "site": f"https://neocities.org" + usr.find('a').get("href"),
                "site_name": cleanup(usr.find('a').text),
                "views": cleanup(site.find("div", class_="site-stats hide-on-mobile").find("a").text)
            }
        }
        array.append(data)

    return array

# get max pages
def getMaxPage():
    result = []
    content = requests.get(f'https://neocities.org/browse')
    soup = BeautifulSoup(content.text, 'html.parser')

    e = soup.find('div', class_="txt-Center eps pagination")

    for a in e.find_all('a', attrs={"aria-label": True}):
        result.append(a["aria-label"].split(' ')[1])

    return result.pop()


def getSiteInfo(site):
    content = requests.get(f'https://neocities.org/site/{site}')
    soup = BeautifulSoup(content.text, 'html.parser')

    # general 
    url = soup.find("p",class_="site-url").text
    title = cleanup(soup.find("h2",class_="eps title-with-badge").text)

    # stats
    start = soup.find("div", class_="header-Outro with-site-image")
    stats = start.find("div", class_="stats").find_all("div", class_="stat")

    end = soup.find("div", class_="container site-profile")
    stats2 = end.find("div", class_="stats").find_all("div", class_="stat")
    
    # following
    following = []
    try:
        for f1 in end.find("div", class_="following-list").find_all("a"):
            following.append("https://neocities.org" + f1.get("href"))
        following.pop(0)
    except:
        following = []

    # followers
    follower = []
    try:
        for f1 in end.find("div", class_="follower-list").find_all("a"):
            follower.append("https://neocities.org" + f1.get("href"))
        follower.pop(0)
    except:
        follower = []

    # tags
    tags = []
    try:
        for t in end.find_all("a", class_="tag"):
            tags.append("https://neocities.org" + t.get("href"))
    except:
        tags = []


    statlist = {
        "views": cleanup(stats[0].find("strong").text),
        "followers": cleanup(stats[1].find("strong").text),
        "updates": cleanup(stats[2].find("strong").text),
        "tips": cleanup(stats[3].find("strong").text)
    }

    l = {
        "stats": statlist,
        "updated": cleanup(stats2[0].find("strong").text),
        "joined": cleanup(stats2[1].find("strong").text),
        "following": following,
        "followed_by": follower,
        "url": url,
        "site": site,
        "title": title,
        "tags": tags
    }

    return l

def randomSite():
    y = random.randrange(1,maxpages)
    result = getSites(y)

    return random.choice(result)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html',r=randomSite(),m=maxpages)


@app.route('/random/', methods=['GET'])
def r():
    return jsonify(randomSite())

@app.route('/list/<number>', methods=['GET'])
def l(number):
    try:
        number = int(number)
        if number > maxpages:
            number = maxpages
        elif number < 1:
            number = 1
    except:
        number = 1
    return jsonify(getSites(number))


@app.route('/site/<site>', methods=['GET'])
def s(site):
    try:
        return jsonify(getSiteInfo(site))
    except AttributeError:
        return 'site not found'

if __name__ == '__main__':
    maxpages = int(getMaxPage())
    app.run(host='0.0.0.0',port=5050)