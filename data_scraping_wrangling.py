import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import json


def clean_title(title):
    # Common replacements and standardizations
    replacements = {
        "20,000 Leagues Under the Sea": "Twenty Thousand Leagues Under the Sea",
        "The Wonderful Wizard of Oz": "The Wizard of Oz",
        "The Adventures of Oliver Twist": "Oliver Twist",
        "&": "and",
        "harry potter and the philosopher's stone": "harry potter and the sorcerer's stone",
        "-": " ",
        "the adventures of pinocchio": "pinocchio",
        # Add more replacements as necessary
    }
    for old_title, new_title in replacements.items():
        title = title.replace(old_title, new_title)

    # Handle 'The Lord of the Rings' series titles
    lotr_titles = ["The Fellowship of the Ring", "The Two Towers", "The Return of the King"]
    if title in lotr_titles:
        title = "The Lord of the Rings"

    # Lowercase and remove parentheses and their contents
    title = re.sub(r'\s*\([^)]*\)\s*', '', title).lower()

    # Remove all articles ('the', 'a', 'an') from the title
    articles = ["the", "a", "an"]
    for article in articles:
        title = title.replace(article + " ", "").replace(" " + article, "")

    # Split on ', or,' and ':' and strip extra whitespace
    title = title.split(', or,')[0].split(':')[0].strip()

    return title


# Read the JSON file into a DataFrame (country, title, author, year)
with open('books.json') as json_file:
    json_data = json.load(json_file)

df_json = pd.DataFrame(json_data)



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

        genre = row.get('class')[-1] if 'class' in row.attrs else "gen_fiction"

        rank_genre.append({'Rank': rank, 'Title': title, 'Author': author, 'Genre': genre})


df_rank_genre = pd.DataFrame(rank_genre)
df_rank_genre = df_rank_genre.drop(0)
df_rank_genre = df_rank_genre.loc[:, ['Title', 'Author', 'Rank', 'Genre']]
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




# Applying the clean_title function to the datasets
df_rank_genre['Title'] = df_rank_genre['Title'].apply(clean_title)
df_json['Title'] = df_json['title'].apply(clean_title)
df_sell['Title'] = df_sell['Title'].apply(clean_title)



#merge dfs together
master_list = pd.merge(df_rank_genre, df_json, on='Title', how='left')
master_list = pd.merge(master_list, df_sell, on='Title', how='left')
master_list['Approx. sales (in millions)'] = master_list['Approx. sales (in millions)'].fillna('<10')
master_list['Bestseller'] = master_list['Bestseller'].fillna('No')

master_list = master_list[['Title', 'Author', 'countries', 'Rank', 'Genre', 'first_year_published', 'Approx. sales (in millions)', 'Bestseller']]
master_list.to_csv('master_list.csv', index=False)






