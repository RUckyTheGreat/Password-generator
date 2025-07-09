
# 🔐 Safe Password Generator

A secure, user-friendly password generator made with Python and Tkinter.  
It supports multiple generation modes for various user needs, with built-in password strength checking.

## 🌟 Features

- **Super Safety Mode**: Uses system-level random bytes (`os.urandom`) for strong entropy.
- **Simple Mode**: Ensures all character types are included (uppercase, lowercase, digits, symbols).
- **Custom Mode**: Let users specify how many of each character type they want.
- **Shuffle My Words**: Shuffle your own input string into a random arrangement.
- **Password Strength Bar**: Gives visual feedback on how strong the generated password is.
- **Copy to Clipboard**: One-click copy functionality.
- **About Section**: Educational description of each mode's working.

---

## 🖥️ How It Works

Each mode uses a different generation logic:

### 🔒 Super Safety
- Uses `os.urandom()` to generate raw bytes.
- Converts to hex, maps to characters using modulus operation on `ascii + digits + symbols`.
- Ensures password has at least 1 of each character type (lowercase, uppercase, digit, symbol).

### ✨ Simple
- Combines character sets and guarantees one of each type.
- Fills the rest randomly and shuffles the result.

### 🧪 Custom
- Takes user-defined numbers of lowercase, uppercase, digits, and symbols.
- Builds the password accordingly and shuffles it.

### 🔄 Shuffle My Words
- Accepts user text input.
- Shuffles the characters randomly.

---

## 🚀 Getting Started

### Requirements
- Python 3.x

### Run the App

```bash
python password_generator.py
```

> No external libraries needed, all built-in modules are used.

---

## 🧠 Password Strength Calculation

The app calculates password strength based on:
- Length (>=8, >=12)
- Presence of:
  - Lowercase
  - Uppercase
  - Digit
  - Symbol

The score is scaled to a percentage and classified as:
- **Weak** (Red) — < 40%
- **Medium** (Orange) — 40%–79%
- **Strong** (Green) — 80%–100%

---

## 📷 Preview

![UI Screenshot](screenshot.png) <!-- Replace this with your own screenshot if hosted -->

---

## 📁 Project Structure

```
password_generator.py      # Main application file
README.md                  # This file
```

---

## 🙋‍♂️ About

This app was built to help users understand the importance of strong passwords, especially in the digital era.  
Created with love using Python and Tkinter 💚

---

## 📄 License

MIT License - Use it freely!

---

## 💬 Credits

Built by Raka Sabari Pratama  
SMKN 2 Bandung — IT Hero Cortex
