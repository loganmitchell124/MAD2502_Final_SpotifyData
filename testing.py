import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df=pd.read_csv('songs_normalize.csv')

df.head()
df.tail()
df.sample(10)

df.info()
df.describe()
df['duration_M']=df['duration_ms']/60000
df.describe(include='O')
df.isnull().sum()
df.duplicated().sum()
df[df.duplicated(keep=False)].sort_values(by='song')
df.drop_duplicates(inplace=True)
df.duplicated().sum()
sns.histplot(data=df, x='tempo', bins=30, kde=True)
plt.show()

fig = px.box(df, x='tempo', title='Tempo Distribution')
fig.update_layout(width=800, height=800)  # equivalent to figsize=(8,8)
fig.show()