import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import json

#Function for cleaning the titles
# def clean_title(title):
#     title = title.replace("20,000 Leagues Under the Sea", "Twenty Thousand Leagues Under the Sea")
#     title = title.replace("The Wonderful Wizard of Oz", "The Wizard of Oz")
#     title = title.replace("The Adventures of Oliver Twist", "Oliver Twist")
#     # Replace titles one by one
#     titles_to_replace = ["The Fellowship of the Ring", "The Two Towers", "The Return of the King"]
#     replacement_title = "The Lord of the Rings"
#     for old_title in titles_to_replace:
#         title = title.replace(old_title, replacement_title)
    
#     title = title if title == "The Invisible Man" else title.replace('The ', '')
#     title = title.replace("&", "and")
#     title = re.sub(r'\s*\([^)]*\)\s*', '', title)
#     title = title.lower()
#     title = title.split(', or,')[0]
#     title = title.split(':')[0]
#     title = title.strip()
#     return title

# Modifying the clean_title function to be more comprehensive in handling title variations
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

    # Remove parentheses and their contents, and lowercase the title
    title = re.sub(r'\s*\([^)]*\)\s*', '', title).lower()

    # Remove leading 'The ' and split on ', or,' and ':'
    title = title.replace('the ', '').split(', or,')[0].split(':')[0].strip()

    return title



## Master List with Title(key), Author, Year
df1 = pd.read_csv('tgb_1.csv', header = None)
df2 = pd.read_csv('tgb_2.csv', header = None)

fic_nonfic_list = pd.concat([df1, df2], ignore_index=True)
fic_nonfic_list = fic_nonfic_list.drop(fic_nonfic_list.columns[0], axis=1)
fic_nonfic_list.columns = ['Title', 'Author', 'Year']
fic_nonfic_list = fic_nonfic_list[['Title', 'Year']]

title_to_replace = "The Wonderful Wizard of Oz"
replacement_title = "The Wizard of Oz"
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].replace(title_to_replace, replacement_title)


#cleaning to try and match other lists
fic_nonfic_list['Title'] = fic_nonfic_list.apply(lambda row: row['Title'] if row['Title'] == "The Invisible Man" else row['Title'].replace('The ', ''), axis=1)
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].replace("&", "and", regex=True)
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True)
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].str.lower()
#fic_nonfic_list['Title'] = fic_nonfic_list['Title'].str.replace(r'^the\s', '')
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].str.split(', or,').str[0]
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].str.split(':').str[0]
fic_nonfic_list['Title'] = fic_nonfic_list['Title'].str.strip()  # Added line to remove leading and trailing spaces

fic_nonfic_list.to_csv('fic_nonfic_list.csv', index=False)



# Read the JSON file into a DataFrame
with open('books.json') as json_file:
    json_data = json.load(json_file)

df_json = pd.DataFrame(json_data)

# Apply the clean_title function to the 'Title' column
df_json['title'] = df_json['title'].apply(clean_title)
df_json['Title'] = df_json['title'].apply(clean_title)
books_json['cleaned_title'] = books_json['title'].apply(clean_title)


# Save the modified DataFrame back to a JSON file
df_json.to_json('books_mod.json', orient='records', lines=True)


#integrate the country data with fic_nonfiction list
country_list = pd.merge(fic_nonfic_list, df_json, left_on='Title', right_on='title', how='left')
country_list = country_list.drop


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

# df_sell['Title'] = df_sell['Title'].str.replace(r'\s*\([^)]*\)\s*', '', regex=True)
# df_sell['Title'] = df_sell['Title'].str.lower()
# df_sell['Title'] = df_sell['Title'].str.replace(r'^the\s', '')
# df_sell['Title'] = df_sell['Title'].str.split(', or,').str[0]
# df_sell['Title'] = df_sell['Title'].str.split(':').str[0]
# df_sell['Title'] = df_sell['Title'].str.strip() 

# Applying the clean_title function to both datasets
df_rank_genre['cleaned_title'] = df_rank_genre['Title'].apply(clean_title)

# Displaying the first few rows after cleaning to verify the changes
df_rank_genre[['Title', 'cleaned_title']].head(), books_json[['title', 'cleaned_title']].head()



#merge dfs together
master_list = pd.merge(df_rank_genre, fic_nonfic_list, on='Title', how='left')
master_list = pd.merge(master_list, df_sell, on='Title', how='left')
master_list = pd.merge(master_list, df_json, on='Title', how='left')
master_list['Approx. sales (in millions)'] = master_list['Approx. sales (in millions)'].fillna('<10')
master_list['Bestseller'] = master_list['Bestseller'].fillna('No')

master_list = master_list[['Title', 'Author', 'countries', 'Rank', 'Genre', 'first_year_published', 'Approx. sales (in millions)', 'Bestseller']]
master_list.to_csv('master_list.csv', index=False)






