import tkinter as tk
from tkinter import Text, messagebox, PhotoImage
from LLM_Server_Access import query_server

def send():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        response = query_server(user_input)
        output_text.configure(state='normal')
        output_text.insert(tk.END, f"USER: {user_input}\n", 'user_text')
        output_text.insert(tk.END, f"AI: {response}\n\n", '#00ff00')
        output_text.configure(state='disabled')
        input_text.delete("1.0", tk.END)
    else:
        messagebox.showinfo("Info", "Please enter some text to send.")

def on_enter_key(event):
    send()
    return 'break'

app = tk.Tk()
app.title("LLM Interface")
app.geometry("1920x1080")

background_color = "#000000"
text_color = "#00ff00"
button_color = "#333333"
border_color = "#555"
font_style = ("Consolas", 12)
app.configure(bg=background_color)

info_text = Text(app, height=40, width=30, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                 borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
info_text.insert(tk.END, "AI Model Information:\n\n- Model Type: Mistral Instruct v0 1 7B Q4_0 gguf\n- Developer: Mistral AI\n")
info_text.configure(state='disabled')
info_text.pack(side='right', fill='y', padx=0, pady=0)

info_text2 = Text(app, height=40, width=30, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                 borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
info_text2.insert(tk.END, "Model Instructions:\n\nYou are a helpful AI assistant named NEURON.\nYou live in my macbook in the LMStudio platform.")
info_text2.configure(state='disabled')
info_text2.pack(side='left', fill='y', padx=0, pady=0)

ascii_art = r"""
░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    
░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    
                                                                                                               
                                                                                                               
"""

title_label = tk.Label(app, text=ascii_art, font=("Courier New", 10), bg=background_color, fg=text_color, anchor='center', justify='center')
title_label.pack(fill='x', padx=10, pady=10)

input_text = Text(app, height=3, width=50, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                  borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
input_text.pack(pady=10, padx=10)
input_text.bind("<Return>", on_enter_key)

output_text = Text(app, height=45, width=100, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                   borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
output_text.pack(pady=10, padx=10)
output_text.configure(state='disabled')

output_text.tag_config('user_text', foreground="#FF0000")
output_text.tag_config('green_text', foreground="#2eb82e")

app.mainloop()
