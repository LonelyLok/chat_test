import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext
import threading
import os

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=api_key)

def list_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

# model = genai.GenerativeModel('models/gemini-ultra')
# models/gemini-1.0-pro
# models/gemini-1.0-pro-001
# models/gemini-1.0-pro-latest
# models/gemini-1.0-pro-vision-latest
# models/gemini-1.5-pro-latest
# models/gemini-pro
# models/gemini-pro-vision

# if __name__ == '__main__':
#   model = genai.GenerativeModel('models/gemini-ultra')
#   chat = model.start_chat()
#   while True:
#     user_input = input("")
#     if user_input == "exit":
#       break
#     response = chat.send_message(user_input, stream=True)
#     for chunk in response:
#       print(chunk.text)
#       print("_"*80)

#   pass

class ChatApplication(tk.Tk):
    def __init__(self, chat):
        super().__init__()
        self.chat = chat
        
        self.title("Chat with AI")
        self.geometry("1280x720")

        self.dark_background = "#363636"
        self.light_foreground = "#E1E1E1"
        self.input_background = "#4D4D4D"
        self.button_background = "#5C5C5C"

        self.configure(bg=self.dark_background)

        self.chat_display = scrolledtext.ScrolledText(self, state='disabled', wrap=tk.WORD, bg=self.dark_background, fg=self.light_foreground)
        self.chat_display.pack(padx=10, pady=10, side=tk.TOP, expand=True, fill='both')

        self.bottom_frame = tk.Frame(self, bg=self.dark_background)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.message_entry = tk.Entry(self.bottom_frame, bg=self.input_background, fg=self.light_foreground, insertbackground=self.light_foreground)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=5, pady=5)
        self.message_entry.bind("<Return>", self.initiate_send_message)

        self.send_button = tk.Button(self.bottom_frame, text="Send", bg=self.button_background, fg=self.light_foreground, command=self.initiate_send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def display_message(self, message, sender="You"):
        if self.chat_display:
            self.chat_display.config(state='normal')
            if sender != "":
              separator = "\n" + "-" * 50 + "\n"
            else:
              separator = ""
            # Check if we need to add sender prefix
            prefix = separator  + f"{sender}: " if sender else ""
            self.chat_display.insert(tk.END, prefix + message + "\n")
            self.chat_display.config(state='disabled')
            self.chat_display.yview(tk.END)

    def append_message(self, message):
        # Append a message directly without sender prefix
        self.display_message(message, sender="")

    def send_message(self, user_input):
        # Initial call to display user's message
        self.display_message(user_input, sender="You")
        
        # Start receiving the response chunks
        response = self.chat.send_message(user_input, stream=True)
        
        # Initialize flag for first chunk
        is_first_chunk = True
        for chunk in response:
            if is_first_chunk:
                # Display first chunk with "AI:" prefix
                self.display_message(chunk.text, sender="AI")
                is_first_chunk = False
            else:
                # Directly append subsequent chunks
                self.append_message(chunk.text)

    def initiate_send_message(self, event=None):
        user_input = self.message_entry.get().strip()
        if user_input and user_input.lower() != "exit":
            self.message_entry.delete(0, tk.END)
            threading.Thread(target=self.send_message, args=(user_input,)).start()
        elif user_input.lower() == "exit":
            self.quit()

if __name__ == '__main__':
    # model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    # chat = model.start_chat()
    # app = ChatApplication(chat)
    # app.mainloop()
    list_models()