# GithubWebscraper

## Launch

1. Fetch repo
2. Run: `pip3 install -r requirements.txt`
3. Create duplicate `.env.example` file and rename it to `.env`

```env
USER_NAME=LOGIN_TO_GITHUB // your github login
PASSWORD=GITHUB_PASSWORD // your github password
URL=URL_TO_SCRAPE // url to page that you want to scrape
```

4. Fetch data from github `python3 webscraper.py`
5. Parse data `python3 parsedata.py`
