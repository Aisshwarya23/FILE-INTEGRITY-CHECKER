# Cyber-Security-and-Ethical-Hacking

**COMPANY**: CODTECH IT SOLUTIONS
**NAME**: AISHWARYA C
**INTERN ID**: CT06DG624
**DOMAIN**: CYBER SECURITY AND ETHICAL HACKING
**DURATION**: 6 WEEKS
**MENTOR**: NEELA SANTOSH

# File Integrity Checker

A File Integrity Checker application with a graphical user interface (GUI) built using Python and Tkinter. This tool monitors file changes in a specified directory by comparing the current state against a previously saved baseline using SHA-256 hashes. It also allows users to generate a PDF summary report of the results.


## Features

- **Directory Selection** – Browse and select a directory to monitor.
- **Save Baseline** – Generate and store SHA-256 hashes of all files in the directory.
- **Check Integrity** – Detect:
  - Modified files
  - Deleted files
  - Newly added files
- **Show All Files** – Display a list of all files currently in the selected directory.
- **Generate PDF Summary** – Create a printable PDF report summarizing the integrity check.
- **User-Friendly GUI** – A clean, color-coded interface for easy navigation.



## Technologies & Tools Used

| Category         | Tools/Modules                     |
|------------------|------------------------------------|
| Language         | Python 3                           |
| GUI Framework    | `tkinter`, `tkinter.scrolledtext`  |
| File Hashing     | `hashlib` (SHA-256)                |
| File I/O         | `os`, `json`, `datetime`           |
| PDF Generation   | `reportlab`                        |



## How It Works

1. **Select Directory** – Choose the folder you want to monitor.
2. **Save Baseline** – Hashes of all files in the directory are saved to `baseline.json`.
3. **Check Integrity** – Compare current file hashes with the saved baseline:
   - Modified files have changed content.
   - Deleted files are missing from the current directory.
   - New files are added since the baseline was saved.
4. **View Report** – Results are shown in a styled text area.
5. **Generate PDF** – Summary statistics are saved to a formatted PDF file.



## Installation & Usage

### Requirements

- Python 3.x
- Required modules:
  ```bash
  pip install reportlab
