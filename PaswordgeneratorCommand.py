# === IMPORT SECTION
import tkinter as tk
from tkinter import messagebox, ttk
import os
import binascii
import string
import random

# === PASSWORD LOGIC

def generate_strong_password(length=16):
    if length < 8:
        raise ValueError("Password must be at least 8 characters long.")
    chars = string.ascii_letters + string.digits + string.punctuation
    char_len = len(chars)

    while True:
        raw_bytes = os.urandom(length)
        hex_str = binascii.hexlify(raw_bytes).decode('utf-8')
        password_chars = [chars[int(hex_str[i:i+2], 16) % char_len] for i in range(0, length * 2, 2)]
        password = ''.join(password_chars)
        if (any(c.islower() for c in password) and any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and any(c in string.punctuation for c in password)):
            return password

def generate_simple_password(length=16):
    if length < 8:
        raise ValueError("Password must be at least 8 characters.")
    chars = string.ascii_letters + string.digits + string.punctuation
    required = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase),
                random.choice(string.digits), random.choice(string.punctuation)]
    remaining = [random.choice(chars) for _ in range(length - 4)]
    password = required + remaining
    random.shuffle(password)
    return ''.join(password)

def generate_custom_password(lower, upper, digits, symbols):
    if any(i < 0 for i in [lower, upper, digits, symbols]):
        raise ValueError("Character amounts cant be negative.")
    total = lower + upper + digits + symbols
    if total < 8:
        raise ValueError("Total character must be at least 8.")
    password = (random.choices(string.ascii_lowercase, k=lower) +
                random.choices(string.ascii_uppercase, k=upper) +
                random.choices(string.digits, k=digits) +
                random.choices(string.punctuation, k=symbols))
    random.shuffle(password)
    return ''.join(password)

def shuffle_user_input(text):
    if not text.strip():
        raise ValueError("Please enter some text to shuffle.")
    chars = list(text.strip())
    random.shuffle(chars)
    return ''.join(chars)

def check_password_strength(password): 
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    percent = int((score / 6) * 100)
    if percent < 40: return percent, "Weak", "red"
    elif percent < 80: return percent, "Medium", "orange"
    else: return percent, "Strong", "green"

# === UI FUNCTIONS

def generate_password():
    try:
        mode = mode_var.get()
        if mode == "Custom":
            lower = int(entry_lower.get())
            upper = int(entry_upper.get())
            digits = int(entry_digits.get())
            symbols = int(entry_symbols.get())
            result = generate_custom_password(lower, upper, digits, symbols)
        elif mode == "Shuffle My Words":
            user_text = entry_shuffle.get()
            result = shuffle_user_input(user_text)
        else:
            length = int(length_entry.get())
            if mode == "Super safety":
                result = generate_strong_password(length)
            else:
                result = generate_simple_password(length)

        output_var.set(result)
        percent, label, color = check_password_strength(result)
        strength_bar["value"] = percent
        strength_label.config(text=label, fg=color)

    except ValueError as e:
        messagebox.showerror("Oops!", str(e))

def salin_password():
    root.clipboard_clear()
    root.clipboard_append(output_var.get())
    root.update()
    messagebox.showinfo("Copied!", "Password has been copied to clipboard")

def switch_mode(*args):
    mode = mode_var.get()
    if mode == "Custom":
        frame_custom.pack(pady=5)
        frame_length.pack_forget()
        frame_shuffle.pack_forget()
    elif mode == "Shuffle My Words":
        frame_shuffle.pack(pady=5)
        frame_custom.pack_forget()
        frame_length.pack_forget()
    else:
        frame_length.pack(pady=5)
        frame_custom.pack_forget()
        frame_shuffle.pack_forget()

def About_This_App():
    About_text = (
        "Safe Password Generator for your digital life privacy \n\n"
        "Aplikasi ini di buat untuk membantu pengguna digital untuk mencari password yang aman serta mempelajari tentang pentingnya password yang kuat \n di era digital sekarang"
        "\n tentang cara kerja setiap mode:"
        "\nMode Super Safety: \nMenggunakan Urandom mengambil byte acak dari device sendiri, mengubah byte menjadi int lalu di ubah menjadi string melalui index len"
        "\nMode Simple: \nMenggabungkan semua huruf menjadi satu lalu mengambil satu dari setiap jenis berbeda (angka, huruf besar/kecil, simbol) lalu input pengguna dikurang 4. sisanya di ambil acak lagi hingga memenuhi syarat."
        "\nMode Custom: \nMeminta 4 jenis angka yang dapat di isi oleh user, untuk di buat password generator custom. Menggunakan cara random choice satu persatu hingga memenuhi keinginan user lalu di acak lagi agar tidak tersusun seperti formula awal: kecil, besar, digit dan symbol"
        "\nMode Shuffle My Words: \nMeminta teks dari user lalu di acak menggunakan shuffle random"
    )
    messagebox.showinfo("About this app", About_text)

# === BUILD UI

root = tk.Tk()
root.title("Safe Password Generator")
root.geometry("430x400")
root.resizable(False, False)



tk.Label(root, text="Password Mode:").pack(pady=5)


mode_var = tk.StringVar(value="Super safety")
tk.OptionMenu(root, mode_var, "Super safety", "Simple", "Custom", "Shuffle My Words").pack()

# Frame standard length input.
frame_length = tk.Frame(root)
tk.Label(frame_length, text="Password Length (min 8):").grid(row=0, column=0, padx=5, pady=5)
length_entry = tk.Entry(frame_length)
length_entry.insert(0, "16")
length_entry.grid(row=0, column=1)
frame_length.pack(pady=5)

# Frame custom inputs.
frame_custom = tk.Frame(root)
def add_custom_input(row, label):
    tk.Label(frame_custom, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=3)
    entry = tk.Entry(frame_custom, width=10)
    entry.insert(0, "0")
    entry.grid(row=row, column=1)
    return entry

entry_lower = add_custom_input(0, "Lowercase:")
entry_upper = add_custom_input(1, "Uppercase:")
entry_digits = add_custom_input(2, "Digits:")
entry_symbols = add_custom_input(3, "Symbols:")

# Frame shuffle input
frame_shuffle = tk.Frame(root)
tk.Label(frame_shuffle, text="Enter words to shuffle:").grid(row=0, column=0, padx=5, pady=5)
entry_shuffle = tk.Entry(frame_shuffle, width=30)
entry_shuffle.grid(row=0, column=1, padx=5, pady=5)

# Generate button.
tk.Button(root, text="Generate Password", command=generate_password, bg="#329C36", fg="white").pack(pady=10)
# Output password.
output_var = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_var, font=('Courier', 12), width=34, justify='center', state='readonly')
output_entry.pack(pady=5)


# Strength bar.
frame_strength = tk.Frame(root)
frame_strength.pack(pady=5)
tk.Label(frame_strength, text="Strength:").grid(row=0, column=0, padx=5)
strength_bar = ttk.Progressbar(frame_strength, orient="horizontal", length=200, mode="determinate", maximum=100)
strength_bar.grid(row=0, column=1)
strength_label = tk.Label(frame_strength, text="", font=("Arial", 10, "bold"))
strength_label.grid(row=0, column=2, padx=5)

# Copy button.
tk.Button(root, text="Copy to clipboard", command=salin_password).pack(pady=5)


tk.Button(root, text="About", command=About_This_App).pack(side="bottom", pady=5)

switch_mode()
mode_var.trace_add("write", switch_mode)

root.mainloop()
