import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# === Global summary data ===
summary_stats = {
    "modified": 0,
    "deleted": 0,
    "added": 0,
    "scanned": 0,
    "directory": ""
}

# === Function to compute SHA-256 hash ===
def compute_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None  # Skip unreadable files

# === Function to scan a directory ===
def scan_directory(directory):
    hash_data = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = compute_hash(full_path)
            if file_hash:
                hash_data[full_path] = file_hash
    return hash_data

# === GUI Button Functions ===
def select_directory():
    path = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, path)

def save_baseline():
    directory = directory_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory selected.")
        return
    hashes = scan_directory(directory)
    with open("baseline.json", 'w') as f:
        json.dump(hashes, f, indent=4)
    report_text.configure(state='normal')
    report_text.delete('1.0', tk.END)
    report_text.insert(tk.END, f"✅ Baseline saved for:\n{directory}\n", "success")
    report_text.insert(tk.END, f"📦 Total files recorded: {len(hashes)}\n", "info")
    report_text.configure(state='disabled')

def check_integrity():
    directory = directory_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory selected.")
        return

    try:
        with open("baseline.json", 'r') as f:
            old_hashes = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Baseline file not found. Please save it first.")
        return

    new_hashes = scan_directory(directory)

    # Reset summary data
    summary_stats["modified"] = summary_stats["deleted"] = summary_stats["added"] = 0
    summary_stats["scanned"] = len(new_hashes)
    summary_stats["directory"] = directory

    report_text.configure(state='normal')
    report_text.delete('1.0', tk.END)
    report_text.insert(tk.END, f"🛡️ File Integrity Report for:\n{directory}\n", "heading")
    report_text.insert(tk.END, "-" * 60 + "\n")

    for path in old_hashes:
        if path not in new_hashes:
            report_text.insert(tk.END, f"❌ Deleted: {path}\n", "deleted")
            summary_stats["deleted"] += 1
        elif old_hashes[path] != new_hashes[path]:
            report_text.insert(tk.END, f"⚠️ Modified: {path}\n", "modified")
            summary_stats["modified"] += 1

    for path in new_hashes:
        if path not in old_hashes:
            report_text.insert(tk.END, f"🆕 New File: {path}\n", "new")
            summary_stats["added"] += 1

    report_text.insert(tk.END, "\nSummary:\n", "heading")
    report_text.insert(tk.END, f"🔄 Modified: {summary_stats['modified']}\n", "modified")
    report_text.insert(tk.END, f"🗑️ Deleted: {summary_stats['deleted']}\n", "deleted")
    report_text.insert(tk.END, f"➕ New Files: {summary_stats['added']}\n", "new")
    report_text.insert(tk.END, f"📄 Total Scanned Now: {summary_stats['scanned']}\n", "info")
    report_text.configure(state='disabled')

def show_scanned_files():
    directory = directory_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "Invalid directory selected.")
        return
    report_text.configure(state='normal')
    report_text.delete('1.0', tk.END)
    report_text.insert(tk.END, f"🔍 Scanning all files in:\n{directory}\n", "heading")
    report_text.insert(tk.END, "-" * 60 + "\n")
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            report_text.insert(tk.END, f"{path}\n")
            count += 1
    report_text.insert(tk.END, f"\n📦 Total files found: {count}\n", "info")
    report_text.configure(state='disabled')

def generate_summary_pdf():
    if not summary_stats["directory"]:
        messagebox.showinfo("Info", "Run 'Check Integrity' first to generate summary.")
        return

    filename = f"Integrity_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "🛡️ File Integrity Summary Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Directory Checked: {summary_stats['directory']}")
    c.drawString(50, height - 110, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 150, f"🔄 Modified Files: {summary_stats['modified']}")
    c.drawString(50, height - 170, f"🗑️ Deleted Files: {summary_stats['deleted']}")
    c.drawString(50, height - 190, f"➕ New Files: {summary_stats['added']}")
    c.drawString(50, height - 210, f"📄 Total Files Scanned: {summary_stats['scanned']}")

    c.save()
    messagebox.showinfo("PDF Saved", f"Summary PDF saved as:\n{filename}")

# === GUI Setup ===
root = tk.Tk()
root.title("File Integrity Checker")
root.geometry("850x620")
root.configure(bg="#f2f2f2")
root.resizable(False, False)

# === Styles ===
button_color = "#4CAF50"
button_fg = "#ffffff"
label_font = ("Helvetica", 12, "bold")
entry_font = ("Helvetica", 11)

# === Header ===
tk.Label(root, text="🛡️ File Integrity Checker", font=("Helvetica", 16, "bold"), bg="#f2f2f2", fg="#333").pack(pady=10)

# === Directory Selection ===
dir_frame = tk.Frame(root, bg="#f2f2f2")
dir_frame.pack(pady=10)

tk.Label(dir_frame, text="Select Directory to Monitor:", font=label_font, bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
directory_entry = tk.Entry(dir_frame, width=60, font=entry_font)
directory_entry.pack(side=tk.LEFT, padx=5)
tk.Button(dir_frame, text="Browse", bg=button_color, fg=button_fg, command=select_directory).pack(side=tk.LEFT)

# === Buttons Frame ===
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Save Baseline", bg=button_color, fg=button_fg, width=18, command=save_baseline).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Check Integrity", bg="#2196F3", fg="white", width=18, command=check_integrity).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Show All Files", bg="#FF9800", fg="white", width=18, command=show_scanned_files).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Summarize to PDF", bg="#9C27B0", fg="white", width=18, command=generate_summary_pdf).pack(side=tk.LEFT, padx=10)

# === Report Text Area ===
report_text = scrolledtext.ScrolledText(root, width=100, height=25, font=("Consolas", 10), state='disabled', wrap='word')
report_text.pack(pady=10)

# === Tag Colors ===
report_text.tag_config("heading", foreground="blue", font=("Consolas", 10, "bold"))
report_text.tag_config("modified", foreground="orange")
report_text.tag_config("deleted", foreground="red")
report_text.tag_config("new", foreground="green")
report_text.tag_config("success", foreground="green", font=("Consolas", 10, "bold"))
report_text.tag_config("info", foreground="purple")

root.mainloop()
