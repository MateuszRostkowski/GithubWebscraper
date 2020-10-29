from requests import session
from bs4 import BeautifulSoup as bs
import json
import datetime
import maya

from dotenv import load_dotenv
import os

load_dotenv()

URL1 = 'https://github.com/session'
USER = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
URL2 = os.environ.get("URL")


print(USER)
print(PASSWORD)
print(URL2)

with session() as s:
                  
    req = s.get(URL1).text
    html = bs(req, "html.parser")
    token = html.find("input", {"name": "authenticity_token"}).attrs['value']
    com_val = html.find("input", {"name": "commit"}).attrs['value']        
    
    login_data = {'login': USER,
                  'password': PASSWORD,
                  'commit' : com_val,
                  'authenticity_token' : token}
                      
    response_1 = s.post(URL1, data = login_data)
    response_2 = s.get(URL2)

    content = bs(response_2.content, "html.parser")

    commits = []

    for commit in content.findAll('li', attrs={"class": "js-commits-list-item"}):
        try:
            additional = commit.find('pre', attrs={"class": "text-small ws-pre-wrap"}).text
        except AttributeError:
            additional = None

        commitObject = {
            "author": commit.find('a', attrs={"class": "commit-author"}).text,
            "date": commit.find('relative-time')["datetime"],
            "text": commit.find('a', attrs={"class": "link-gray-dark text-bold js-navigation-open"}).text,
            "additional": additional,
        }
        commits.append(commitObject)
        

    day = 1
    data = []

    for i in commits:
        dt = maya.parse(i['date']).datetime(to_timezone='Europe/Warsaw', naive=False).replace(tzinfo=None)
        difference = (datetime.datetime.today() - dt).days
        if difference == day: 
            data.append(i['text'])

    with open('commits.json', 'w') as outfile:
        json.dump(data, outfile)
