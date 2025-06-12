import tkinter as Tk
from tkinter import Label
from PIL import Image, ImageTk, ImageSequence
import pygame
from pygame import mixer
import os
import threading

# Initialize Pygame mixer for music
mixer.init()

# Function to play GIF without blocking the main program
def play_gif():
    root = Tk.Tk()
    root.geometry("1000x500")
    root.title("GIF Player")

    # Load GIF frames
    img = Image.open("gui.gif")
    frames = [ImageTk.PhotoImage(frame.resize((1000, 500))) for frame in ImageSequence.Iterator(img)]

    # Label to display GIF
    lbl = Label(root)
    lbl.place(x=0, y=0)

    # Function to animate GIF
    def animate_gif(frame_idx=0):
        lbl.config(image=frames[frame_idx])
        lbl.image = frames[frame_idx]  # Keep reference
        root.after(50, animate_gif, (frame_idx + 1) % len(frames))  # Loop GIF

    # Play music if file exists
    if os.path.exists("music.mp3"):
        mixer.music.load("music.mp3")
        mixer.music.play()

    # Start animation
    animate_gif()
    
    # Run the GUI for a limited time, then close
    root.after(5000, root.destroy)  # Close after 5 seconds (adjust as needed)
    root.mainloop()

# Function to start GIF in a separate thread
def start_intro():
    thread = threading.Thread(target=play_gif)
    thread.start()
