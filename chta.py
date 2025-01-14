import tkinter as tk
from tkhtmlview import HTMLLabel

def open_chatbot():
    # Embed the chatbot in a web view
    chatbot_window = tk.Toplevel(root)
    chatbot_window.title("Chatbot")
    chatbot_window.geometry("800x600")

    chatbot_label = HTMLLabel(
        chatbot_window,
        html=f"""
        <iframe src="https://files.bpcontent.cloud/2025/01/13/16/20250113161917-CQX9A3TD.js" 
        width="100%" height="100%" frameborder="0"></iframe>
        """,
    )
    chatbot_label.pack(fill="both", expand=True)

# Create the main application window
root = tk.Tk()
root.title("Chatbot Integration Example")
root.geometry("400x300")

# Add a clickable icon button to open the chatbot
chatbot_icon = tk.PhotoImage(file="chatbot.png")  # Replace with your icon file path
chatbot_button = tk.Button(root, image=chatbot_icon, command=open_chatbot)
chatbot_button.pack(pady=50)

root.mainloop()
