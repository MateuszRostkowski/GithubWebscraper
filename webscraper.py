from requests import session
from bs4 import BeautifulSoup as bs
import json
from dotenv import load_dotenv
import os

load_dotenv()

URL1 = 'https://github.com/session'
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
URL2 = os.environ.get("URL")

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
        commitObject = {
            "author": commit.find('a', attrs={"class": "commit-author"}).text,
            "date": commit.find('relative-time')["datetime"],
            "name": commit.find('a', attrs={"class": "link-gray-dark text-bold js-navigation-open"}).text,
        }
        commits.append(commitObject)
        
    with open('commits.json', 'w') as outfile:
        json.dump(commits, outfile)
