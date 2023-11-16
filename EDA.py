import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

merged = sns.load_dataset('./merged_df.csv')
author_freq = sns.histplot(data=merged, x="Author",
             binwidth=3,
             color='skyblue')
author_freq.set(xlabel='number of books written',
                        ylabel='Frequency',
                        title='Authored Books Frequency')
