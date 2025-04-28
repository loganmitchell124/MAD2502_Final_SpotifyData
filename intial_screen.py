import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import Image, ImageTk, ImageSequence

def show_about_project():
    about_window = Toplevel()
    about_window.title("About the Project")
    about_window.geometry("700x800")
    about_window.configure(bg="black")

    # Load the animated GIF
    gif_path = "LogoSpotify.gif"  # <--- your renamed GIF file
    gif = Image.open(gif_path)

    frames = []
    try:
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGBA')
            frames.append(ImageTk.PhotoImage(frame))
    except EOFError:
        pass

    gif_label = tk.Label(about_window, bg="black")
    gif_label.pack(pady=20)

    def update(ind):
        frame = frames[ind]
        gif_label.configure(image=frame)
        ind = (ind + 1) % len(frames)
        about_window.after(100, update, ind)  # 100ms between frames, adjust if you want faster/slower

    update(0)

    # Team names
    creators = tk.Label(about_window, text="Created by:\nLogan Mitchell, Samantha Cuenot, Minh Anh Do",
                        font=("Helvetica", 16, "bold"), fg="white", bg="black")
    creators.pack(pady=10)

    # Project summary
    summary = tk.Label(about_window, text="Project Summary:\nThis interactive Spotify dashboard allows users to\n"
                                          "explore their music data with visualizations.\n\n"
                                          "Users can view their most played artists, tracks, and genres,\n"
                                          "as well as analyze their listening trends.",
                       font=("Helvetica", 14), fg="white", bg="black", justify="center")
    summary.pack(pady=10)

def explore_data_sets():
    import mainmenu  # Import your mainmenu.py file (make sure it's in the same folder)
    mainmenu.run_main_program()

def analyze_own_data():
    from personal_data import import_json_from_user, plot_top_artists

    data = import_json_from_user()
    if data:
        plot_top_artists(data)
    else:
        from tkinter import messagebox
        messagebox.showerror("Error", "No data was loaded. Please try again.")

def main_menu():
    window = tk.Tk()
    window.title("Spotify Interactive Dashboard")
    window.geometry("700x600")
    window.configure(bg="black")

    title_label = tk.Label(window, text="Spotify Interactive Dashboard",
                           font=("Helvetica", 28, "bold"), fg="#1DB954", bg="black")
    title_label.pack(pady=40)

    about_button = tk.Button(window, text="About the Project", command=show_about_project,
                              font=("Helvetica", 14), width=30, height=2, bg="#1DB954", fg="black")
    about_button.pack(pady=10)

    explore_button = tk.Button(window, text="Explore General Datasets", command=explore_data_sets,
                                font=("Helvetica", 14), width=30, height=2, bg="#1DB954", fg="black")
    explore_button.pack(pady=10)

    analyze_button = tk.Button(window, text="Analyze Your Own Data", command=analyze_own_data,
                                font=("Helvetica", 14), width=30, height=2, bg="#1DB954", fg="black")
    analyze_button.pack(pady=10)

    window.mainloop()

# Run the app
main_menu()
