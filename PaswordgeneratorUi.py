import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os, binascii, string

# --------- PASSWORD GENERATOR ---------
def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    char_len = len(chars)
    while True:
        raw_bytes = os.urandom(length)
        hex_str = binascii.hexlify(raw_bytes).decode('utf-8')
        password = ''.join(chars[int(hex_str[i:i+2], 16) % char_len] for i in range(0, length * 2, 2))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

# --------- ENKRIPSI & SIMPAN ---------
def encrypt_and_save(password, user_key, file_path):
    try:
        salt = get_random_bytes(16)
        key = PBKDF2(user_key, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(password.encode())

        with open(file_path, "wb") as f:
            f.write(salt + cipher.nonce + tag + ciphertext)

        messagebox.showinfo("Sukses", "Password berhasil disimpan dan dienkripsi.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengenkripsi: {str(e)}")

# --------- DEKRIPSI FILE ---------
def decrypt_password_from_file(file_path, user_key):
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        salt = data[:16]
        nonce = data[16:32]
        tag = data[32:48]
        ciphertext = data[48:]

        key = PBKDF2(user_key, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode()
    except Exception as e:
        messagebox.showerror("Gagal Dekripsi", f"Error: {str(e)}")
        return None

# --------- GUI LOGIC ---------
def generate_password_gui():
    try:
        length = int(entry_length.get())
        password = generate_strong_password(length)
        output_var.set(password)
    except ValueError:
        messagebox.showerror("Error", "Masukkan angka valid untuk panjang password.")

def save_password_gui():
    password = output_var.get()
    user_key = entry_master.get()
    if not password:
        messagebox.showwarning("Peringatan", "Password belum digenerate.")
        return
    if not user_key:
        messagebox.showwarning("Peringatan", "Masukkan master key untuk enkripsi.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary File", "*.bin")])
    if file_path:
        encrypt_and_save(password, user_key, file_path)

def load_password_gui():
    file_path = filedialog.askopenfilename(filetypes=[("Binary File", "*.bin")])
    if file_path:
        user_key = entry_master.get()
        if not user_key:
            messagebox.showwarning("Peringatan", "Masukkan master key untuk dekripsi.")
            return
        result = decrypt_password_from_file(file_path, user_key)
        if result:
            output_var.set(result)
            messagebox.showinfo("Sukses", "Password berhasil didekripsi.")

# --------- GUI SETUP ---------
root = tk.Tk()
root.title("Password Generator & Manager Aman")

tk.Label(root, text="Panjang Password (min 8):").pack()
entry_length = tk.Entry(root)
entry_length.insert(0, "16")
entry_length.pack()

tk.Button(root, text="Generate Password", command=generate_password_gui).pack(pady=5)

tk.Label(root, text="Password yang dihasilkan:").pack()
output_var = tk.StringVar()
tk.Entry(root, textvariable=output_var, width=40).pack()

tk.Label(root, text="Master Key (untuk Enkripsi / Dekripsi):").pack()
entry_master = tk.Entry(root, show="*", width=40)
entry_master.pack()

frame_buttons = tk.Frame(root)
tk.Button(frame_buttons, text="Simpan Terenkripsi", command=save_password_gui).pack(side="left", padx=5)
tk.Button(frame_buttons, text="Buka & Dekripsi File", command=load_password_gui).pack(side="left", padx=5)
frame_buttons.pack(pady=10)

root.mainloop()
