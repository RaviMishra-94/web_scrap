import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from io import StringIO
import time

def get_page_links():
    url = "https://www.footballdb.com/games/index.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    html_content = urllib.request.urlopen(req).read().decode('utf-8')
    
    soup = BeautifulSoup(html_content, 'html5lib')
    
    # Find all links in the page
    links = soup.find_all('a', href=re.compile(r'/games/boxscore/'))
    
    return [link['href'] for link in links]


def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req).read()


# Get the links from the page
page_links = get_page_links()

for i, link in enumerate(page_links):
    # URL to download table from.
    to_download = f"https://www.footballdb.com/{link}"
    downloaded_site = download(to_download)

# decode the downloaded content
    html_content = downloaded_site.decode('utf-8')

# use BeautifulSoup with html5lib parser
    soup = BeautifulSoup(html_content, 'html5lib')

# find all tables on the page
    tables = soup.find_all('table')

# Download only the second table (index 1)
    for j, table in enumerate(tables):
        if j == 1:
        # Add a sleep here to avoid making requests too quickly
            time.sleep(2)  # Sleep for 2 seconds (adjust as needed)

        # extract table data using pandas with StringIO
            df = pd.read_html(StringIO(str(table)))[0]  # Use the current table, adjust as needed

        # remove MultiIndex columns
            df.columns = ['_'.join(map(str, col)) if isinstance(col, tuple) else str(col) for col in df.columns]

        # save to Excel file with a unique name
            filename = f"game{i + 1}.xlsx"
            df.to_excel(filename, index=False)

            print(f"Table {i + 1} content saved to '{filename}'")
        
        # Break out of the loop once the second table is processed
            break



    

