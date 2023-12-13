import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def download(url):
    return urllib.request.urlopen(url).read()

# URL to download table from.
to_download = "https://en.wikipedia.org/wiki/Ludhiana"
downloaded_site = download(to_download)

# decode the downloaded content
html_content = downloaded_site.decode('utf-8')

# use BeautifulSoup with html5lib parser
soup = BeautifulSoup(html_content, 'html5lib')

# find all tables on the page
tables = soup.find_all('table')

# Extract each table and save to separate Excel files
for i, table in enumerate(tables):
    # extract table data using pandas with StringIO
    df = pd.read_html(StringIO(str(table)))[0]  # Use the current table, adjust as needed
    
    # remove MultiIndex columns
    df.columns = ['_'.join(map(str, col)) if isinstance(col, tuple) else str(col) for col in df.columns]
    
    # save to Excel file with a unique name
    filename = f"output_table_{i + 1}.xlsx"
    df.to_excel(filename, index=False)

    print(f"Table {i + 1} content saved to '{filename}'")
