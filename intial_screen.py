import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk, ImageSequence


def show_about_project():
    about_window = Toplevel()
    about_window.title("About the Project")
    about_window.geometry("700x800")
    about_window.configure(bg="black")

    # Load the animated GIF
    gif_path = "LogoSpotify.gif"
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
        about_window.after(100, update, ind)

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
    import main
    main.run_main_program()

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
    window.geometry("700x800")
    window.configure(bg="black")

    title_label = tk.Label(window, text="Spotify Interactive Dashboard",
                           font=("Helvetica", 28, "bold"), fg="#1DB954", bg="black")
    title_label.pack(pady=20)

    gif_path = "Nt6v.gif"
    gif = Image.open(gif_path)

    frames = []
    try:
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGBA')
            frames.append(ImageTk.PhotoImage(frame))
    except EOFError:
        pass

    gif_label = tk.Label(window, bg="black")
    gif_label.pack(pady=10)

    def update_gif(ind):
        frame = frames[ind]
        gif_label.configure(image=frame)
        ind = (ind + 1) % len(frames)
        window.after(100, update_gif, ind)

    update_gif(0)

    # --- Buttons ---
    button_frame = tk.Frame(window, bg="black")
    button_frame.pack(pady=20)

    about_button = tk.Button(button_frame, text="About the Project", command=show_about_project,
                              font=("Helvetica", 14), width=30, height=2, bg="#1DB954", fg="black")
    about_button.pack(pady=10)

    explore_button = tk.Button(button_frame, text="Explore General Datasets", command=explore_data_sets,
                                font=("Helvetica", 14), width=30, height=2, bg="#1DB954", fg="black")
    explore_button.pack(pady=10)

    analyze_button = tk.Button(button_frame, text="Analyze Your Own Data", command=analyze_own_data,
                                font=("Helvetica", 14), width=30, height=2, bg="#1DB954", fg="black")
    analyze_button.pack(pady=10)

    window.mainloop()

# Run the app
main_menu()
