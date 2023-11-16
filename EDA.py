import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


df = pd.read_csv('./merged_df.csv')

author_freq = sns.histplot(data=df, x="Author",
             binwidth=3,
             color='skyblue')
author_freq.set(xlabel='number of books written',
                        ylabel='Frequency',
                        title='Authored Books Frequency')
                        
sns.scatterplot(data=df, x="Year", y="Rank",
                                            hue="Bestseller",
                                            palette="Set2")

sns.pairplot(df, hue='Genre')
plt.show()

sns.countplot(x='Genre', data=df)
plt.xticks(rotation=90)
              
plt.show()


g = sns.PairGrid(df, hue='Genre')
g.map_upper(sns.scatterplot)
g.map_diag(sns.histplot)
g.map_lower(sns.kdeplot)
g.add_legend()