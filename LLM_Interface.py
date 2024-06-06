import tkinter as tk
from tkinter import Text, messagebox, Label
from LLM_Server_Access import query_server
from Logo import ascii_art
import requests

def query_server(user_input):
    response = requests.post('http://192.168.56.1:5000/query', json={'query': user_input})
    return response.json().get('response', 'Error: No response from server')

def update_status(status):
    info_text.configure(state='normal')
    if status == "TESTING":
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, "Status: TESTING\n", 'status_text')
    elif status == "ONLINE":
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, "Status: ONLINE\n", 'status_text')
    elif status == "OFFLINE":
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, "Status: OFFLINE\n", 'error_text')
    info_text.configure(state='disabled')

def send():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        response = query_server(user_input)
        output_text.configure(state='normal')
        output_text.insert(tk.END, f"USER: {user_input}\n", 'user_text')
        output_text.insert(tk.END, f"AI: {response}\n\n", '#00ff00')
        output_text.see(tk.END)
        output_text.configure(state='disabled')
        input_text.delete("1.0", tk.END)

        update_info_text2(f"Latest Query: {user_input[:30]}... (truncated)\nResponse Length: {len(response)} characters\n\n")
    else:
        messagebox.showinfo("Info", "Please enter some text to send.")

def on_enter_key(event):
    send()
    return 'break'

def load_text_character_by_character(widget, text, index=0, delay=50):
    if index < len(text):
        if isinstance(widget, tk.Text):
            widget.configure(state='normal')
            widget.insert(tk.END, text[index])
            widget.configure(state='disabled')
        elif isinstance(widget, tk.Label):
            current_text = widget.cget("text")
            widget.configure(text=current_text + text[index])
        widget.see(tk.END) if isinstance(widget, tk.Text) else None
        widget.after(delay, lambda: load_text_character_by_character(widget, text, index + 1, delay))

def update_info_text2(text):
    info_text2.configure(state='normal')
    info_text2.insert(tk.END, text)
    info_text2.see(tk.END)
    info_text2.configure(state='disabled')

app = tk.Tk()
app.title("NEURON Interface")
app.geometry("1280x720")
app.attributes("-alpha", 0.9)

background_color = "#000000"
text_color = "#00ff00"
button_color = "#333333"
border_color = "#555"
font_style = ("Consolas", 12)
app.configure(bg=background_color)
print(ascii_art)

info_text2 = Text(app, height=40, width=30, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                  borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
info_text2.pack(side='left', fill='y', padx=0, pady=0)

info_text = Text(app, height=40, width=30, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                 borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
info_text.pack(side='right', fill='y', padx=0, pady=0)

title_label = tk.Label(app, font=("Courier New", 10), bg=background_color, fg=text_color, anchor='center', justify='center')
title_label.pack(fill='x', padx=10, pady=10)

input_text = Text(app, height=3, width=50, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                  borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
input_text.pack(pady=10, padx=10)
input_text.bind("<Return>", on_enter_key)

output_text = Text(app, height=30, width=100, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                   borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
output_text.pack(pady=10, padx=10)
output_text.configure(state='disabled')

def send_test_message():
    update_status("TESTING")
    load_text_character_by_character(info_text2, "Sending test to LLM...\n\n")
    app.after(2000, perform_server_check)

def perform_server_check():
    response = query_server("hello")
    if "Error" in response:
        update_status("OFFLINE")
        load_text_character_by_character(info_text2,"Model Status: OFFLINE\n\nTest Failed\nModel Unresponsive\n\n")
    else:
        update_status("ONLINE")
        load_text_character_by_character(info_text2,"Model Status: ONLINE\n\nTest Successful\nModel Responsive\n\n")

def update_status(status):
    status_value_label.config(text=status)
    if status == "TESTING":
        status_value_label.config(fg='yellow')
    elif status == "ONLINE":
        status_value_label.config(fg='#00ff00')
    elif status == "OFFLINE":
        status_value_label.config(fg='red')

status_label = Label(app, text="AI STATUS:", font=("Consolas", 15), bg="#000000", fg="#00ff00")
status_label.pack(side='left', padx=(0, 2))

status_value_label = Label(app, text="INITIALIZING...", font=("Consolas", 15), bg="#000000", fg="#00ff00")
status_value_label.pack(side='left', padx=(2, 10))

app.after(500, lambda: load_text_character_by_character(info_text2, "Model Updates:\n\n", 0, 20))
app.after(1500, lambda: load_text_character_by_character(info_text,"""AI MODEL INFORMATION:\n\nModel Type: \nMistral Instruct \n(v0 1 7B Q4_0 gguf)\n\nDeveloper: \nMistral AI\n\nAI Name: \nNEURON\n\nModel Instructions:
'You are a helpful AI assistant named NEURON.\nYou live in my macbook in the LMStudio platform.'\n""", 0, 20))
app.after(2000, lambda: load_text_character_by_character(title_label, ascii_art, 0, 1))
app.after(10000, send_test_message)

app.mainloop()
