import json
from tkinter import filedialog

import pandas as pd
import matplotlib.pyplot as plt


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
    plt.figure(figsize=(10, 10))
    plt.barh(top_artists['Artist'], top_artists['HoursListened'])
    plt.xlabel('Hours Listened')
    plt.ylabel(f'Top {top_n} Listened to Artists by You')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
