import tkinter as tk
from tkinter import ttk

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
    btn_explore = ttk.Button(window, text="Explore Dataset", style="Green.TButton", width=btn_width)
    btn_upload = ttk.Button(window, text="Upload Your Own Data", style="Green.TButton", width=btn_width)
    btn_about = ttk.Button(window, text="ℹAbout the Project", style="Green.TButton", width=btn_width)

    btn_explore.pack(pady=8)
    btn_upload.pack(pady=8)
    btn_about.pack(pady=8)
    window.mainloop()

if __name__ == "__main__":
    make_main_gui()
