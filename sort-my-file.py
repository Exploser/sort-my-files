import os
import shutil
import signal
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def list_files(directory, ignore_files, exclude_files, exclude_folders, include_extensions):
    file_list = []
    abs_directory = os.path.abspath(directory)
    for root, dirs, files in os.walk(abs_directory):
        if any(exclude_folder in root for exclude_folder in exclude_folders):
            continue
        for file in files:
            if file in ignore_files or file in exclude_files:
                continue
            file_extension = os.path.splitext(file)[1][1:]
            if include_extensions and file_extension not in include_extensions:
                continue
            file_list.append(os.path.join(root, file))
    return file_list

def display_files():
    directory = entry_directory.get()
    ignore_files = entry_ignore.get().split()
    exclude_files = entry_exclude.get().split()
    exclude_folders = entry_exclude_folders.get().split()
    include_extensions = entry_include.get().split()
    
    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return
    
    files = list_files(directory, ignore_files, exclude_files, exclude_folders, include_extensions)
    
    listbox_files.delete(0, tk.END)
    if files:
        for file in files:
            listbox_files.insert(tk.END, file)
    else:
        listbox_files.insert(tk.END, "No files to display.")
    
def exclude_selected_files():
    selected_indices = listbox_files.curselection()
    for index in selected_indices[::-1]:  # Reverse order to avoid index shift
        file = listbox_files.get(index)
        entry_exclude.insert(tk.END, f"{os.path.basename(file)} ")
        listbox_files.delete(index)

def organize_files(mode):
    directory = entry_directory.get()
    ignore_files = entry_ignore.get().split()
    exclude_files = entry_exclude.get().split()
    exclude_folders = entry_exclude_folders.get().split()
    include_extensions = entry_include.get().split()

    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

    abs_directory = os.path.abspath(directory)
    for root, dirs, files in os.walk(abs_directory):
        if any(exclude_folder in root for exclude_folder in exclude_folders):
            continue
        for file in files:
            if file in ignore_files or file in exclude_files:
                continue
            
            file_extension = os.path.splitext(file)[1][1:]
            if include_extensions and file_extension not in include_extensions:
                continue
            if not file_extension:
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
    
    messagebox.showinfo("Success", f"Files organized successfully by {mode}.")

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

def close_app():
    app.quit()
    app.destroy()

def signal_handler(sig, frame):
    print("Interrupt received, closing the application...")
    close_app()

# Set up the signal handler
signal.signal(signal.SIGINT, signal_handler)

app = tk.Tk()
app.title("File Organizer")

frame = ttk.Frame(app, padding="10 10 10 10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

label_directory = ttk.Label(frame, text="Directory:")
label_directory.grid(row=0, column=0, sticky=tk.W, pady=5)

entry_directory = ttk.Entry(frame, width=40)
entry_directory.grid(row=0, column=1, pady=5, padx=5)

button_browse = ttk.Button(frame, text="Browse", command=select_directory)
button_browse.grid(row=0, column=2, pady=5)

label_ignore = ttk.Label(frame, text="Ignore Files (space-separated):")
label_ignore.grid(row=1, column=0, sticky=tk.W, pady=5)

entry_ignore = ttk.Entry(frame, width=40)
entry_ignore.grid(row=1, column=1, pady=5, padx=5)

label_exclude = ttk.Label(frame, text="Exclude Files (space-separated):")
label_exclude.grid(row=2, column=0, sticky=tk.W, pady=5)

entry_exclude = ttk.Entry(frame, width=40)
entry_exclude.grid(row=2, column=1, pady=5, padx=5)

label_exclude_folders = ttk.Label(frame, text="Exclude Folders (space-separated):")
label_exclude_folders.grid(row=3, column=0, sticky=tk.W, pady=5)

entry_exclude_folders = ttk.Entry(frame, width=40)
entry_exclude_folders.grid(row=3, column=1, pady=5, padx=5)

label_include = ttk.Label(frame, text="Include Extensions (space-separated):")
label_include.grid(row=4, column=0, sticky=tk.W, pady=5)

entry_include = ttk.Entry(frame, width=40)
entry_include.grid(row=4, column=1, pady=5, padx=5)

button_display = ttk.Button(frame, text="Display Files", command=display_files)
button_display.grid(row=5, columnspan=3, pady=10)

listbox_files = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=60, height=15)
listbox_files.grid(row=6, columnspan=3, pady=5)

button_exclude = ttk.Button(frame, text="Exclude Selected", command=exclude_selected_files)
button_exclude.grid(row=7, column=0, pady=10)

button_move = ttk.Button(frame, text="Move Files", command=lambda: organize_files('move'))
button_move.grid(row=7, column=1, pady=10)

button_copy = ttk.Button(frame, text="Copy Files", command=lambda: organize_files('copy'))
button_copy.grid(row=7, column=2, pady=10)

button_close = ttk.Button(frame, text="Close", command=close_app)
button_close.grid(row=8, columnspan=3, pady=10)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

app.mainloop()
