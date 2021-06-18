from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
import time
import pandas as pd


def scroller(url):
    browser = webdriver.Chrome(executable_path = "chromedriver.exe")

    browser.get(url)
    time.sleep(3)
    last_height = browser.execute_script("return document.body.scrollHeight")

    i = 0
    while i < 1:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i+=1

    html = (browser.page_source).encode('utf-8')
    return html

def main():

    url = 'https://www.twitter.com/search/requestforstartup'

    users = list()
    tweets = list()
    dates = list()
    discs = list()
    retweets = list()
    likes = list()

    soup = bs(scroller(url), 'html.parser')
    image_tags = soup.find_all("div", {"data-testid": "tweet"})

    for i in image_tags:
        if (i != None):
            users.append(i.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}).text)
            tweets.append(i.find("div", {"css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"}).find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}).text)
            dates.append(i.find("a", {"class": "css-4rbku5 css-18t94o4 css-901oao r-9ilb82 r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"}).find("time").text)
            
            iDiscs = i.find("div", {"data-testid":"reply"})
            for j in iDiscs:
                if (j.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}) != None):
                    discs.append(j.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}).text)
                else:
                    discs.append("0")

            iRets = i.find("div", {"data-testid":"retweet"})
            for k in iRets:
                if (k.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}) != None):
                    retweets.append(k.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}).text)
                else:
                    retweets.append("0")
            
            iLikes = i.find("div", {"data-testid":"like"})
            for l in iLikes:
                if (l.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}) != None):
                    likes.append(l.find("span", {"class":"css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"}).text)
                else:
                    likes.append("0")
            


    data_dict = {
        "Author": users,
        "Tweet": tweets,
        "Date": dates,
        "Comments": discs,
        "Retweets": retweets,
        "Likes": likes}

    df = pd.DataFrame.from_dict(data_dict)
    df.to_csv('dataset.csv',mode='w', encoding='utf-8')


if __name__ == "__main__":
    main()