import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import bcrypt
import main_gui
import os


# =====================================================
# 🔹 Utility Functions
# =====================================================
def verify_login(username, password):
    """Check if username and password match in users.csv"""
    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    if bcrypt.checkpw(password.encode("utf-8"), row["password"].encode("utf-8")):
                        return True
        return False
    except FileNotFoundError:
        messagebox.showerror("Error", "users.csv not found!")
        return False


def get_security_question(username):
    """Return the security question for a given username"""
    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    return row["security_question"]
        return None
    except FileNotFoundError:
        messagebox.showerror("Error", "users.csv not found!")
        return None


def reset_password(username, answer, new_password):
    """Reset the user's password if the answer is correct"""
    users = []
    updated = False

    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    if row["security_answer"].lower() == answer.lower():
                        hashed_pw = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        row["password"] = hashed_pw
                        updated = True
                users.append(row)
    except FileNotFoundError:
        messagebox.showerror("Error", "users.csv not found!")
        return False

    if updated:
        with open("users.csv", "w", newline="") as file:
            fieldnames = ["username", "password", "role", "security_question", "security_answer"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        return True
    else:
        return False


def add_new_user(username, password, role, question, answer):
    """Add a new user securely"""
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Check if user already exists
    if os.path.exists("users.csv"):
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    messagebox.showerror("Error", "Username already exists!")
                    return False

    # Add user
    with open("users.csv", "a", newline="") as file:
        fieldnames = ["username", "password", "role", "security_question", "security_answer"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if os.stat("users.csv").st_size == 0:
            writer.writeheader()

        writer.writerow({
            "username": username,
            "password": hashed_pw,
            "role": role,
            "security_question": question,
            "security_answer": answer.lower()
        })

    messagebox.showinfo("Success", f"User '{username}' created successfully!")
    return True


# =====================================================
# 🔹 GUI Functions
# =====================================================
def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    if verify_login(username, password):
        messagebox.showinfo("Success", f"Welcome {username}!")
        root.destroy()
        main_gui.open_main_gui(username)  # ✅ Open dashboard
    else:
        messagebox.showerror("Error", "Invalid username or password!")


def forgot_password():
    username = simpledialog.askstring("Forgot Password", "Enter your username:")
    if not username:
        return

    question = get_security_question(username)
    if not question:
        messagebox.showerror("Error", "User not found!")
        return

    answer = simpledialog.askstring("Security Question", question)
    if not answer:
        return

    new_password = simpledialog.askstring("Reset Password", "Enter your new password:", show="*")
    if not new_password:
        return

    if reset_password(username, answer, new_password):
        messagebox.showinfo("Success", "Password reset successfully!")
    else:
        messagebox.showerror("Error", "Incorrect answer or user not found!")


def create_user():
    new_username = simpledialog.askstring("New User", "Enter new username:")
    new_password = simpledialog.askstring("New User", "Enter new password:", show="*")
    role = simpledialog.askstring("New User", "Enter role (Admin/Teacher/Staff):")
    question = simpledialog.askstring("New User", "Enter security question:")
    answer = simpledialog.askstring("New User", "Enter answer to security question:")

    if not (new_username and new_password and role and question and answer):
        messagebox.showerror("Error", "All fields are required!")
        return

    add_new_user(new_username, new_password, role, question, answer)


# =====================================================
# 🔹 Login Window
# =====================================================
root = tk.Tk()
root.title("Login - Smart Attendance System")
root.geometry("400x350")
root.configure(bg="#ecf0f1")
root.resizable(False, False)

# Title
tk.Label(root, text="Smart Attendance System", font=("Segoe UI", 14, "bold"), bg="#2c3e50", fg="white", width=40, height=2).pack(pady=10)

# Username
tk.Label(root, text="Username:", bg="#ecf0f1", font=("Segoe UI", 10, "bold")).pack(pady=5)
entry_username = tk.Entry(root, width=30)
entry_username.pack()

# Password
tk.Label(root, text="Password:", bg="#ecf0f1", font=("Segoe UI", 10, "bold")).pack(pady=5)
entry_password = tk.Entry(root, width=30, show="*")
entry_password.pack()

# Buttons
tk.Button(root, text="Login", bg="#27ae60", fg="white", width=20, command=login).pack(pady=10)
tk.Button(root, text="Forgot Password?", bg="#f39c12", fg="white", width=20, command=forgot_password).pack(pady=5)
tk.Button(root, text="Create New User", bg="#3498db", fg="white", width=20, command=create_user).pack(pady=5)
tk.Button(root, text="Exit", bg="#e74c3c", fg="white", width=20, command=root.destroy).pack(pady=15)

root.mainloop()
