# --- IMPORTS ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

# --- MAIN ENTRY POINT ---
def run_main_program():
    csv_path = "songs_normalize.csv"
    df = pd.read_csv(csv_path)

    generate_all_charts(df)
    open_dashboard_window(df)

# --- GENERATE DASHBOARD CHARTS ---
def generate_all_charts(df):
    # Top Artists
    top_artists = df.groupby('artist')['popularity'].mean().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(4, 4))
    top_artists.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'), ax=ax)
    ax.set_ylabel('')
    plt.title('Top Artists')
    plt.tight_layout()
    fig.savefig("top_artists_chart.png")
    plt.close(fig)

    # Top Genres
    df['genre'] = df['genre'].astype(str).str.replace(r"[\[\]']", "", regex=True).str.strip()
    df['genre'] = df['genre'].str.split(', ')
    df_exploded = df.explode('genre')
    top_genres = df_exploded['genre'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(4, 4))
    top_genres.plot(kind='bar', color=sns.color_palette('muted'), ax=ax)
    plt.title('Top Genres')
    plt.ylabel('Songs')
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig("top_genres_chart.png")
    plt.close(fig)

    # Listening Timeline
    year_counts = df['year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(4, 4))
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o", ax=ax)
    plt.title('Listening Timeline')
    plt.xlabel('Year')
    plt.ylabel('Number of Songs')
    plt.grid(True)
    plt.tight_layout()
    fig.savefig("listening_timeline.png")
    plt.close(fig)

    # Top Tracks
    top_tracks = df.groupby('song')['popularity'].mean().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(4, 4))
    top_tracks.plot(kind='barh', color=sns.color_palette('pastel'), ax=ax)
    plt.title('Top Tracks')
    plt.xlabel('Popularity')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    fig.savefig("top_tracks_chart.png")
    plt.close(fig)

