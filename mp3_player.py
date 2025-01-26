import os
import pygame
import tkinter as tk
from tkinter import messagebox, filedialog

class MP3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("800x480")

        self.init_pygame()

        # Add a button to select USB drive directory
        self.select_usb_button = tk.Button(
            root, text="Select USB Drive", command=self.select_usb_directory
        )
        self.select_usb_button.pack(pady=10)

        # Frame to hold buttons for MP3 files
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # Store the current directory and mp3 files
        self.current_directory = None
        self.mp3_files = []

    def init_pygame(self):
        pygame.mixer.init()

    def select_usb_directory(self):
        directory = filedialog.askdirectory(title="Select USB Drive")
        if directory:
            self.current_directory = directory
            self.scan_mp3_files()

    def scan_mp3_files(self):
        """Scans the selected directory for MP3 files."""
        if not self.current_directory:
            messagebox.showerror("Error", "No directory selected!")
            return

        self.mp3_files = [
            f for f in os.listdir(self.current_directory) if f.lower().endswith(".mp3")
        ]

        if not self.mp3_files:
            messagebox.showinfo("No Files", "No MP3 files found in the selected directory.")
            return

        self.display_mp3_buttons()

    def display_mp3_buttons(self):
        """Displays a button for each MP3 file."""
        # Clear previous buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for mp3 in self.mp3_files:
            button = tk.Button(
                self.button_frame,
                text=mp3,
                command=lambda file=mp3: self.play_mp3(file),
            )
            button.pack(fill=tk.X, pady=2)

    def play_mp3(self, filename):
        """Plays the selected MP3 file."""
        file_path = os.path.join(self.current_directory, filename)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        messagebox.showinfo("Playing", f"Now playing: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3PlayerApp(root)
    root.mainloop()
