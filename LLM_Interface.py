import tkinter as tk
from tkinter import Text, messagebox, PhotoImage
from LLM_Server_Access import query_server
from logo import ascii_art

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
app.geometry("1920x1080")

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

output_text = Text(app, height=45, width=100, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD,
                   borderwidth=1, relief="solid", highlightbackground=border_color, highlightthickness=1)
output_text.pack(pady=10, padx=10)
output_text.configure(state='disabled')

app.after(500, lambda: load_text_character_by_character(info_text2, "Model Updates:\n\n", 0, 20))
app.after(1500, lambda: load_text_character_by_character(info_text,"""AI MODEL INFORMATION:\n\nModel Type: \nMistral Instruct \n(v0 1 7B Q4_0 gguf)\n\nDeveloper: \nMistral AI\n\nAI Name: \nNEURON\n\nModel Instructions:
'You are a helpful AI assistant named NEURON.\nYou live in my macbook in the LMStudio platform.'\n""", 0, 20))
app.after(2000, lambda: load_text_character_by_character(title_label, ascii_art, 0, 1))

app.mainloop()
