import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

## Master List with Title(key), Author, Year
df1 = pd.read_csv('tgb_1.csv', header = None)
df2 = pd.read_csv('tgb_2.csv', header = None)

master_list = pd.concat([df1, df2], ignore_index=True)
master_list = master_list.drop(master_list.columns[0], axis=1)
master_list.columns = ['Title', 'Author', 'Year']
master_list['Title'] = master_list['Title'].str.extract(r'^([^(]*)')

## Genre and Rank
url = 'https://www.oclc.org/en/worldcat/library100/top500.html'

response = requests.get(url)
rank_genre = []

# Check if the request was successful (status code 200)
if response.status_code == 200:
    html_content = response.content

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    table_rows = soup.find_all('tr')

    # Iterate through the rows and extract information
for row in table_rows:
        # Check if the 'td' with class 'ra' exists
        rank_td = row.find('td', class_='ra')
        rank = rank_td.text.strip() if rank_td else "N/A"

        # Check if the 'td' with class 'ti' and 'a' exists
        title_td = row.find('td', class_='ti')
        title = title_td.a.text.strip() if title_td and title_td.a else "N/A"

        # Check if the 'td' with class 'au' exists
        author_td = row.find('td', class_='au')
        author = author_td.text.strip() if author_td else "N/A"

        genre = row.get('class')[-1] if 'class' in row.attrs else "Fiction"

        rank_genre.append({'Rank': rank, 'Title': title, 'Author': author, 'Genre': genre})


df_rank_genre = pd.DataFrame(rank_genre)
df_rank_genre = df_rank_genre.drop(0)
df_rank_genre['Title'] = df_rank_genre['Title'].str.extract(r'^([^(]*)')

## Bestselling Information
url = 'https://en.wikipedia.org/wiki/List_of_best-selling_books#More_than_100_million_copies'
tables = pd.read_html(url)
df1 = tables[0]
df1['Approximate sales'] = '>100'
df2 = tables[1]
df2['Approximate sales'] = '50-100'
df3 = tables[2]
df3['Approximate sales'] = '20-50'
df4 = tables[3]
df4['Approximate sales'] = '10-20'

df_sell = pd.concat([df1, df2,df3,df4])
df_sell.rename(columns={'Approximate sales': 'Approx. sales (in millions)', 'Book': 'Title'}, inplace=True)
df_sell['Bestseller'] = 'Yes'
df_sell['Title'] = df_sell['Title'].str.extract(r'^([^(]*)')




