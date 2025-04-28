import json
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk



def import_json_from_user():
    """
    Author: Samantha Cuenot
    Summary: takes user spotify input and converts it to json
    """
    file_path = filedialog.askopenfilename(
        title="Select your Spotify JSON File",
        filetypes=(("JSON Files", "*.json"),)
    )
    if not file_path:
        return None

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON")
        return None
    except Exception as e:
        print("Error: " + str(e))
        return None


def plot_top_artists(data, top_n = 10):
    """
    Author: Samantha Cuenot
    Summary: takes user spotify data and plots top n artists based on the ms streamed
    """
    artist_listen_time = {}

    for entry in data:
        artist = entry['artistName']
        ms_played = entry['msPlayed']
        if artist in artist_listen_time:
            artist_listen_time[artist] += ms_played
        else:
            artist_listen_time[artist] = ms_played

    # Convert the ms to hours
    artist_hours = {artist: ms / (1000 * 60 * 60) for artist, ms in artist_listen_time.items()}
    artist_df = pd.DataFrame(list(artist_hours.items()), columns=['Artist', 'HoursListened'])
    artist_df.sort_values('HoursListened', ascending=False, inplace=True)

    top_artists = artist_df.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top_artists['Artist'], top_artists['HoursListened'])
    ax.set_xlabel('Hours Listened')
    ax.set_ylabel(f'Top {top_n} Listened to Artists by You')
    ax.invert_yaxis()
    fig.tight_layout()

    fig.savefig('top_artists_plot.png')
    plt.close(fig)

    img_window = tk.Toplevel()
    img_window.title("Your Spotify Top Artists")
    img_window.geometry("850x700")
    img_window.configure(bg="#2e2e2e")

    img = Image.open("top_artists_plot.png")
    img = img.resize((800, 600))
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(img_window, image=img_tk, bg="#2e2e2e")
    label.image = img_tk
    label.pack(pady=20)

    close_button = tk.Button(img_window, text="Close", bg="2e7d32", fg="white", font=("Helvetica", 12), command=img_window.destroy)
    close_button.pack(pady=10)
