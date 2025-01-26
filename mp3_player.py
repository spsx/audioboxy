import os
import pygame
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess

class MP3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Player")

        # Set the window to full-screen
        self.root.attributes('-fullscreen', True)  # Set the window to full-screen mode
        #self.root.resizable(False, False)

        self.init_pygame()

        # Add a button to select USB drive directory
        self.select_usb_button = tk.Button(
            root, text="Select USB Drive", command=self.select_usb_directory, width=20, height=5
        )
        self.select_usb_button.place(x=50, y=50)  # Use 'place' to control the position

        # Add a button to connect to Bluetooth speaker
        self.connect_bluetooth_button = tk.Button(
            root, text="Connect Bluetooth Speaker", command=self.connect_bluetooth_speaker, width=20, height=5
        )
        self.connect_bluetooth_button.place(x=50, y=150)  # Position below the first button

        # Frame to hold buttons for audio files
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.BOTH, expand=True)

        # Store the current directory and audio files
        self.current_directory = None
        self.audio_files = []

    def init_pygame(self):
        pygame.mixer.init()

    def select_usb_directory(self):
        # Open file dialog starting from /media directory
        directory = filedialog.askdirectory(initialdir='/media', title="Select USB Drive")
        if directory:
            self.current_directory = directory
            self.scan_audio_files()

    def scan_audio_files(self):
        """Scans the selected directory for MP3 and WAV files."""
        if not self.current_directory:
            messagebox.showerror("Error", "No directory selected!")
            return

        self.audio_files = [
            f for f in os.listdir(self.current_directory) if f.lower().endswith((".mp3", ".wav"))
        ]

        if not self.audio_files:
            messagebox.showinfo("No Files", "No MP3 or WAV files found in the selected directory.")
            return

        self.display_audio_buttons()

    def display_audio_buttons(self):
        """Displays a button for each audio file."""
        # Clear previous buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for audio in self.audio_files:
            button = tk.Button(
                self.button_frame,
                text=audio,
                command=lambda file=audio: self.play_audio(file),
                width=20, height=5  # Set button size to 100x80 pixels (approximately)
            )
            button.pack(fill=tk.X, pady=2)

    def play_audio(self, filename):
        """Plays the selected audio file."""
        file_path = os.path.join(self.current_directory, filename)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        messagebox.showinfo("Playing", f"Now playing: {filename}")

    def connect_bluetooth_speaker(self):
        """Connects to a Bluetooth speaker using bluetoothctl."""
        try:
            # Launch bluetoothctl for pairing and connecting
            subprocess.run("bluetoothctl", shell=True)
            messagebox.showinfo("Bluetooth", "Use the terminal to pair and connect to your Bluetooth speaker.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch bluetoothctl: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3PlayerApp(root)
    root.mainloop()
