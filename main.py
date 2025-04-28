from tkinter import simpledialog

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import tkinter as tk
from PIL import Image, ImageTk


# SUMMARY OF DATA -----------------------------------------------------------------------------------------------
def summarize_song_dataset(csv_file_path):
    """
    Author: Minh Anh Do
    :param csv_file_path
    :return: Summary of dataset including time range, genre list, song count, and musical attributes
    """

    df = pd.read_csv(csv_file_path)
    total_songs = len(df)
    min_year = df['year'].min()
    max_year = df['year'].max()

    unique_genres = df['genre'].dropna().str.lower().str.split(', ')
    exploded_genres = unique_genres.explode().unique()
    genre_list = sorted([g for g in exploded_genres if g != 'set()'])

    music_attributes = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
    ]

    print(f"🎵 Total Songs: {total_songs}")
    print(f"📅 Time Range: {min_year} to {max_year}")
    print(f"🎼 Number of Unique Genres: {len(genre_list)}")
    print(f"🎧 Genres Included: {', '.join(genre_list)}")
    print(f"🔊 Musical Attributes: {', '.join(music_attributes)}")
# NOTES -----------------------------------------------------------------------------------------------
""" The code above will show the summary of data set 'songs_normalize' 
    With significant data like genre, period, and music attributes """

""" It will be useful for some features implemented later which will ask for input
    The output will vary based on users' input """





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

    figure.savefig("artist_year_graph.png")
    plt.close(figure)

    img_window = tk.Toplevel()
    img_window.title("Most Popular Artist Each Year")
    img_window.geometry("850x700")
    img_window.configure(bg='#2e2e2e')

    img = Image.open("artist_year_graph.png")
    img = img.resize((800, 600))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(img_window, image=img_tk, bg='#2e2e2e')
    label.image = img_tk
    label.pack(pady=20)

    close_button = tk.Button(img_window, text="Close", bg="2e7d32", fg="white", font=("Helvetica", 12), command=img_window.destroy)
    close_button.pack(pady=10)


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

    figure.savefig("genre_year_graph.png")
    plt.close(figure)

    img_window = tk.Toplevel()
    img_window.title("Most Popular Genre Each Year")
    img_window.geometry("850x700")
    img_window.configure(bg='#2e2e2e')

    img = Image.open("genre_year_graph.png")
    img = img.resize((800, 600))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(img_window, image=img_tk, bg='#2e2e2e')
    label.image = img_tk
    label.pack(pady=20)

    close_button = tk.Button(img_window, text="Close", bg="2e7d32", fg="white", font=("Helvetica", 12), command=img_window.destroy)
    close_button.pack(pady=10)
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

    figure, axis = plt.subplots(figsize=(14, 8))
    for genre in genre_popularity_by_year.columns:
        axis.plot(genre_popularity_by_year.index, genre_popularity_by_year[genre], label=genre)

    axis.set_title('Popularity of genres over time (2000-2019')
    axis.set_xlabel('Year')
    axis.set_ylabel('Total Popularity')
    axis.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
    axis.grid(True)
    figure.tight_layout()

    figure.savefig("genre_popularity.png")
    plt.close(figure)

    img_window = tk.Toplevel()
    img_window.title("Most Popular Artist Each Year")
    img_window.geometry("850x700")
    img_window.configure(bg='#2e2e2e')

    img = Image.open("genre_popularity.png")
    img = img.resize((800, 600))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(img_window, image=img_tk, bg='#2e2e2e')
    label.image = img_tk
    label.pack(pady=20)

    close_button = tk.Button(img_window, text="Close", bg="2e7d32", fg="white", font=("Helvetica", 12), command=img_window.destroy)
    close_button.pack(pady=10)
#NOTES-------------------------------------------------------------------------------------------------------------
'''
This shows the popularity of every genre over time, by adding together the popularity points from the data file. From the graph, we can see that pop is the most popular, so we'll focus on this genre when we look at other characteristics like danceability and tempo.
'''




