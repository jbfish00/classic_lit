import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter



df = pd.read_csv('master_list.csv')


######Map_Plot########
# Assuming 'counties' column exists in your DataFrame 'df'
country_counts = df['countries'].value_counts()

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# Merge the country counts onto the world dataframe
world = world.set_index('name').join(country_counts)
# Create the figure and axis objects
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
# Use logarithmic normalization
norm = mcolors.LogNorm(vmin=world['countries'].min()+1, vmax=world['countries'].max())
# Plotting
world.plot(column='countries', ax=ax, legend=True, norm=norm, cmap='OrRd', missing_kwds={"color": "lightgrey"})
# Create color bar
sm = plt.cm.ScalarMappable(cmap='OrRd', norm=norm)
sm.set_array([])  # You can pass your data in here but it's not necessary
cbar = fig.colorbar(sm, ax=ax)
# Define the tick locations and then set the tick labels
tick_locs = [1, 2, 5, 10, 20, 50, 100, 200]
cbar.set_ticks(tick_locs)
cbar.set_ticklabels([str(int(loc)) for loc in tick_locs])
# Use a function formatter to ensure ticks are displayed in regular numbers
cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: str(int(x))))
ax.set_title('Distribution of Books by Country', fontsize=16, pad=20)
# Remove axis labels
ax.set_axis_off()
# Show the plot
plt.show()


#Number of bestsellers per country
bestsellers_by_country = df[df['Bestseller'] == 'Yes'].groupby('countries').size().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=bestsellers_by_country.index, y=bestsellers_by_country.values)
plt.xticks(rotation=90)
plt.title('Countries with the Most Bestsellers')
plt.xlabel('Country')
plt.ylabel('Number of Bestsellers')
plt.show()

#Top 10 countreis with lowest rank
best_ranked_countries = df.groupby('countries')['Rank'].min().sort_values().head(10)
plt.figure(figsize=(10, 6))
for country, rank in best_ranked_countries.items():
    plt.scatter(country, rank)
    plt.text(country, rank, f'{rank}', ha='center', va='bottom')
plt.title('Countries with the Best Rank')
plt.xlabel('Country')
plt.ylabel('Best Rank')
plt.xticks(rotation=90)
plt.gca().invert_yaxis()  # Invert y-axis to show best rank at top
plt.show()


#Top 10 genres with best rank
best_ranked_genre = df.groupby('Genre')['Rank'].min().sort_values().head(10)
plt.figure(figsize=(10, 6))
for genre, rank in best_ranked_genre.items():
    plt.scatter(genre, rank)
    plt.text(genre, rank, f'{rank}', ha='center', va='bottom')
plt.scatter(best_ranked_genre.index, best_ranked_genre.values)
plt.title('Genres with the Best Rank')
plt.xlabel('Genre')
plt.ylabel('Best Rank')
plt.xticks(rotation=90)
plt.gca().invert_yaxis()  # Invert y-axis to show best rank at top
plt.show()


#Genres with most bestsellers
bestsellers_by_genre = df[df['Bestseller'] == 'Yes'].groupby('Genre').size().sort_values(ascending=False)
bestsellers_by_genre.plot(kind='bar')
plt.title('Genres with Most Bestsellers')
plt.xlabel('Genre')
plt.ylabel('Number of Bestsellers')
plt.xticks(rotation=45)
plt.show()



#Boxplot of Rank and Bestseller status
plt.figure(figsize=(8, 6))
sns.boxplot(x='Bestseller', y='Rank', data=df)
plt.title('Rank Distribution by Bestseller Status')
plt.xlabel('Bestseller Status')
plt.ylabel('Rank')
plt.gca().invert_yaxis()  # To show the best ranks at the top
plt.show()


#Rank of books by author (most prolific)
top_authors = df['Author'].value_counts().head(10).index

# Filter the DataFrame to only include rows with the top 10 authors
df_top_authors = df[df['Author'].isin(top_authors)]

# Create the boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(x='Author', y='Rank', data=df_top_authors)
plt.title('Rank Distribution by Top 10 Authors')
plt.xlabel('Author')
plt.ylabel('Rank')
plt.xticks(rotation=45)  # Rotate the author names for better readability
plt.gca().invert_yaxis()  # To show the best ranks at the top
plt.show()


