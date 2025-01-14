import tkinter as tk
import os
import ast

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def load_correctness_data():
    """Load correctness data passed via environment variable."""
    correctness_data_str = os.getenv("CORRECTNESS_DATA", "[]")
    try:
        return ast.literal_eval(correctness_data_str)
    except Exception as e:
        print(f"Error loading correctness data: {e}")
        return []

def display_scoreboard(score, correctness_data):
    """Display the scoreboard with correctness data."""
    # Create the Tkinter window for the scoreboard
    window = tk.Tk()
    window.title("Scoreboard")
    window.geometry("360x640")
    window.configure(bg="#FFFFFF")

    window_width, window_height = 360, 640
    center_window(window, window_width, window_height)

    # Create canvas for the background
    canvas = tk.Canvas(window, bg="#FFFFFF", height=640, width=360, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Create header area
    canvas.create_rectangle(0.0, 0.0, 360.0, 84.0, fill="#7CA5AE", outline="")
    canvas.create_text(32.0, 30.0, anchor="nw", text="Language Learning", fill="#FFFFFF", font=("Amaranth Regular", 36 * -1))
    canvas.create_text(180.0, 120.0, text="Score Board", fill="black", font=("Amaranth Regular", 18), anchor="center")

    # Add a frame with a vertical scrollbar
    scroll_canvas = tk.Canvas(window, bg="#FFFFFF", highlightthickness=0)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=scroll_canvas.yview)
    scrollable_frame = tk.Frame(scroll_canvas, bg="#FFFFFF")

    # Configure canvas and scrollbar
    scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scroll_canvas.place(x=10, y=140, width=340, height=440)
    scrollbar.place(x=350, y=140, height=440)

    # Bind the frame to adjust scrolling
    def on_frame_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Display congratulatory message and score
    congrats_label = tk.Label(scrollable_frame, text="Congratulations! You completed the quiz.", font=("Arial", 14), wraplength=320, bg="#FFFFFF")
    congrats_label.pack(pady=10)

    total_score_label = tk.Label(scrollable_frame, text=f"Your Total Score: {score}/{len(correctness_data)}", font=("Arial", 12), bg="#FFFFFF")
    total_score_label.pack(pady=5)

    # Display each label, translation, and correctness
    for label, translation, transliteration, correct in correctness_data:
        color = "#7eff22" if correct else "#ff2222"  # Green for correct, red for incorrect
        label_frame = tk.Frame(scrollable_frame, bg=color, padx=10, pady=5)
        label_frame.pack(fill="x", pady=5)

        label_text = f"Label: {label}\nTranslation: {translation}"
        if transliteration:
            label_text += f"\nHint: {transliteration}"

        label_widget = tk.Label(label_frame, text=label_text, font=("Arial", 10), bg=color, anchor="w", wraplength=320, justify="left")
        label_widget.pack(fill="x")

    # Add an exit button
    exit_button = tk.Button(window, text="Exit", font=("Arial", 12), bg="#7CA5AE", fg="#FFFFFF", relief="flat", command=window.quit)
    exit_button.place(x=130, y=600, width=100, height=30)

    # Run the Tkinter window loop
    window.mainloop()

# Load correctness data and score (passed by the quiz.py)
correctness_data = load_correctness_data()
score = int(os.getenv("USER_SCORE", 0))  # Default to 0 if no score is passed

# Display the scoreboard with the score and correctness data
display_scoreboard(score, correctness_data)
