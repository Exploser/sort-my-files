import os
import shutil
import signal
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess

# Global variable to store sudo password
sudo_password = None

# Function to list files in a directory, excluding certain files, folders, and extensions
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
            relative_path = os.path.relpath(os.path.join(root, file), abs_directory)
            file_list.append(relative_path)
    return file_list

# Function to display files in the listbox
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
    
# Function to exclude selected files from the listbox
def exclude_selected_files():
    selected_indices = listbox_files.curselection()
    for index in selected_indices[::-1]:  # Reverse order to avoid index shift
        file = listbox_files.get(index)
        entry_exclude.insert(tk.END, f"{os.path.basename(file)} ")
        listbox_files.delete(index)

# Function to exclude the path of selected files from the listbox
def exclude_selected_paths():
    selected_indices = listbox_files.curselection()
    for index in selected_indices[::-1]:  # Reverse order to avoid index shift
        file = listbox_files.get(index)
        entry_exclude_folders.insert(tk.END, f"{os.path.dirname(file)} ")
        listbox_files.delete(index)

# Function to prompt for sudo password and store it
def get_sudo_permission():
    global sudo_password
    sudo_password = simpledialog.askstring("Sudo Password", "Please enter your sudo password:", show='*')
    if sudo_password is None:
        messagebox.showwarning("Warning", "Sudo permission not granted.")
        return False
    return True

# Function to run a command with stored sudo password
def run_with_sudo(command):
    global sudo_password
    if sudo_password is None:
        messagebox.showwarning("Warning", "Sudo permission not granted.")
        return False
    try:
        result = subprocess.run(['sudo', '-S'] + command, input=sudo_password + '\n', text=True, capture_output=True)
        if result.returncode != 0:
            messagebox.showerror("Error", f"Command failed with error: {result.stderr}")
            return False
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

# Function to organize files by moving or copying them based on their extensions
def organize_files(mode):
    if sudo_password is None:
        warning = messagebox.askyesno("Warning", "Sudo permission not granted. Do you want to continue?")
        if not warning:
            return

    directory = entry_directory.get()
    ignore_files = entry_ignore.get().split()
    exclude_files = entry_exclude.get().split()
    exclude_folders = entry_exclude_folders.get().split()
    include_extensions = entry_include.get().split()

    if not directory:
        messagebox.showerror("Error", "Please select a directory.")
        return

    abs_directory = os.path.abspath(directory)
    commands = []
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
                commands.append(['mv', source_path, destination_path])
            elif mode == 'copy':
                commands.append(['cp', '-r', source_path, destination_path])

    if commands:
        for command in commands:
            if sudo_password is not None and not run_with_sudo(command):
                return
            elif sudo_password is None:
                try:
                    if mode == 'move':
                        shutil.move(command[1], command[2])
                    elif mode == 'copy':
                        shutil.copy2(command[1], command[2])
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return
        messagebox.showinfo("Success", f"Files organized successfully by {mode}.")

# Function to select a directory using a file dialog
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

# Function to close the application
def close_app():
    app.quit()
    app.destroy()

# Function to handle interrupt signals and close the application gracefully
def signal_handler(sig, frame):
    print("Interrupt received, closing the application...")
    close_app()

# Set up the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Initialize the main application window
app = tk.Tk()
app.title("Sort my Stuff")

# Create the main frame with padding
frame = ttk.Frame(app, padding="10 10 10 10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

# Directory selection widgets
label_directory = ttk.Label(frame, text="Directory:")
label_directory.grid(row=0, column=0, sticky=tk.W, pady=5)

entry_directory = ttk.Entry(frame, width=40)
entry_directory.grid(row=0, column=1, pady=5, padx=5)

button_browse = ttk.Button(frame, text="Browse", command=select_directory)
button_browse.grid(row=0, column=2, pady=5)

# Ignore files input
label_ignore = ttk.Label(frame, text="Ignore Files (space-separated):")
label_ignore.grid(row=1, column=0, sticky=tk.W, pady=5)

entry_ignore = ttk.Entry(frame, width=40)
entry_ignore.grid(row=1, column=1, pady=5, padx=5)

# Exclude files input
label_exclude = ttk.Label(frame, text="Exclude Files (space-separated):")
label_exclude.grid(row=2, column=0, sticky=tk.W, pady=5)

entry_exclude = ttk.Entry(frame, width=40)
entry_exclude.grid(row=2, column=1, pady=5, padx=5)

# Exclude folders input
label_exclude_folders = ttk.Label(frame, text="Exclude Folders (space-separated):")
label_exclude_folders.grid(row=3, column=0, sticky=tk.W, pady=5)

entry_exclude_folders = ttk.Entry(frame, width=40)
entry_exclude_folders.grid(row=3, column=1, pady=5, padx=5)

# Include extensions input
label_include = ttk.Label(frame, text="Include Extensions (space-separated):")
label_include.grid(row=4, column=0, sticky=tk.W, pady=5)

entry_include = ttk.Entry(frame, width=40)
entry_include.grid(row=4, column=1, pady=5, padx=5)

# Display files button
button_display = ttk.Button(frame, text="Display Files", command=display_files)
button_display.grid(row=5, columnspan=3, pady=10)

# Listbox to display files
listbox_files = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=60, height=15)
listbox_files.grid(row=6, columnspan=3, pady=5)

# Exclude selected files button
button_exclude = ttk.Button(frame, text="Exclude Selected", command=exclude_selected_files)
button_exclude.grid(row=7, column=0, pady=10)

# Exclude selected paths button
button_exclude_paths = ttk.Button(frame, text="Exclude Selected Paths", command=exclude_selected_paths)
button_exclude_paths.grid(row=7, column=1, pady=10)

# Sudo permission button
button_sudo = ttk.Button(frame, text="Get Sudo Permission", command=get_sudo_permission)
button_sudo.grid(row=7, column=2, pady=10)

# Move files button
button_move = ttk.Button(frame, text="Move Files", command=lambda: organize_files('move'))
button_move.grid(row=8, column=0, pady=10)

# Copy files button
button_copy = ttk.Button(frame, text="Copy Files", command=lambda: organize_files('copy'))
button_copy.grid(row=8, column=1, pady=10)

# Close application button
button_close = ttk.Button(frame, text="Close", command=close_app)
button_close.grid(row=8, column=2, pady=10)

# Add padding to all child widgets
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

# Start the main event loop
app.mainloop()
