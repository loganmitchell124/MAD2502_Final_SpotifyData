import pandas as pd

df = pd.read_csv('songs_normalize.csv')

'''
First going to make a baseline for music popularity from 2000 to 2019. In this, we are specifically looking at 
    (1) most popular genre each year
    (2) most popular artist each year
'''




'''
Then, within the most popular genre and artist, we are going to look at their music characteristics, including
    - Danceability
    - Tempo
    - Average duration of their music (for artist specifically)
'''