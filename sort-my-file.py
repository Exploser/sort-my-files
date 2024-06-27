import os
import shutil
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

def organize_files(directory, ignore_files, exclude_extensions, mode):
    abs_directory = os.path.abspath(directory)

    for root, dirs, files in os.walk(abs_directory):
        for file in files:
            if file in ignore_files:
                continue
            
            file_extension = os.path.splitext(file)[1][1:]
            if not file_extension or file_extension in exclude_extensions:
                continue

            extension_dir = os.path.join(abs_directory, file_extension)
            if not os.path.exists(extension_dir):
                os.makedirs(extension_dir)

            source_path = os.path.join(root, file)
            destination_path = os.path.join(extension_dir, file)
            if mode == 'move':
                shutil.move(source_path, destination_path)
                print(f'Moved {file} to {extension_dir}')
            elif mode == 'copy':
                shutil.copy2(source_path, destination_path)
                print(f'Copied {file} to {extension_dir}')

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

def run_organize_files():
    directory = entry_directory.get()
    ignore_files = entry_ignore.get().split()
    exclude_extensions = entry_exclude.get().split()
    mode = var_mode.get()

    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

    organize_files(directory, ignore_files, exclude_extensions, mode)
    messagebox.showinfo("Success", "Files organized successfully.")

app = tk.Tk()
app.title("File Organizer")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

label_directory = tk.Label(frame, text="Directory:")
label_directory.grid(row=0, column=0, sticky=tk.W, pady=5)

entry_directory = tk.Entry(frame, width=40)
entry_directory.grid(row=0, column=1, pady=5)

button_browse = tk.Button(frame, text="Browse", command=select_directory)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_ignore = tk.Label(frame, text="Ignore Files (space-separated):")
label_ignore.grid(row=1, column=0, sticky=tk.W, pady=5)

entry_ignore = tk.Entry(frame, width=40)
entry_ignore.grid(row=1, column=1, pady=5)

label_exclude = tk.Label(frame, text="Exclude Extensions (space-separated):")
label_exclude.grid(row=2, column=0, sticky=tk.W, pady=5)

entry_exclude = tk.Entry(frame, width=40)
entry_exclude.grid(row=2, column=1, pady=5)

label_mode = tk.Label(frame, text="Mode:")
label_mode.grid(row=3, column=0, sticky=tk.W, pady=5)

var_mode = tk.StringVar(value="move")
radio_move = tk.Radiobutton(frame, text="Move", variable=var_mode, value="move")
radio_move.grid(row=3, column=1, sticky=tk.W, pady=5)
radio_copy = tk.Radiobutton(frame, text="Copy", variable=var_mode, value="copy")
radio_copy.grid(row=3, column=1, pady=5)

button_run = tk.Button(frame, text="Organize Files", command=run_organize_files)
button_run.grid(row=4, columnspan=3, pady=10)

app.mainloop()

