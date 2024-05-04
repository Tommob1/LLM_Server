import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Scrollbar, Style  # Make sure to use ttk's Scrollbar for better style support
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
    return 'break'

app = tk.Tk()
app.title("LLM Interface")
app.geometry("400x400")  # Keep the window size consistent

# Styling
background_color = "#333"
text_color = "#EEE"
button_color = "#555"
scrollbar_color = "#666"  # Dark grey color for scrollbars
font_style = ("Arial", 12)

app.configure(bg=background_color)

# Style configuration for ttk scrollbars
style = Style()
style.theme_use('default')  # Ensure default theme is active to apply custom style
style.configure("Vertical.TScrollbar", gripcount=0,
                background=scrollbar_color, darkcolor=scrollbar_color, lightcolor=scrollbar_color,
                troughcolor=background_color, bordercolor=background_color, arrowcolor=text_color)

# Input Text Box
input_text = scrolledtext.ScrolledText(app, height=3, width=50, font=font_style, bg=background_color, fg=text_color)
input_text.pack(pady=10, padx=10)
input_text.bind("<Return>", on_enter_key)

# Custom ttk Scrollbar for input_text
input_scrollbar = Scrollbar(app, orient="vertical", style="Vertical.TScrollbar")
input_scrollbar.pack(side="right", fill="y")
input_scrollbar.config(command=input_text.yview)
input_text.config(yscrollcommand=input_scrollbar.set)

# Output Text Box
output_text = scrolledtext.ScrolledText(app, height=15, width=50, font=font_style, bg=background_color, fg=text_color)
output_text.pack(pady=10, padx=10)
output_text.configure(state='disabled')

# Custom ttk Scrollbar for output_text
output_scrollbar = Scrollbar(app, orient="vertical", style="Vertical.TScrollbar")
output_scrollbar.pack(side="right", fill="y")
output_scrollbar.config(command=output_text.yview)
output_text.config(yscrollcommand=output_scrollbar.set)

output_text.tag_config('user_text', foreground="#FF6347")  # Tomato
output_text.tag_config('green_text', foreground="#90EE90")  # Light green

# Send Button
send_button = tk.Button(app, text="Send", command=send, font=font_style, bg=button_color, fg=text_color)
send_button.pack(pady=10, padx=10)

app.mainloop()
