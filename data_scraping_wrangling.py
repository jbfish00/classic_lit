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
master_list = master_list[['Title', 'Year']]

title_to_replace = "The Wonderful Wizard of Oz"
replacement_title = "The Wizard of Oz"
master_list['Title'] = master_list['Title'].replace(title_to_replace, replacement_title)


#cleaning to try and match other lists
master_list['Title'] = master_list.apply(lambda row: row['Title'] if row['Title'] == "The Invisible Man" else row['Title'].replace('The ', ''), axis=1)
master_list['Title'] = master_list['Title'].replace("&", "and", regex=True)
master_list['Title'] = master_list['Title'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True)
master_list['Title'] = master_list['Title'].str.lower()
#master_list['Title'] = master_list['Title'].str.replace(r'^the\s', '')
master_list['Title'] = master_list['Title'].str.split(', or,').str[0]
master_list['Title'] = master_list['Title'].str.split(':').str[0]
master_list['Title'] = master_list['Title'].str.strip()  # Added line to remove leading and trailing spaces

master_list.to_csv('master_list.csv', index=False)

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
df_rank_genre = df_rank_genre.loc[:, ['Title', 'Author', 'Rank', 'Genre']]

title_to_replace = "20,000 Leagues Under the Sea"
replacement_title = "Twenty Thousand Leagues Under the Sea"
df_rank_genre['Title'] = df_rank_genre['Title'].replace(title_to_replace, replacement_title)

titles_to_replace = ["The Fellowship of the Ring", "The Two Towers", "The Return of the King"]
replacement_title = "The Lord of the Rings"
df_rank_genre['Title'] = df_rank_genre['Title'].replace(titles_to_replace, replacement_title)

df_rank_genre['Title'] = df_rank_genre.apply(lambda row: row['Title'] if row['Title'] == "The Invisible Man" else row['Title'].replace('The ', ''), axis=1)
df_rank_genre['Title'] = df_rank_genre['Title'].replace("&", "and", regex=True)
df_rank_genre['Title'] = df_rank_genre['Title'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True)
df_rank_genre['Title'] = df_rank_genre['Title'].str.lower()
#df_rank_genre['Title'] = df_rank_genre['Title'].str.replace(r'^the\s', '')
df_rank_genre['Title'] = df_rank_genre['Title'].str.split(', or,').str[0]
df_rank_genre['Title'] = df_rank_genre['Title'].str.split(':').str[0]
df_rank_genre['Title'] = df_rank_genre['Title'].str.strip() 

df_rank_genre['Rank'] = pd.to_numeric(df_rank_genre['Rank'].str.replace('.', ''), errors='coerce')

df_rank_genre.to_csv('df_rank_genre.csv', index=False)


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
df_sell = df_sell.loc[:, ['Title', 'Approx. sales (in millions)', 'Bestseller']]

df_sell['Title'] = df_sell['Title'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True)
df_sell['Title'] = df_sell['Title'].str.lower()
df_sell['Title'] = df_sell['Title'].str.replace(r'^the\s', '')
df_sell['Title'] = df_sell['Title'].str.split(', or,').str[0]
df_sell['Title'] = df_sell['Title'].str.split(':').str[0]
df_sell['Title'] = df_sell['Title'].str.strip() 


#merge dfs together
merged_df = pd.merge(df_rank_genre, master_list, on='Title', how='left')
merged_df = pd.merge(merged_df, df_sell, on='Title', how='left')
merged_df['Approx. sales (in millions)'] = merged_df['Approx. sales (in millions)'].fillna('<10')
merged_df['Bestseller'] = merged_df['Bestseller'].fillna('No')
merged_df.to_csv('merged_df.csv', index=False)






