import tkinter as tk
import os
import ast  # For parsing the string representation of quiz data
import random
import subprocess  # To run the scoreboard script
from PIL import Image, ImageTk 

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def load_quiz_data():
    """Load quiz data passed via environment variable."""
    quiz_data_str = os.getenv("QUIZ_DATA", "[]")
    try:
        # Parse the string representation of the list
        return ast.literal_eval(quiz_data_str)
    except Exception as e:
        print(f"Error loading quiz data: {e}")
        return []

def start_quiz(quiz_data):
    """Start the quiz interface."""
    current_question_index = [0]  # Use a list to allow modification within nested functions
    score = [0]  # User's score
    selected_answers = []  # Store selected answers for correctness tracking

    def next_question():
        # Clear the previous question
        for widget in question_frame.winfo_children():
            widget.destroy()
        question_title = tk.Label(
        question_frame,
        text="Answer the Questions",
        font=("Amaranth Regular", 18),
        fg="black",
        bg="#FFFFFF",
        anchor="center"
    )
        question_title.pack(pady=(10, 20))

        # Check if we have more questions
        if current_question_index[0] < len(quiz_data):
            question_data = quiz_data[current_question_index[0]]
            label, translation, transliteration = question_data

            # Formulate the question
            question_text = f"What is the translation of '{label}'?"
            if transliteration:
                question_text += f" (Hint: {transliteration})"

            # Display the question
            question_label = tk.Label(question_frame, text=question_text, font=("Arial", 14), wraplength=350, bg="#FFFFFF")
            question_label.pack(pady=10)

            # Generate options (correct answer + random distractors)
            correct_answer = translation
            distractors = random.sample([q[1] for q in quiz_data if q[1] != correct_answer], k=min(3, len(quiz_data) - 1))
            options = distractors + [correct_answer]
            random.shuffle(options)

            # Create radio buttons for answers
            selected_answer = tk.StringVar(value="")

            for option in options:
                radio_button = tk.Radiobutton(
                    question_frame, text=option, value=option, variable=selected_answer, font=("Arial", 12), bg="#FFFFFF"
                )
                radio_button.pack(anchor="w", padx=20, pady=5)

            def handle_button_click():
                # Store the selected answer
                selected_answers.append(selected_answer.get())
                # Check answer and update score
                if selected_answer.get() == correct_answer:
                    score[0] += 1
                current_question_index[0] += 1
                if current_question_index[0] == len(quiz_data):
                    end_quiz()  # If it's the last question, end the quiz
                else:
                    next_question()  # Otherwise, go to the next question

            # Create the appropriate button for the question
            if current_question_index[0] == len(quiz_data) - 1:  # Last question
                button_text = "Submit"
            else:
                button_text = "Next"

            action_button = tk.Button(question_frame, text=button_text, command=handle_button_click, font=("Arial", 12), bg="#7CA5AE", fg="#FFFFFF", relief="flat", padx=10, pady=5)
            action_button.pack(pady=20)

        else:
            end_quiz()

    def end_quiz():
        # Prepare correctness data for the scoreboard
        correctness_data = []
        for i, question_data in enumerate(quiz_data):
            label, translation, transliteration = question_data
            correct = selected_answers[i] == translation  # Compare selected answer with the correct answer
            correctness_data.append((label, translation, transliteration, correct))

        # Pass correctness data to the scoreboard via environment variable
        os.environ["CORRECTNESS_DATA"] = str(correctness_data)
        os.environ["USER_SCORE"] = str(score[0])

        for widget in question_frame.winfo_children():
            widget.destroy()

        # Display the final score
        score_label = tk.Label(
            question_frame,
            text=f"Quiz Completed! Your Score: {score[0]}/{len(quiz_data)}",
            font=("Arial", 16),
            wraplength=350,
            bg="#FFFFFF"
        )
        score_label.pack(pady=20)

        # Add buttons based on the score
        if score[0] == len(quiz_data):  # Full marks
            view_scoreboard_button = tk.Button(
                question_frame, text="View Scoreboard", font=("Arial", 12), bg="#7CA5AE", fg="#FFFFFF", relief="flat", command=view_scoreboard
            )
            view_scoreboard_button.pack(pady=10)
        else:  # Not full marks
            restart_button = tk.Button(
                question_frame, text="Restart Quiz", font=("Arial", 12), bg="#7CA5AE", fg="#FFFFFF", relief="flat", command=lambda: restart_quiz()
            )
            restart_button.pack(pady=10)

            view_scoreboard_button = tk.Button(
                question_frame, text="View Scoreboard", font=("Arial", 12), bg="#7CA5AE", fg="#FFFFFF", relief="flat", command=view_scoreboard
            )
            view_scoreboard_button.pack(pady=10)

    def view_scoreboard():
        """Open the scoreboard script."""
        try:
            window.destroy()
            subprocess.run(["python", "score_board.py"])
        except Exception as e:
            print(f"Error opening scoreboard: {e}")

    def restart_quiz():
        """Restart the quiz."""
        window.destroy()
        start_quiz(quiz_data)

    # Main Tkinter window
    window = tk.Tk()
    window.title("Quiz")
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

    canvas.create_text(180.0, 120.0, text="Answer the Questions", fill="black", font=("Amaranth Regular", 18), anchor="center")

    # Quiz frame
    question_frame = tk.Frame(window, bg="#FFFFFF")
    question_frame.place(x=10, y=85, width=360, height=480)

    image_path = r"C:\Users\HEMA DARSHINY\Downloads\installation_opencv-python\object_detection\bottom_quiz.png"
    original_image = Image.open(image_path)

    # Resize the image to fit the width of the window (360px)
    resized_image = original_image.resize((360, int(original_image.height * 360 / original_image.width)))

    # Convert the resized image to PhotoImage
    image_bottom = ImageTk.PhotoImage(resized_image)

    # Place the image at the bottom center of the window
    canvas.create_image(180, 600, image=image_bottom)

    # Start the first question
    next_question()

    # Run the Tkinter loop
    window.mainloop()

# Load quiz data
quiz_data = load_quiz_data()

if quiz_data:
    start_quiz(quiz_data)
else:
    print("No quiz data found. Make sure to run this script after setting up the data.")




