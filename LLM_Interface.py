import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import LLM_Server_Access

def send():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        try:
            response = query_server(user_input)
            output_text.configure(state='normal')
            output_text.insert(tk.END, f"USER: {user_input}\n AI: {response}\n\n")
            output_text.configure(state='disabled')
            input_text.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showinfo("Info", "Enter text.")

