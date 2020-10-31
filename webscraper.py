from requests import session
from tabulate import tabulate
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

print('Script started')

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
    print('Successfuly logged to github')
    response_2 = s.get(URL2)
    print('Successfuly fetched data from github')

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

    day = 0
    days = 5
    output = {}

    for x in range(days):
        
        data = []
        date = ''
        for i in commits:
            dt = maya.parse(i['date']).datetime(to_timezone='Europe/Warsaw', naive=False).replace(tzinfo=None)
            date = dt.strftime('%Y-%m-%d')
            difference = (datetime.datetime.today() - dt).days
            if difference == day: 
                toAdd = i['additional'] if i['additional'] else ''
                data.append(i['text'] + toAdd)
                output[date] = data
                
        day = day + 1

    table = []
    for key in output:
        table.append([key, '\n'.join(output[key])])
    print(tabulate(table))

    with open('commits.json', 'w') as outfile:
        json.dump(output, outfile)

    print('Successfuly saved commits')