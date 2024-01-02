import requests
from bs4 import BeautifulSoup
from io import StringIO
import pandas as pd
import numpy as np
import time

def download(url):
    return requests.get(url).text

# URL to download
google_sheets_link = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTFlwrVJW9Qi8CV39mZhChTL_yX-B2xgG4jJpv35whAkq_hd1obF9aGhaH6m63cgwennEPtwGs-n7f0/pubhtml?gid=1318557900#"
downloaded_site = download(google_sheets_link)
soup = BeautifulSoup(downloaded_site, 'html5lib')

tables = soup.find_all('table')

for index, table_to_download in enumerate(tables):
    df = pd.read_html(StringIO(str(table_to_download)))[0]  
    
    df.columns = df.columns.map('_'.join).str.strip('_')

    sheet_name = f"Sheet_{index + 1}"
    df.to_excel(f"output_google_sheets_{sheet_name}.xlsx", index=False)

    print(f"Downloaded table content from {sheet_name} saved to 'output_google_sheets_{sheet_name}.xlsx'")

# Above here is the extractor/scraper code.
# Below here is the code for manupulating excel.
    
time.sleep(5)
'''Here the path should be where this code python file is stored. First part of code downloads 8 files. 
   Enter the .xlsx file for which you want output as per your format.
   GraceAvail'23 = output_google_sheets_Sheet_1.xlsx 
   EvoAvail'23   = output_google_sheets_Sheet_2.xlsx 
   GraceAvail'24 = output_google_sheets_Sheet_3.xlsx 
   EvoAvail'24   = output_google_sheets_Sheet_4.xlsx 
   GraceAvail'25 = output_google_sheets_Sheet_5.xlsx 
   EvoAvail'25   = output_google_sheets_Sheet_6.xlsx 
   GraceAvail'26 = output_google_sheets_Sheet_7.xlsx 
   EvoAvail'26   = output_google_sheets_Sheet_8.xlsx 
   '''
df = pd.read_excel("e:/upwork/Grace/output_google_sheets_Sheet_3.xlsx") #path to your directory

df = df.iloc[15:]
df = df.iloc[:-22]
df = df.drop(columns=df.columns[:1])
df = df.dropna(axis=0, how='all')
df = df.dropna(how='all')
df = df.dropna(axis=1, how='all')

ship_name = "Grace"  # Change as per you ship
df.insert(0, 'Ship', ship_name)

df = df[~df.apply(lambda row: any('free' in str(cell).lower() for cell in row), axis=1)]
df = df[~df.apply(lambda row: any('Start' in str(cell) for cell in row), axis=1)]
df = df[~df.apply(lambda row: any('Booked' in str(cell) for cell in row), axis=1)]
df = df[~df.apply(lambda row: any('Available' in str(cell) for cell in row), axis=1)]



df['Max Value'] = df.apply(lambda row: max(cell for cell in row[4:14] if cell != '-') if any(cell != '-' for cell in row[4:14]) else '-', axis=1)
df['Min Value'] = df.apply(lambda row: min(cell for cell in row[4:14] if cell != '-') if any(cell != '-' for cell in row[4:14]) else '-', axis=1)

df = df.drop(columns=df.columns[4:14])
df = df.drop(columns=df.columns[[5, 6]])

new_column_names = {df.columns[1]: 'Start Date', df.columns[2]: 'End Date', df.columns[3]: 'Route', df.columns[4]: 'Available'}
df = df.rename(columns=new_column_names)
df['Route'] = df['Route'].apply(lambda x: f"{x.split('-')[-1].strip()} : {x.split('-')[0].strip()}")

df.insert(3, 'night', np.nan)

import pandas as pd

df['night'] = df['Route'].str.extract(r'(\d+)').astype(int) - 1

df.to_excel('grace24.xlsx', index=False) # Change as per you ship and year

time.sleep(2)

pd.set_option('display.max_colwidth', 100)

with pd.ExcelWriter('grace24.xlsx', engine='xlsxwriter') as writer: # Change as per you ship and year
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    worksheet.set_column('E:E', 45)

print("Excel File is Ready.")
    

