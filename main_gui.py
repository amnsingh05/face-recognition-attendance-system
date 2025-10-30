import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import pandas as pd
from datetime import datetime
import attendance  # ✅ Import your attendance.py file directly

# -------------------------------
# Global variable for current user
# -------------------------------
CURRENT_USER = None


# -------------------------------
# Functions
# -------------------------------
def set_current_user(username):
    global CURRENT_USER
    CURRENT_USER = username


def capture_faces():
    try:
        subprocess.run(["python", "dataset_creator.py"])
    except Exception as e:
        messagebox.showerror("Error", str(e))


def train_model():
    try:
        subprocess.run(["python", "trainer.py"])
        messagebox.showinfo("Success", "Model trained successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def take_attendance():
    if not CURRENT_USER:
        messagebox.showerror("Error", "No user logged in!")
        return
    try:
        attendance.start_attendance(CURRENT_USER)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def view_attendance():
    if not CURRENT_USER:
        messagebox.showerror("Error", "No user logged in!")
        return

    file_path = os.path.join("teachers_attendance", f"{CURRENT_USER}_attendance.csv")

    if not os.path.exists(file_path):
        messagebox.showinfo("Info", "No attendance file found yet!")
        return

    try:
        df = pd.read_csv(file_path)
        if df.empty:
            messagebox.showinfo("Info", "Attendance file is empty!")
            return

        top = tk.Toplevel(root)
        top.title(f"Attendance Record - {CURRENT_USER}")
        top.geometry("550x400")
        top.configure(bg="#f0f2f5")

        tk.Label(
            top,
            text=f"Attendance - {CURRENT_USER} ({datetime.now().strftime('%d %b %Y')})",
            font=("Arial", 13, "bold"),
            bg="#f0f2f5",
            fg="#2c3e50"
        ).pack(pady=10)

        text_box = tk.Text(top, wrap="none", font=("Consolas", 10))
        text_box.pack(expand=True, fill="both", padx=15, pady=10)

        text_box.insert("1.0", df.to_string(index=False))
        text_box.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def exit_app():
    root.destroy()


# -------------------------------
# Main GUI Window
# -------------------------------
def open_main_gui(username):
    set_current_user(username)

    global root
    root = tk.Tk()
    root.title("Smart Face Recognition Attendance System")
    root.geometry("420x520")
    root.configure(bg="#ecf0f1")
    root.resizable(False, False)

    header_frame = tk.Frame(root, bg="#2c3e50", height=80)
    header_frame.pack(fill="x")

    title = tk.Label(
        header_frame,
        text=f"Welcome, {username}",
        font=("Segoe UI", 13, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title.pack(pady=20)

    btn_frame = tk.Frame(root, bg="#ecf0f1")
    btn_frame.pack(pady=30)

    btn_style = {
        "width": 25,
        "height": 2,
        "font": ("Segoe UI", 10, "bold"),
        "relief": "flat",
        "bd": 3
    }

    tk.Button(btn_frame, text="📸  Capture Faces", bg="#3498db", fg="white", command=capture_faces, **btn_style).pack(pady=8)
    tk.Button(btn_frame, text="🧠  Train Model", bg="#27ae60", fg="white", command=train_model, **btn_style).pack(pady=8)
    tk.Button(btn_frame, text="✅  Take Attendance", bg="#f39c12", fg="white", command=take_attendance, **btn_style).pack(pady=8)
    tk.Button(btn_frame, text="📋  View Attendance", bg="#9b59b6", fg="white", command=view_attendance, **btn_style).pack(pady=8)
    tk.Button(btn_frame, text="❌  Exit", bg="#e74c3c", fg="white", command=exit_app, **btn_style).pack(pady=8)

    footer = tk.Label(root, text="© 2025 Smart Attendance System", font=("Segoe UI", 8), bg="#ecf0f1", fg="#7f8c8d")
    footer.pack(side="bottom", pady=10)

    root.mainloop()


# -------------------------------
# For testing manually
# -------------------------------
if __name__ == "__main__":
    open_main_gui("teacher1")
