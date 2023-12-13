import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import matplotlib.pyplot as plt


df = pd.read_csv('master_list.csv')

# Assuming 'counties' column exists in your DataFrame 'df'
country_counts = df['countries'].value_counts()

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world.set_index('name').join(country_counts)

fig, ax = plt.subplots(1, 1)
world.plot(column='countries', ax=ax, legend=True)
plt.show()


sns.boxplot(x='Genre', y='Approx. sales (in millions)', data=df)
plt.xticks(rotation=45)
plt.show()


df['first_year_published'].value_counts().sort_index().plot(kind='line')
plt.xlabel('Year')
plt.ylabel('Number of Books')
plt.show()



df['Bestseller'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.ylabel('')
plt.show()


author_sales = df.groupby('Author')['Approx. sales (in millions)'].sum().sort_values(ascending=False)
author_sales.head(10).plot(kind='barh')  # Top 10 authors
plt.xlabel('Total Sales (in millions)')
plt.show()



sns.heatmap(df[['Rank', 'Approx. sales (in millions)', 'first_year_published']].corr(), annot=True, fmt=".2f")
plt.show()


genre_over_time = df.groupby(['first_year_published', 'Genre']).size().unstack().fillna(0)
genre_over_time.plot(kind='area', stacked=True)
plt.xlabel('Year')
plt.ylabel('Number of Books')
plt.show()


