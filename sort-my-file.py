import os
import shutil
import signal
import tkinter as tk
from tkinter import filedialog, messagebox

def list_files(directory, ignore_files, exclude_extensions):
    file_list = []
    abs_directory = os.path.abspath(directory)
    for root, dirs, files in os.walk(abs_directory):
        for file in files:
            if file in ignore_files:
                continue
            file_extension = os.path.splitext(file)[1][1:]
            if not file_extension or file_extension in exclude_extensions:
                continue
            file_list.append(os.path.join(root, file))
    return file_list

def display_files():
    directory = entry_directory.get()
    ignore_files = entry_ignore.get().split()
    exclude_extensions = entry_exclude.get().split()
    
    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return
    
    files = list_files(directory, ignore_files, exclude_extensions)
    
    text_files.delete('1.0', tk.END)
    if files:
        for file in files:
            text_files.insert(tk.END, file + "\n")
    else:
        text_files.insert(tk.END, "No files to display.")
    
def organize_files(mode):
    directory = entry_directory.get()
    ignore_files = entry_ignore.get().split()
    exclude_extensions = entry_exclude.get().split()

    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

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

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

label_directory = tk.Label(frame, text="Directory:")
label_directory.grid(row=0, column=0, sticky=tk.W, pady=5)

entry_directory = tk.Entry(frame, width=40)
entry_directory.grid(row=0, column=1, pady=5, padx=5)

button_browse = tk.Button(frame, text="Browse", command=select_directory)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_ignore = tk.Label(frame, text="Ignore Files (space-separated):")
label_ignore.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

entry_ignore = tk.Entry(frame, width=40)
entry_ignore.grid(row=1, column=1, pady=5)

label_exclude = tk.Label(frame, text="Exclude Extensions (space-separated):")
label_exclude.grid(row=2, column=0, sticky=tk.W, pady=5)

entry_exclude = tk.Entry(frame, width=40)
entry_exclude.grid(row=2, column=1, pady=5)

button_display = tk.Button(frame, text="Display Files", command=display_files)
button_display.grid(row=3, columnspan=3, pady=10)

text_files = tk.Text(frame, width=60, height=15)
text_files.grid(row=4, columnspan=3, pady=5)

button_move = tk.Button(frame, text="Move Files", command=lambda: organize_files('move'))
button_move.grid(row=5, column=0, pady=10)

button_copy = tk.Button(frame, text="Copy Files", command=lambda: organize_files('copy'))
button_copy.grid(row=5, column=1, pady=10)

button_close = tk.Button(frame, text="Close", command=close_app)
button_close.grid(row=5, column=2, pady=10)

app.mainloop()

