from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import os

# Define paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(r"C:\Users\HEMA DARSHINY\Downloads\installation_opencv-python\object_detection\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to navigate to gui1.py
def navigate_to_gui1():
    gui1_path = r"C:\Users\HEMA DARSHINY\Downloads\installation_opencv-python\object_detection\language.py"
    window.destroy()  # Close the current window
    os.system(f'python "{gui1_path}"')  # Run gui1.py

# Function to center the window on the screen
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

# Initialize the window
window = Tk()
window_width = 335
window_height = 624
center_window(window, window_width, window_height)  # Center the window
window.configure(bg="#7CA5AE")

canvas = Canvas(
    window,
    bg="#7CA5AE",
    height=window_height,
    width=window_width,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# Add button with navigation to gui1.py
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png")
)

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=navigate_to_gui1,  # Navigate to gui1.py
    relief="flat"
)
button_1.place(
    x=79.0,
    y=185.0,
    width=176.0,
    height=142.0
)

canvas.create_text(
    40.0,
    338.0,
    anchor="nw",
    text="Smart Edu Application",
    fill="#FFFFFF",
    font=("Amaranth Regular", 24 * -1)
)

# Prevent window resizing
window.resizable(False, False)

# Start the main loop
window.mainloop()