#FAVORITE ARTIST-------------------------------------------------------------------------------------------------------------
def favorite_artist(csv_file_path):
    """
    Author: Samantha Cuenot
    :param csv_file_path:
    :return: table showing characteristics of the user's favorite artist
    """
    df = pd.read_csv(csv_file_path)

    root = tk.Tk()
    root.withdraw()
    artist_name = simpledialog.askstring('Favorite Artist', 'Enter the name of your favorite artist')

    if not artist_name:
        return None

    artist_data = df[df['artist'].str.lower() == artist_name.lower()]

    if artist_data.empty:
        error_window = tk.Toplevel()
        error_window.title("Error")
        error_label = tk.Label(error_window, text=f'No data found for artist {artist_name}.', font=('Helvetica', 14), fg='red')
        error_label.pack(pady=20)
        return

    avg_popularity = artist_data['popularity'].mean()
    avg_tempo = artist_data['tempo'].mean()
    avg_danceability = artist_data['danceability'].mean()

    genres = artist_data['genre'].dropna().str.split(', ')
    genres = genres.explode()
    most_common_genre = genres.mode().iloc[0] if not genres.empty else "N/A"

    stats_window = tk.Toplevel()
    stats_window.title(f"Stats for {artist_name}")
    stats_window.geometry("450x400")
    stats_window.configure(bg='#2e2e2e')

    title = tk.Label(stats_window, text=f'{artist_name} Summary', font=('Helvetica', 18, "bold"), bg='#2e2e2e', fg='white', pady=20)
    title.pack()

    stats_text = (
        f"Average Popularity: {round(avg_popularity, 2)}\n"
        f"Most Frequent Genre: {most_common_genre}\n"
        f"Average Tempo: {round(avg_tempo, 2)}\n"
        f"Average Danceability: {round(avg_danceability, 2)}\n"
    )

    stats_label = tk.Label(stats_window, text=stats_text, font=("Helvetica", 14), bg='#2e2e2e', fg='white', justify='left', pady=20)
    stats_label.pack(pady=10)

    close_button = tk.Button(stats_window, text="Close", bg="2e7d32", fg="white", font=("Helvetica", 12), command=stats_window.destroy)
    close_button.pack(pady=10)
#NOTES-------------------------------------------------------------------------------------------------------------
'''
Gathers data on the user's favorite artist and displays it.
'''



# EXPECTED COUNT -----------------------------------------------------------------------------------------------
def genre_artist_distribution(csv_file_path):
    """
    Author: Minh Anh Do
    :param csv_file_path: Path to the CSV file

    """
    df = pd.read_csv(csv_file_path)
    df = df.dropna(subset=['genre', 'artist', 'year']).copy()
    df['genre'] = df['genre'].str.lower().str.split(', ')
    df = df.explode('genre')

    # --- Get user input ---
    time_input = input("Enter a year or decade: ").strip().lower()
    if time_input.endswith('s'):
        start_decade = int(time_input[:-1])
        df_time = df[(df['year'] >= start_decade) & (df['year'] < start_decade + 10)]
    else:
        year = int(time_input)
        df_time = df[df['year'] == year]

    if df_time.empty:
        print("No data available for the given time period.")
        return

    # --- Plot: Genre distribution in the given time period ---
    genre_counts = df_time['genre'].value_counts()
    genre_percentages = genre_counts / genre_counts.sum() * 100

    plt.figure(figsize=(12, 6))
    genre_percentages.plot(kind='bar', color='skyblue')
    plt.title(f"Probability of Each Genre in {time_input}")
    plt.ylabel("Probability (%)")
    plt.xlabel("Genre")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # --- Ask user for a genre Y ---
    genre_input = input("Enter a genre to explore artist distribution: ").lower()
    genre_df = df_time[df_time['genre'] == genre_input]

    if genre_df.empty:
        print(f"No songs found for genre '{genre_input}' in {time_input}.")
        return

    # --- Plot: Artist distribution within that genre ---
    artist_counts = genre_df['artist'].value_counts()
    artist_percentages = artist_counts / artist_counts.sum() * 100

    plt.figure(figsize=(12, 6))
    artist_percentages.plot(kind='bar', color='mediumseagreen')
    plt.title(f"Probability of Artists Given Genre = '{genre_input}' in {time_input}")
    plt.ylabel("Probability (%)")
    plt.xlabel("Artist")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