top_authors = df['Author'].value_counts().head(10)
# Create the bar plot for these top authors
plt.figure(figsize=(12, 6))
sns.barplot(x=top_authors.index, y=top_authors.values)
plt.title('Top 10 Most Prolific Authors by Number of Books')
plt.xlabel('Author')
plt.ylabel('Number of Books')
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.xticks(rotation=45)  # Rotate the author names for better readability
plt.show()




# # Identify the top 10 most prolific authors
# top_authors = df['Author'].value_counts().head(10).index

# # Filter the DataFrame to include only the top authors
# df_top_authors = df[df['Author'].isin(top_authors)]

# # Manually create a mapping of authors to their correct countries
# # Example: author_to_country = {'Charles Dickens': 'United Kingdom', 'C.S. Lewis': 'United Kingdom', ...}
# # Replace the example with actual mappings based on your data
# author_to_country = {
#     'Charles Dickens': 'United Kingdom',
#     'C.S. Lewis': 'United Kingdom',
#     'J.R.R. Tolkien': 'United Kingdom',
#     # Add other authors and their correct countries here
# }

# # Apply the mapping to the DataFrame
# df_top_authors['Country'] = df_top_authors['Author'].map(author_to_country)

# # Recalculate the book counts for each author
# author_book_counts = df_top_authors['Author'].value_counts().reindex(top_authors)

# # Create a unique color for each country
# unique_countries = df_top_authors['Country'].unique()
# palette = dict(zip(unique_countries, sns.color_palette("hls", len(unique_countries))))

# # Create the bar plot
# plt.figure(figsize=(12, 6))
# sns.barplot(x=author_book_counts.index, y=author_book_counts.values, palette=df_top_authors['Country'].map(palette))

# # Set the y-axis to show whole numbers only and add title, labels, etc.
# plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
# plt.title('Top 10 Most Prolific Authors by Number of Books and Country of Origin')
# plt.xlabel('Author')
# plt.ylabel('Number of Books')
# plt.xticks(rotation=45)
# plt.legend(title='Country of Origin', labels=unique_countries)
# plt.show()
















#Auhtors by # of bestsellers
authors_bestsellers = df[df['Bestseller'] == 'Yes'].groupby('Author').size().sort_values(ascending=False).head(10)  # Adjust as needed
authors_bestsellers.plot(kind='barh')
plt.title('Authors with Most Bestsellers')
plt.xlabel('Number of Bestsellers')
plt.ylabel('Author')
plt.show()

#Top 10 books by bestseller status
top_books = df.sort_values('Rank').head(10)
sns.barplot(x='Title', y='Rank', hue='Bestseller', data=top_books)
plt.xticks(rotation=90)
plt.title('Top 10 Books and Their Ranks (Colored by Bestseller Status)')
plt.xlabel('Book Title')
plt.ylabel('Rank')
plt.gca().invert_yaxis()  # Invert y-axis to show best rank at top
plt.legend(title='Bestseller')
plt.show()



#Year vs Rank
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='first_year_published', y='Rank', hue='Bestseller', style='Bestseller')

# Invert the y-axis to show the best rank (1) at the top
plt.gca().invert_yaxis()

# Set the plot title and labels
plt.title('Year of Publication vs. Rank')
plt.xlabel('Year of Publication')
plt.ylabel('Rank')

# Show the plot
plt.show()




#Boxplot genre vs rank
plt.figure(figsize=(12, 6))
sns.boxplot(x='Genre', y='Rank', data=df)
plt.xticks(rotation=45)
plt.title('Distribution of Book Ranks by Genre')
plt.xlabel('Genre')
plt.ylabel('Rank')
plt.show()



#Number of books by genre by decade
# Cleaning the data by dropping NaN values and creating a 'Decade' column
df_cleaned = df.dropna(subset=['first_year_published'])
df_cleaned['Decade'] = (df_cleaned['first_year_published'] // 10 * 10).astype(int)

# Grouping by genre and decade and counting the number of books
genre_by_decade = df_cleaned.groupby(['Genre', 'Decade']).size().reset_index(name='Count')

# Creating a pivot table for the plot
pivot_table = genre_by_decade.pivot(index='Decade', columns='Genre', values='Count')

# Plotting with a unique color for each genre using the 'tab20' colormap
pivot_table.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='tab20')

plt.title('Number of Books in Each Genre by Decade')
plt.xlabel('Decade')
plt.ylabel('Number of Books')
plt.xticks(rotation=45)
plt.legend(title='Genre')
plt.show()



