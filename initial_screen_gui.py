import tkinter as tk
from tkinter import ttk
from personal_data import *
from main import *


#MAIN PAGE --------------------------------------------------------------------------------------------------------------------------------------------
def make_main_gui():
    """
    Author: Logan Mitchell
    Creates the main GUI with three different buttons you can press
    """
    window = tk.Tk()
    window.title("Spotify Data Explorer 🎧")
    window.geometry("320x300")
    window.configure(bg="#2e2e2e")
    title_label = tk.Label(
        window,
        text="Spotify Data Explorer 🎧",
        font=("Helvetica", 18, "bold"),
        bg="#2e2e2e",
        fg="white",
        pady=20
    )
    title_label.pack()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Green.TButton",
        foreground="white",
        background="#2e7d32",
        font=("Helvetica", 12),
        padding=10
    )
    style.map("Green.TButton", background=[('active', '#388e3c')])
    btn_width = 25
    btn_explore = ttk.Button(window, text="Explore Dataset", style="Green.TButton", width=btn_width, command=open_explore_dataset)
    btn_upload = ttk.Button(window, text="Upload Your Own Data", style="Green.TButton", width=btn_width, command=upload_personal_data)
    btn_about = ttk.Button(window, text="ℹAbout the Project", style="Green.TButton", width=btn_width, command=about_the_project)

    btn_explore.pack(pady=8)
    btn_upload.pack(pady=8)
    btn_about.pack(pady=8)
    window.mainloop()



#ABOUT PAGE --------------------------------------------------------------------------------------------------------------------------------------------
def about_the_project():
    """
    Author: Samantha Cuenot
    Creates the page where the user can learn more about the project
    """
    about_window = tk.Tk()
    about_window.title("About the Project")
    about_window.geometry("320x300")
    about_window.configure(bg="#2e2e2e")

    title = tk.Label(
        about_window,
        text = "Spotify Data Explorer 🎧",
        font=("Helvetica", 18, "bold"),
        bg="#2e2e2e",
        fg="white",
        pady=20
    )
    title.pack()

    creators_label = tk.Label(
        about_window,
        text = "Created by: Logan Mitchell, Samantha Cuenot, Minh Anh Do",
        font=("Helvetica", 18, "bold"),
        bg="#2e2e2e",
        fg="white",
        pady=20
    )
    creators_label.pack()

    summary_text = (
        "The Spotify Data Explorer is an interactive tool designed to help users explore musical trends, genres, artists, and popularity over time.\n\n"
        "Users can either upload their own personal Spotify Data or use data on Billboard's top 100 from 2000-2019"
    )

    summary_label = tk.Label(
        about_window,
        text = summary_text,
        font=("Helvetica", 11),
        bg="#2e2e2e",
        fg="white",
        justify = "left",
        padx=20
    )
    summary_label.pack(pady=10)

    back_button = ttk.Button(
        about_window,
        text="Back",
        style="Green.TButton",
        command = about_the_project.destroy,
        width=15
    )
    back_button.pack(pady=20)



#EXPLORE DATASET PAGE --------------------------------------------------------------------------------------------------------------------------------------------
def open_explore_dataset():
    """
    Author: Samantha Cuenot
    Creates the page if the user selects to explore the provided dataset
    """

    def handle_year_data():
        artist_year_graph("songs_normalize.csv")
        genre_year_graph("songs_normalize.csv")

    def handle_genre_popularity():
        genre_popularity_over_time("songs_normalize.csv")

    def handle_fav_artist():
        favorite_artist("songs_normalize.csv")

    def handle_relationships():
        relationship_between_variables("songs_normalize.csv")

    explore_window = tk.Toplevel()
    explore_window.title("Explore Dataset Options")
    explore_window.geometry("400x400")
    explore_window.configure(bg="#2e2e2e")
    title = tk.Label(
        explore_window,
        text = "Choose an option",
        font = ("Helvetica", 18, "bold"),
        bg = "#2e2e2e",
        fg = "white",
        pady = 20
    )
    title.pack()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Green.TButton",
        foreground="white",
        background="#2e7d32",
        font=("Helvetica", 12),
        padding=10
    )
    style.map("Green.TButton", background=[('active', '#388e3d')])

    btn_width = 50
    btn_year_data = ttk.Button(explore_window, text="1. Look at the most popular artist and genre each year", style="Green.TButton", width=btn_width, command=handle_year_data)
    btn_genre_pop = ttk.Button(explore_window, text="2. Look at the popularity of genres over time", style="Green.TButton", width=btn_width, command=handle_genre_popularity)
    btn_fav_artist = ttk.Button(explore_window, text="3. Learn more about your favorite artist", style="Green.TButton", width=btn_width, command=handle_fav_artist)
    btn_relationships = ttk.Button(explore_window, text="4. Explore relationships between song characteristics", style="Green.TButton", width=btn_width, command=handle_relationships)

    btn_year_data.pack(pady=8)
    btn_genre_pop.pack(pady=8)
    btn_fav_artist.pack(pady=8)
    btn_relationships.pack(pady=8)

    back_button = ttk.Button(
        explore_window,
        text="Back",
        style="Green.TButton",
        command=explore_window.destroy,
        width=15
    )
    back_button.pack(pady=20)




#UPLOAD PERSONAL DATA PAGE --------------------------------------------------------------------------------------------------------------------------------------------
def upload_personal_data():
    """
    Author: Samantha Cuenot
    Creates the page if the user selects to upload their own personal Spotify data
    """
    upload_window = tk.Toplevel()
    upload_window.title("Upload Your Spotify Data")
    upload_window.geometry("400x300")
    upload_window.configure(bg="#2e2e2e")

    title = tk.Label(
        upload_window,
        text = "Upload Your Spotify JSON File",
        font=("Helvetica", 18, "bold"),
        bg="#2e2e2e",
        fg="white",
        pady=20
    )
    title.pack()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Green.TButton",
        foreground="white",
        background="#2e7d32",
        font=("Helvetica", 12),
        padding=10
    )
    style.map("Green.TButton", background=[('active', '#388e3d')])

    def handle_upload():
        spotify_data = import_json_from_user()
        if spotify_data:
            plot_top_artists(spotify_data)

    upload_button = ttk.Button(
        upload_window,
        text="Upload & Analyze",
        style="Green.TButton",
        command=handle_upload,
        width=20
    )
    upload_button.pack(pady=20)

    back_button = ttk.Button(
        upload_window,
        text="Back",
        style="Green.TButton",
        command=upload_window.destroy,
        width=15
    )
    back_button.pack(pady=20)



if __name__ == "__main__":
    make_main_gui()
