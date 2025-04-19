import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

def expected_count_by_genre(csv_file_path):
    """
    Author: Minh Anh Do
    :param csv_file_path: Path to the CSV file containing song data
    :return: Interactive interface for genre, artist, and time analysis
    """
    df = pd.read_csv(csv_file_path)
    df = df.dropna(subset=['genre', 'artist', 'year']).copy()
    df['genre'] = df['genre'].str.lower().str.split(', ')
    df = df.explode('genre')

    # Ask user for input
    genre_input = simpledialog.askstring("Input", "Enter a genre (e.g., pop, rock, hip hop):").lower()
    artist_input = simpledialog.askstring("Input", "Enter an artist name (e.g., Britney Spears):")
    time_input = simpledialog.askstring("Input", "Enter a year or decade (e.g., 1999 or 90s):")

    # Filter based on time input
    if time_input.endswith('s'):
        start_decade = int(time_input[:-1])
        df_time = df[(df['year'] >= start_decade) & (df['year'] < start_decade + 10)]
    else:
        df_time = df[df['year'] == int(time_input)]

    # Apply genre and artist filter
    df_filtered = df_time[(df_time['genre'] == genre_input)]
    if df_filtered.empty:
        messagebox.showinfo("Result", "No data found for the given genre and time period.")
        return

    artist_counts = df_filtered['artist'].value_counts()
    artist_percentages = artist_counts / artist_counts.sum() * 100

    # Plot the graph
    plt.figure(figsize=(12, 6))
    artist_percentages.plot(kind='bar', color='mediumseagreen')
    plt.title(f'P(Artist | Genre={genre_input}, Time={time_input})')
    plt.ylabel('Probability (%)')
    plt.xlabel('Artist')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

    # Ask if user wants more breakdowns
    response = messagebox.askyesno("More Breakdown?", "Do you want to see more probability breakdowns?")
    if response:
        df_filtered_all = df.copy()

        # Joint P(X, T)
        joint_xt = df_filtered_all[(df_filtered_all['artist'] == artist_input) & (df_filtered_all['year'].isin(df_time['year']))]
        p_xt = len(joint_xt) / len(df_filtered_all) * 100

        # P(X, Y=y)
        joint_xy = df_filtered_all[(df_filtered_all['artist'] == artist_input) & (df_filtered_all['genre'] == genre_input)]
        p_xy = len(joint_xy) / len(df_filtered_all) * 100

        # P(X|T)
        df_t = df_time.copy()
        p_x_given_t = len(df_t[df_t['artist'] == artist_input]) / len(df_t) * 100

        # P(Y|X)
        df_x = df_filtered_all[df_filtered_all['artist'] == artist_input]
        p_y_given_x = len(df_x[df_x['genre'] == genre_input]) / len(df_x) * 100 if len(df_x) > 0 else 0

        message = (
            f"P(Artist = {artist_input}, Time = {time_input}): {p_xt:.2f}%\n"
            f"P(Artist = {artist_input}, Genre = {genre_input}): {p_xy:.2f}%\n"
            f"P(Artist = {artist_input} | Time = {time_input}): {p_x_given_t:.2f}%\n"
            f"P(Genre = {genre_input} | Artist = {artist_input}): {p_y_given_x:.2f}%"
        )
        messagebox.showinfo("Probability Breakdown", message)

# GUI setup
root = tk.Tk()
root.withdraw()  # Hide main window
expected_count_by_genre('songs_normalize.csv')