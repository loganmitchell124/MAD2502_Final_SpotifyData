import pandas as pd
import matplotlib.pyplot as plt

#YEAR -----------------------------------------------------------------------------------------------
def artist_year_graph(csv_file_path):
    """
    Author: Logan Mitchell
    input: file path
    output: data frame
    generates a graph of most popular artist per year
    """
    df = pd.read_csv(csv_file_path)
    top_indices = df.groupby("year")["popularity"].idxmax()
    top_artists_df = df.loc[top_indices, ["year", "artist"]].sort_values("year").reset_index(drop=True)
    lines = []
    for index, row in top_artists_df.iterrows():
        line = f"{row['year']}: {row['artist']}"
        lines.append(line)
    full_text = "\n".join(lines)
    figure, axis = plt.subplots(figsize=(8, len(lines) * 0.4))
    figure.patch.set_facecolor('#e0f2ff')
    axis.set_facecolor('#e0f2ff')
    axis.text(
        0.5, 1, full_text,
        fontsize=12,
        va='top',
        ha='center',
        fontfamily='monospace',
        transform=axis.transAxes
    )
    axis.axis("off")
    plt.title("Most Popular Artist Each Year (2000–2017)", fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()
artist_year_graph("songs_normalize.csv")


#GENRE-----------------------------------------------------------------------------------------------
def genre_year_graph(csv_file_path):
    """
    Author: Logan Mitchell
    input: file path
    output: data frame
    generates a graph sorted by genre popularity throughout year
    """
    df = pd.read_csv(csv_file_path)
    df["genre"] = df["genre"].astype(str).str.split(", ")
    df_exploded = df.explode("genre")
    top_indices = df_exploded.groupby("year")["popularity"].idxmax()
    top_genres_df = df_exploded.loc[top_indices, ["year", "genre"]].sort_values("year").reset_index(drop=True)
    lines = []
    for index, row in top_genres_df.iterrows():
        line = f"{row['year']}: {row['genre']}"
        lines.append(line)
    full_text = "\n".join(lines)
    figure, axis = plt.subplots(figsize=(8, len(lines) * 0.4))
    figure.patch.set_facecolor('#e0f2ff')
    axis.set_facecolor('#e0f2ff')
    axis.text(
        0.5, 1, full_text,
        fontsize=12,
        va='top',
        ha='center',
        fontfamily='monospace',
        transform=axis.transAxes
    )
    axis.axis("off")
    plt.title("Most Popular Genre Each Year (2000-2017)", fontsize=16, pad=20)
    plt.tight_layout()
    plt.show()
genre_year_graph("songs_normalize.csv")

#NOTES-------------------------------------------------------------------------------------------------------------
'''
First going to make a baseline for music popularity from 2000 to 2019. In this, we are specifically looking at 
    (1) most popular genre each year
    (2) most popular artist each year **logan is going to do this 4/15**
We should have a chart showing each year's most popular artist and genre. For this, we are going to use the popularity values already provided and see which artist/genre has the greatest value.
''' 




#GENRE POPULARITY OVER TIME -----------------------------------------------------------------------------------------------
def genre_popularity_over_time(csv_file_path):
    """
    Author: Samantha Cuenot
    :param csv_file_path:
    :return: graph showing popularity of genres over time
    """
    df = pd.read_csv(csv_file_path)

    df['genre'] = df['genre'].str.split(', ')
    df_exploded = df.explode("genre")
    df_exploded_filter = df_exploded[(df_exploded['year'] >= 2000) & (df_exploded['year'] <= 2019)]

    genre_popularity_by_year = df_exploded_filter.groupby(['genre', 'year'])['popularity'].sum().unstack(level=0).fillna(0)

    plt.figure(figsize=(14, 8))
    for genre in genre_popularity_by_year.columns:
        plt.plot(genre_popularity_by_year.index, genre_popularity_by_year[genre], label=genre)

    plt.title('Popularity of genres over time (2000-2019')
    plt.xlabel('Year')
    plt.ylabel('Total Popularity')
    plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
genre_popularity_over_time("songs_normalize.csv")

#NOTES-------------------------------------------------------------------------------------------------------------
'''
This shows the popularity of every genre over time, by adding together the popularity points from the data file. From the graph, we can see that pop is the most popular, so we'll focus on this genre when we look at other characteristics like danceability and tempo.
'''






'''
Then, over the course of all 20 years, who is the most popular artist OVERALL? Whoever the most popular artist is overall, we'll look at the characteristics of their music (danceability, tempo, song duration, etc.)
'''



'''
For the most popular artist and genre OVERALL, what is the average
    - Danceability
    - Tempo
    - Duration of their music (for artist specifically)
'''
