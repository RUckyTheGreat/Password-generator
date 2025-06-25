import tkinter as tk
from tkinter import messagebox
import os
import binascii
import string
import random

# === LOGIC PASSWORD ===
def generate_strong_password(length=16):
    if length < 8:
        raise ValueError("Password minumum 8 character for secure.")
    chars = string.ascii_letters + string.digits + string.punctuation
    char_len = len(chars)

    while True:
        raw_bytes = os.urandom(length)
        hex_str = binascii.hexlify(raw_bytes).decode('utf-8')
        password_chars = [
            chars[int(hex_str[i:i+2], 16) % char_len]
            for i in range(0, length * 2, 2)
        ]
        password = ''.join(password_chars)
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

def generate_simple_password(length=16):
    if length < 8:
        raise ValueError("Password minumum 8 character for security.")
    
    chars = string.ascii_letters + string.digits + string.punctuation
    required = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]
    sisa = [random.choice(chars) for _ in range(length - 4)]
    password = required + sisa
    random.shuffle(password)
    return ''.join(password)

# === FUNCTION UI ===
def generate_password():
    try:
        mode = mode_var.get()
        length = int(length_entry.get())

        if length < 8:
            raise ValueError("Password minumum 8 character for security.")
        
        if mode == "Super safety":
            result = generate_strong_password(length)
        else:
            result = generate_simple_password(length)

        output_var.set(result)

    except ValueError as e:
        messagebox.showerror("Wrong", str(e))

def salin_password():
    root.clipboard_clear()
    root.clipboard_append(output_var.get())
    root.update()
    messagebox.showinfo("Copied!", "Password Sucses copy to clipboard!")

# === SETUP UI ===
root = tk.Tk()
root.title("Safe Password Generator")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="Mode Generator:").pack(pady=5)
mode_var = tk.StringVar(value="Super safety")
tk.OptionMenu(root, mode_var, "Super safety", "Simpel").pack()

tk.Label(root, text="Length Password (min. 8):").pack(pady=5)
length_entry = tk.Entry(root)
length_entry.insert(0, "16")
length_entry.pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

output_var = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_var, font=('Courier', 12), width=30, justify='center', state='readonly')
output_entry.pack(pady=5)

tk.Button(root, text="Copy to Clipboard", command=salin_password).pack(pady=5)

root.mainloop()