# --- OPEN DASHBOARD ---
def open_dashboard_window(df):
    window = tk.Toplevel()
    window.title("Spotify Interactive Dashboard - Explore Datasets")
    window.geometry("1200x800")
    window.configure(bg="black")

    title_label = tk.Label(window, text="Spotify Interactive Dashboard", font=("Helvetica", 24, "bold"), fg="#1DB954", bg="black")
    title_label.pack(pady=20)

    frame = tk.Frame(window, bg="black")
    frame.pack(padx=20, pady=10)

    charts = [
        ("Top Artists", "top_artists_chart.png", explore_top_artist),
        ("Top Genres", "top_genres_chart.png", explore_top_genre),
        ("Listening Timeline", "listening_timeline.png", explore_listening_timeline),
        ("Top Tracks", "top_tracks_chart.png", explore_top_tracks)
    ]

    for idx, (title, img_file, explore_func) in enumerate(charts):
        img = Image.open(img_file)
        img = img.resize((400, 300))
        img_tk = ImageTk.PhotoImage(img)

        card = tk.Frame(frame, bg="black", bd=2, relief="flat")
        card.grid(row=idx // 2, column=idx % 2, padx=20, pady=20)

        img_label = tk.Label(card, image=img_tk, bg="black")
        img_label.image = img_tk
        img_label.pack()

        title_label = tk.Label(card, text=title, font=("Helvetica", 14, "bold"), fg="white", bg="black")
        title_label.pack(pady=5)

        explore_button = tk.Button(card, text="Explore More", bg="#1DB954", fg="black", font=("Helvetica", 10), command=lambda f=explore_func: f(df))
        explore_button.pack(pady=5)

# --- EXPLORE FUNCTIONS ---
def explore_top_artist(df):
    artist_name = simpledialog.askstring("Explore Top Artist", "Enter artist name:")
    if not artist_name:
        return
    artist_data = df[df['artist'].str.lower() == artist_name.lower()]
    if artist_data.empty:
        show_error_popup(f"No songs found for '{artist_name}'")
        return
    result_window = tk.Toplevel()
    result_window.title(f"Songs by {artist_name}")
    result_window.geometry("700x500")
    result_window.configure(bg="black")

    title_label = tk.Label(result_window, text=f"Songs by {artist_name}", font=("Helvetica", 20, "bold"), fg="#1DB954", bg="black")
    title_label.pack(pady=20)

    table_frame = tk.Frame(result_window, bg="black")
    table_frame.pack(padx=20, pady=10)

    headers = ["Song Name", "Popularity", "Explicit"]
    for col, header in enumerate(headers):
        tk.Label(table_frame, text=header, font=("Helvetica", 14, "bold"), fg="white", bg="black", anchor="w").grid(row=0, column=col, padx=15, pady=5, sticky="w")

    for idx, (_, row) in enumerate(artist_data.iterrows(), start=1):
        song_name = row['song']
        popularity = row['popularity']
        explicit = "Yes" if row['explicit'] else "No"
        tk.Label(table_frame, text=song_name, font=("Helvetica", 12), fg="white", bg="black", anchor="w").grid(row=idx, column=0, padx=15, pady=2, sticky="w")
        tk.Label(table_frame, text=str(popularity), font=("Helvetica", 12), fg="white", bg="black", anchor="w").grid(row=idx, column=1, padx=15, pady=2, sticky="w")
        tk.Label(table_frame, text=explicit, font=("Helvetica", 12), fg="white", bg="black", anchor="w").grid(row=idx, column=2, padx=15, pady=2, sticky="w")

    tk.Button(result_window, text="Close", command=result_window.destroy, bg="#1DB954", fg="black", font=("Helvetica", 12)).pack(pady=20)


def explore_top_genre(df):
    period_input = simpledialog.askstring("Explore Top Genre", "Enter a year (e.g., 2015) or decade (e.g., 2010s):")
    if not period_input:
        return
    try:
        if period_input.endswith('s'):
            decade = int(period_input[:-1])
            df_period = df[(df['year'] >= decade) & (df['year'] < decade + 10)]
        else:
            year = int(period_input)
            df_period = df[df['year'] == year]
    except ValueError:
        show_error_popup("Invalid input! Please enter a valid year or decade.")
        return

    if df_period.empty:
        show_error_popup(f"No data available for '{period_input}'")
        return

    df_period['genre'] = df_period['genre'].astype(str).str.replace(r"[\[\]']", "", regex=True).str.strip()
    df_period['genre'] = df_period['genre'].str.split(', ')
    df_exploded = df_period.explode('genre')
    top_genres = df_exploded['genre'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(8, 6))
    top_genres.plot(kind='bar', color=sns.color_palette('deep'), ax=ax)
    plt.title(f"Top Genres in {period_input}")
    plt.ylabel("Number of Songs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig("top_genres_explore.png")
    plt.close(fig)

    result_window = tk.Toplevel()
    result_window.title(f"Top Genres in {period_input}")
    result_window.geometry("750x600")
    result_window.configure(bg="black")

    img = Image.open("top_genres_explore.png")
    img = img.resize((650, 500))
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(result_window, image=img_tk, bg="black")
    img_label.image = img_tk
    img_label.pack(pady=20)

    close_button = tk.Button(result_window, text="Close", command=result_window.destroy, bg="#1DB954", fg="black", font=("Helvetica", 12))
    close_button.pack(pady=10)


def explore_listening_timeline(df):
    pass


def explore_top_tracks(df):
    pass

# --- ERROR HANDLER ---
def show_error_popup(message):
    error_window = tk.Toplevel()
    error_window.title("Error")
    error_window.geometry("400x200")
    error_window.configure(bg="black")
    tk.Label(error_window, text=message, font=("Helvetica", 14), fg="red", bg="black").pack(pady=40)
    tk.Button(error_window, text="Close", command=error_window.destroy, bg="#1DB954", fg="black", font=("Helvetica", 12)).pack(pady=10)

