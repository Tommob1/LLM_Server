import tkinter as tk
from tkinter import scrolledtext, messagebox
from LLM_Server_Access import query_server

def send():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        response = query_server(user_input)
        output_text.configure(state='normal')
        output_text.insert(tk.END, f"USER: {user_input}\n", 'user_text')
        output_text.insert(tk.END, f"AI: {response}\n\n", 'green_text')
        output_text.configure(state='disabled')
        input_text.delete("1.0", tk.END)
    else:
        messagebox.showinfo("Info", "Please enter some text to send.")

def on_enter_key(event):
    send()
    return 'break'  # This prevents the default behavior of the Enter key which is to insert a newline.

app = tk.Tk()
app.title("LLM Interface")
app.geometry("400x400")  # Keep the window size consistent

# Styling
background_color = "#333"
text_color = "#EEE"
button_color = "#555"
font_style = ("Arial", 12)
app.configure(bg=background_color)

# Input Text Box
input_text = scrolledtext.ScrolledText(app, height=3, width=50, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD)
input_text.pack(pady=10, padx=10)
input_text.bind("<Return>", on_enter_key)

# Output Text Box
output_text = scrolledtext.ScrolledText(app, height=15, width=50, font=font_style, bg=background_color, fg=text_color, wrap=tk.WORD)
output_text.pack(pady=10, padx=10)
output_text.configure(state='disabled')

output_text.tag_config('user_text', foreground="#FF6347")  # Tomato
output_text.tag_config('green_text', foreground="#90EE90")  # Light green

# Send Button
send_button = tk.Button(app, text="Send", command=send, font=font_style, bg=button_color, fg=text_color)
send_button.pack(pady=10, padx=10)

app.mainloop()
