import os
import shutil
import time
import tkinter as tk
from tkinter import scrolledtext

# =========================
# SETTINGS
# =========================
SOURCE_FOLDER = "/storage/emulated/0/Download"
DRY_RUN = False

FOLDERS = {
    "Images": [".jpg", ".jpeg", ".png", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
    "APKs": [".apk"]
}

# =========================
# FUNCTIONS
# =========================
def log(msg):
    output_box.insert(tk.END, msg + "\n")
    output_box.see(tk.END)

def unique_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    return f"{base}_{int(time.time())}{ext}"

def create_folders():
    for folder in FOLDERS:
        path = os.path.join(SOURCE_FOLDER, folder)
        if not os.path.exists(path):
            os.makedirs(path)

def organize_files():
    log("Starting organization...\n")

    create_folders()

    for file in os.listdir(SOURCE_FOLDER):
        file_path = os.path.join(SOURCE_FOLDER, file)

        if os.path.isdir(file_path):
            continue

        moved = False

        for folder_name, extensions in FOLDERS.items():
            if file.lower().endswith(tuple(extensions)):
                dest = os.path.join(SOURCE_FOLDER, folder_name, file)
                dest = unique_path(dest)

                if DRY_RUN:
                    log(f"[DRY RUN] {file} → {folder_name}")
                else:
                    shutil.move(file_path, dest)
                    log(f"Moved: {file} → {folder_name}")

                moved = True
                break

        if not moved:
            log(f"Skipped: {file}")

    log("\nDone!")

# =========================
# GUI SETUP
# =========================
root = tk.Tk()
root.title("File Organizer")
root.geometry("400x500")

title = tk.Label(root, text="📂 Android File Organizer", font=("Arial", 14))
title.pack(pady=10)

start_btn = tk.Button(root, text="Start Organizing", command=organize_files, bg="green", fg="white")
start_btn.pack(pady=10)

output_box = scrolledtext.ScrolledText(root, width=45, height=20)
output_box.pack(pady=10)

root.mainloop()