import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from LLM_Server_Access import query_server

def send():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        response = query_server(user_input)  # Your function to get the response from the LLM
        output_text.configure(state='normal')
        output_text.insert(tk.END, f"USER: {user_input}\n", 'user_text')  # Optional: Different style for user text
        output_text.insert(tk.END, f"AI: {response}\n\n", 'green_text')  # Apply the green text tag here
        output_text.configure(state='disabled')
        input_text.delete("1.0", tk.END)
    else:
        messagebox.showinfo("Info", "Please enter some text to send.")

app = tk.Tk()
app.title("LLM Interface")

input_text = scrolledtext.ScrolledText(app, height=3, width=50)
input_text.pack(pady=10)

output_text = scrolledtext.ScrolledText(app, height=15, width=50)
output_text.pack(pady=10)
output_text.configure(state='disabled')

output_text.tag_config('green_text', foreground='green')

send_button = tk.Button(app, text="Send", command=send)
send_button.pack(pady=10)

app.mainloop()
