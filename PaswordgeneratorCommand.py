# === IMPORT SETUP ===
import tkinter as tk
from tkinter import messagebox
import os
import binascii
import string
import random

# === LOGIC PASSWORD ===
def generate_strong_password(length=16): #Description the lenght first for skip condition if. like Default of system
    if length < 8:
        raise ValueError("Password minumum 8 character for secure.") #Eror output
    chars = string.ascii_letters + string.digits + string.punctuation # String module have soo many string like alphabet low/ up, symbol and int. 
    #make it become one const for Make the const become len (can use int for search string with Index) example: a[1].... d[4]... etc and print char_len[4] then the output will be d
    char_len = len(chars) #make every single word become int with index A = 1 B =1 A+b = 2 index (like 94 maybe the output of index) for max. like minimum

    while True: #Looping for generate password until find the great pass
        raw_bytes = os.urandom(length) #Byte var. output like length * 2. Example output: 'b'/'x4f'/'x5a'/ etc
        hex_str = binascii.hexlify(raw_bytes).decode('utf-8') #Hex var. Like make byte become some hex var and decode to utf-8 (Basic lang for coding. that human know and robot know) Example output: 4f5a
        password_chars = [
            chars[int(hex_str[i:i+2], 16) % char_len] # search index of chars form  int/ hex_str cut every 2 kode become one group and make the minimum with var of hex: 0-f = 16 Hex desimal % char len for max of output
            for i in range(0, length * 2, 2) # because byte have 2 in every one. then just take 2(last) of var and stop in length (Lenght *2 because for odd condition)
        ] 
        password = ''.join(password_chars) #join the output of pass chars to const pass *string
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and# check c if have islower, upper, digit and simbol. use any because one word can easly skip the condition and go to the next condition. make the output will have all the thing
            any(c in string.punctuation for c in password)):
            return password #Return the output of pass

def generate_simple_password(length=16):
    if length < 8:
        raise ValueError("Password minumum 8 character for security.")
    
    chars = string.ascii_letters + string.digits + string.punctuation
    required = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]# Take one word random from string module.
    Remain = [random.choice(chars) for _ in range(length - 4)] #take random word from random chars and -4 (bc 4 already take from req) 
    password = required + Remain #Req + Remain = full pasword with diff word catagory and in the maximum of lenght
    random.shuffle(password) #2factor scure. make pass const random for scure
    return ''.join(password) #make sure that the output will be string

def generate_custom_password(lower, upper, digits, symbols):
    if any(i < 0 for i in range [lower, upper, digits, symbols])
    


# === FUNCTION UI ===
def generate_password():
    try:
        mode = mode_var.get()
        length = int(length_entry.get()) #try int

        if length < 8:
            raise ValueError("Password minumum 8 character for security.")
        
        if mode == "Super safety":
            result = generate_strong_password(length)
        else:
            result = generate_simple_password(length)

        output_var.set(result)

    except ValueError as e:
        messagebox.showerror("Wrong", str(e)) #eror msg for string input.

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
