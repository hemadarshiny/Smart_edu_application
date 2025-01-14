import tkinter as tk
from googletrans import Translator
import os
import re
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from pypinyin import lazy_pinyin, Style
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk 
from tkinter import ttk

def navigate_to_quiz(quiz_data, window):
    # Save the quiz data to a temporary file or pass directly to the quiz module
    quiz_path = r"C:\Users\HEMA DARSHINY\Downloads\installation_opencv-python\object_detection\quiz.py"
    os.environ["QUIZ_DATA"] = str(quiz_data)  # Pass data via environment variable
    window.destroy()  # Destroy the current Tkinter window
    os.system(f'python "{quiz_path}"')

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def display_labels(labels):
    # Get the selected language from the environment variable
    selected_language = os.getenv("SELECTED_LANGUAGE", "en")


    # Translator initialization
    translator = Translator()

    # Translate the labels
    translations = []
    quiz_data = []  # Store data for the quiz
    for label in set(labels):  # Remove duplicates
        translation = translator.translate(label, src="en", dest=selected_language).text

        # Add transliteration for specific languages
        if selected_language == "zh-cn":
            # Extract only Chinese characters
            chinese_chars = ''.join(re.findall(r'[\u4e00-\u9fff]+', translation))
            pinyin_translation = ' '.join(lazy_pinyin(chinese_chars))  # Pinyin transliteration
            translations.append(f"{label} ---> {chinese_chars} ({pinyin_translation})")
            quiz_data.append((label, chinese_chars, pinyin_translation))

        elif selected_language == "ta":
            # Transliteration for Tamil
            transliteration = transliterate(translation, sanscript.TAMIL, sanscript.ITRANS)
            translations.append(f"{label} ---> {translation.lower()} ({transliteration.lower()})")
            quiz_data.append((label, translation, transliteration.lower()))
        else:
            # Other languages
            translations.append(f"{label} ---> {translation}")
            quiz_data.append((label, translation, ""))
    

    # Create a Tkinter window with the desired UI
    window = tk.Tk()
    window.title("Detected Objects")
    window.geometry("360x640")  # Set the window size
    window.configure(bg="#FFFFFF")

    window_width, window_height = 360, 640
    center_window(window, window_width, window_height)

    # Create canvas for the background
    canvas = tk.Canvas(window, bg="#FFFFFF", height=640, width=360, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)


    # Create header area
    canvas.create_rectangle(0.0, 0.0, 360.0, 84.0, fill="#7CA5AE", outline="")
    canvas.create_text(32.0, 30.0, anchor="nw", text="Language Learning", fill="#FFFFFF", font=("Amaranth Regular", 36 * -1))

    canvas.create_text(180.0, 120.0, text="New Vocabularies", fill="black", font=("Amaranth Regular", 18), anchor="center")

    # Create a label to display the translations
    detected_text = '\n'.join(sorted(translations))
    label = tk.Label(window, text=detected_text, font=("Arial", 12), padx=10, pady=10, justify="left", bg="#FFFFFF")
    label.place(x=10, y=140)

    # Create a modern button using ttk
    navigate_button = ttk.Button(window, text="Generate quiz", command=lambda: navigate_to_quiz(quiz_data, window))

    # Customize the button style
    style = ttk.Style()
    style.configure("Modern.TButton", 
                    font=("Arial", 12),
                    padding=10,
                    relief="flat",
                    background="#4CAF50",  # Green background
                    foreground="black",    # White text
                    width=15)

    # Apply the style to the button
    navigate_button.configure(style="Modern.TButton")

    # Center the button horizontally and place it below the label
    navigate_button.place(relx=0.5, y=350, anchor="center")

    # Add an image at the bottom
    image_path = r"C:\Users\HEMA DARSHINY\Downloads\installation_opencv-python\object_detection\bottom_vol.png"
    original_image = Image.open(image_path)

    # Resize the image to fit the width of the window (360px)
    resized_image = original_image.resize((360, int(original_image.height * 360 / original_image.width)))

    # Convert the resized image to PhotoImage
    image_bottom = ImageTk.PhotoImage(resized_image)

    # Place the image at the bottom center of the window
    canvas.create_image(180, 580, image=image_bottom)  # Centered at the bottom

    window.resizable(False, False)
    window.mainloop()