#NOTES-------------------------------------------------------------------------------------------------------------
''' This function analyzes music data to show two main visualizations:

1. Genre Popularity Over Time (T):
   - Given a user-specified time period (T), either a specific year (e.g., 2005) or a decade (e.g., 90s),
   - It calculates the probability distribution of genres during that time.
   - This answers the question: 
     > "If a song is chosen at random from period T, what is the probability that it belongs to genre Y?"

2. Artist Distribution Within a Genre (Y):
   - After the user selects a genre Y (e.g., pop), the function filters songs from that genre in the chosen time period.
   - It then displays the probability distribution of artists within that genre.
   - This answers the question:
     > "If a song is randomly picked from genre Y in time T, what is the probability that it is by artist X?" '''


def show_slideshow(image_paths, titles):
    """
    Show more than one image in single window
    """
    slideshow_window = tk.Toplevel()
    slideshow_window.title("Relationships Between Variables")
    slideshow_window.geometry("400x400")
    slideshow_window.configure(bg="#2e2e2e")

    images = []
    for path in image_paths:
        img = Image.open(path)
        img = img.resize((300, 300))
        images.append(ImageTk.PhotoImage(img))

    current_index = tk.IntVar(value=0)

    title_label = tk.Label(slideshow_window, text=titles[0], font=("Helvetica", 12), bg="#2e2e2e", fg="white", pady=10)
    title_label.pack()

    image_label = tk.Label(slideshow_window, image=images[0], bg="#2e2e2e")
    image_label.pack(pady=10)

    def show_image(index):
        image_label.config(image=images[index])
        image_label.image = images[index]
        title_label.config(text=titles[index])

    def next_image():
        idx = current_index.get()
        if idx < len(images) - 1:
            current_index.set(idx + 1)
            show_image(current_index.get())

    def prev_image():
        idx = current_index.get()
        if idx > 0:
            current_index.set(idx - 1)
            show_image(current_index.get())

    button_frame = tk.Frame(slideshow_window, bg="#2e2e2e")
    button_frame.pack(pady=10)

    back_button = tk.Button(button_frame, text="Back", command=prev_image, bg='#2e7d32', fg='black', font=("Helvetica", 12), width=10)
    back_button.grid(row=0, column=0, padx=10)

    next_button = tk.Button(button_frame, text='Next', command=next_image, bg='#2e7d32', fg='black', font=("Helvetica", 12),width=10)
    next_button.grid(row=0, column=1, padx=10)

    close_button = tk.Button(slideshow_window, text="Close", bg='#2e7d32', fg='black', font=("Helvetica", 12), command=slideshow_window.destroy)
    close_button.pack(pady=10)



