import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
import json


# Load the dataset
@st.cache_data  # This decorator caches the data loading for faster subsequent reloads
def load_data():
    data = pd.read_csv('master_list.csv')
    return data

df = load_data()



# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a Chart:", 
    ['Books by Genre by Decade', 'Book Ranks by Genre'])




# Sidebar for user input features
st.sidebar.header('User Input Features')
# Example: allow user to select a genre
selected_genre = st.sidebar.selectbox('Select a Genre', df['Genre'].unique())

# Main Page
st.title('Literary Data Visualizations')
st.write("Welcome to the Literary Data Visualizations App!")
st.markdown("""
This app provides interactive visualizations of data related to classic literature
...
Feel free to explore the data and visualizations.""")


# Explanation for the raw data checkbox
st.markdown("""
Toggle the checkbox below to view or hide the raw data used in the visualizations.
This can be useful for a more in-depth analysis or to understand the data foundation of the provided charts.
""")
# Checkbox for raw data
if st.checkbox('Show raw data'):
    st.write(df)

st.markdown("""
### Top 10 Most Prolific Authors
The bar chart below showcases the top 10 authors who have written the most books. By hovering over each bar, 
you can see the exact count of books attributed to each author. This visualization helps to quickly identify which authors have been the most productive in terms of literary output.
""")
top_authors = df['Author'].value_counts().head(10)
# Create the bar plot for these top authors
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_authors.index, y=top_authors.values, ax=ax)
ax.set_title('Top 10 Most Prolific Authors by Number of Books')
ax.set_xlabel('Author')
ax.set_ylabel('Number of Books')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_xticklabels(top_authors.index, rotation=45)  # Rotate the author names for better readability

# Display the figure in Streamlit
st.pyplot(fig)


st.markdown("""
### Author Selection and Detailed Views
Select authors from the dropdown menu to see detailed data and visualizations specific to those authors.
You can choose multiple authors to compare their productivity and the distribution of their book ranks.
""")
# Author selection
st.header('Author Selection')
selected_authors = st.multiselect('Select one or more Authors', df['Author'].unique())

# Check if authors are selected
if selected_authors:
    # Filter the dataframe for the selected authors
    author_data = df[df['Author'].isin(selected_authors)]

    # Calculate the best rank for each author
    best_rank_per_author = author_data.groupby('Author')['Rank'].min()

    # Sort the selected authors based on their best rank
    sorted_authors = best_rank_per_author.loc[selected_authors].sort_values().index.tolist()

    # Display data for the selected authors
    st.write(f"Data for selected authors:")
    st.write(author_data)

    # Example visualization: Number of books by each selected author, ordered by best rank
    st.header('Number of Books by Selected Authors')
    author_book_counts = author_data['Author'].value_counts().loc[sorted_authors]
    st.bar_chart(author_book_counts)

    # Example visualization: Rank distribution for the selected authors, ordered by best rank
    st.header('Rank Distribution for Selected Authors')
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Author', y='Rank', data=author_data, order=sorted_authors)
    plt.xticks(rotation=45)
    st.pyplot(plt)
else:
    st.write('No authors selected.')


st.markdown("""
### Map of Books Produced by Country
The interactive choropleth map below illustrates the distribution of books by country. 
The colors represent the logarithmic scale of the book count, allowing for easy comparison across countries.
Simply hover over a country to display the exact number of books produced.
""")
country_counts = df['countries'].value_counts()

# Load geometries
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the country counts onto the world GeoDataFrame
world = world.merge(country_counts.rename('Book Count'), how='left', left_on='name', right_index=True)

# Fill missing values with 0 for countries with no books
world['Book Count'] = world['Book Count'].fillna(0)

# Convert GeoDataFrame to JSON format
geojson = json.loads(world.to_json())

# Plotly Express requires the key in the GeoJSON features, so we set it explicitly
for feature in geojson['features']:
    feature['id'] = feature['properties']['name']

# Calculate the log of the book count, adding 1 to avoid log(0)
log_book_count = np.log10(world['Book Count'] + 1)

# Create the Plotly figure for an interactive map
fig = px.choropleth(world,
                    geojson=geojson,
                    locations='name',
                    featureidkey='id',
                    color=log_book_count,
                    color_continuous_scale='OrRd',
                    hover_name='name',
                    hover_data={'Book Count': True},
                    title='Distribution of Books by Country'
                   )

# Update the figure layout
fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
fig.update_geos(fitbounds="locations", visible=False)

# Define custom tickvals and ticktext for the color bar
tickvals = [np.log10(x) for x in [1, 2, 5, 10, 20, 50, 100, 200, world['Book Count'].max()]]
ticktext = [str(x) for x in [1, 2, 5, 10, 20, 50, 100, 200, world['Book Count'].max()]]

# Update the color bar with custom tick values and tick text
fig.update_layout(coloraxis_colorbar=dict(
    title='Number of Books',
    tickvals=tickvals,
    ticktext=ticktext,
    tickmode='array'
))

# Display the figure in Streamlit
st.header('Map of Books Produced by Country')
st.plotly_chart(fig)