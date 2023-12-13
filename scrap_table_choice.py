import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def download(url):
    return urllib.request.urlopen(url).read()

# URL to download
to_download = "https://en.wikipedia.org/wiki/Ludhiana"
downloaded_site = download(to_download)

# decode the downloaded content
html_content = downloaded_site.decode('utf-8')

# use BeautifulSoup with html5lib parser
soup = BeautifulSoup(html_content, 'html5lib')

# find the second table on the page (adjust based on your specific HTML structure)
tables = soup.find_all('table')

# Extract the table of your choice (change index)
if len(tables) > 1:
    table_to_down = tables[3]
    
    # extract table data using pandas with StringIO
    df = pd.read_html(StringIO(str(table_to_down)))[0]  # Use the table found, adjust as needed
    
    # remove MultiIndex columns
    df.columns = df.columns.map('_'.join).str.strip('_')

    # save to Excel file
    df.to_excel("output_ch.xlsx", index=False)

    print("downloaded table content saved to 'output_ch.xlsx'")
else:
    print("No second table found on the page.")