# SCATTERPLOT - RELATIONSHIP?
def relationship_between_variables(csv_file_path):
    """
    Author: Minh Anh Do
    Explore how valence, tempo, and liveness influence danceability and popularity.
    Also checks:
      - Correlation between danceability and popularity.
      - Popularity differences between explicit vs. non-explicit songs.
      - Correlations between energy & loudness, and danceability & tempo.

    Graphs include combo plots, scatterplots, grouped bar charts, and a treemap.
    """

    df = pd.read_csv(csv_file_path)

    # Drop missing values in relevant columns
    df = df.dropna(subset=['valence', 'tempo', 'liveness', 'danceability', 'popularity'])

    # Correlation heatmap between selected features
    features = ['valence', 'tempo', 'liveness', 'danceability', 'popularity']
    corr = df[features].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix Between Musical Attributes')
    fig.tight_layout()
    fig.savefig('correlation_heatmap.png')
    plt.close(fig)

    # Danceability vs Popularity Scatterplot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='danceability', y='popularity', alpha=0.5, ax=ax)
    ax.set_title('Danceability vs Popularity')
    fig.tight_layout()
    fig.savefig('danceability_vs_popularity.png')
    plt.close(fig)
    '''
    # Explicit vs Non-Explicit Genre Distribution Treemap
    df_exp = df.dropna(subset=['genre', 'explicit']).copy()
    df_exp['genre'] = df_exp['genre'].str.lower().str.split(', ')
    df_exp = df_exp.explode('genre')
    genre_explicit = df_exp.groupby(['explicit', 'genre']).size().reset_index(name='count')
    
    # Get full genre set to ensure both plots share same axes
    all_genres = sorted(df_exp['genre'].dropna().unique())

    for exp in [True, False]:
        data = genre_explicit[genre_explicit['explicit'] == exp].set_index('genre').reindex(all_genres, fill_value=0).reset_index()
        sizes = data['count'].tolist()

        # Skip plotting if sizes contain all zeros or only one non-zero value
        if sum(sizes) == 0 or len([s for s in sizes if s > 0]) < 2:
            print(f"Insufficient data to plot for {'explicit' if exp else 'non-explicit'} songs.")
            continue

        total = sum(sizes)
        norm_sizes = [s / total for s in sizes if s > 0]
        filtered_labels = [f"{g}\n{round(c / total * 100)}%" for g, c in zip(data['genre'], sizes) if c > 0]

        fig, ax = plt.subplots(figsize=(8, 6))
        squarify.plot(sizes=norm_sizes, label=filtered_labels, alpha=.8, ax=ax)
        title = 'Explicit Songs' if exp else 'Non-Explicit Songs'
        ax.set_title(f"Genre Distribution: {title}")
        plt.axis('off')
        fig.tight_layout()

        file_name = f"tree_map{'explicit' if exp else 'non-explicit'}.png"
        fig.savefig(file_name)
        plt.close(fig)
        show_image_in_window(file_name, f"Genre Treemap - {'Explicit' if exp else 'Non-explicit'} Songs")'''

    # Energy vs Loudness
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='energy', y='loudness', alpha=0.5, ax=ax)
    ax.set_title('Energy vs Loudness')
    fig.tight_layout()
    fig.savefig('energy_vs_loudness.png')
    plt.close(fig)

    # Danceability vs Tempo
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='danceability', y='tempo', ax=ax)
    ax.set_title('Danceability vs Tempo')
    fig.tight_layout()
    fig.savefig('danceability_vs_tempo.png')
    plt.close(fig)

    image_paths = [
        'correlation_heatmap.png',
        'danceability_vs_popularity.png',
        'energy_vs_loudness.png',
        'danceability_vs_tempo.png',
    ]
    titles = [
        "Correlation Heatmap",
        "Danceability vs Popularity",
        "Energy vs Loudness",
        "Danceability vs Tempo",
    ]

    show_slideshow(image_paths, titles)

'''
    # Grouped bar chart: Popularity over decade by genre
    df_decade = df_exp.dropna(subset=['year']).copy()
    df_decade['decade'] = (df_decade['year'] // 10) * 10
    top_genres = df_decade['genre'].value_counts().nlargest(5).index
    df_filtered = df_decade[df_decade['genre'].isin(top_genres)]

    genre_decade_avg = df_filtered.groupby(['decade', 'genre'])['popularity'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=genre_decade_avg, x='decade', y='popularity', hue='genre')
    ax.set_title('Average Popularity by Genre and Decade')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    fig.tight_layout()
    fig.savefig('popularity_by_genre_decade.png')
    plt.close(fig)
    show_image_in_window('popularity_by_genre_decade.png', 'Popularity by Genre')'''
#NOTES-------------------------------------------------------------------------------------------------------------
''' With valence, tempo, and liveness, predict aspects of a song's danceability and/or popularity
    - Is there a relationship any correlation between danceability and popularity? '''

''' A combo chart that demonstrates the relationship between variables'''
''' Are explicit songs more popular on average than non-explicit ones?
 Is there a correlation between energy and loudness, or danceability and tempo?
  What were the top 5 most common genres in each decade?
Why it’s interesting: Reveals how music trends shift over time.

Graph type: Grouped bar chart (x = decade, color = genre)
'''