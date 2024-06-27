File Organizer

A simple Python GUI application to organize files in a directory based on their extensions. You can ignore specific files, exclude selected files, and choose to either move or copy the files into corresponding folders.
Features

    Browse and select a directory to organize.
    Ignore files by specifying their names.
    Exclude files by selecting them from the displayed list.
    Organize files by moving or copying them into folders based on their extensions.
    Graceful handling of interrupts (e.g., Ctrl+C).

Requirements

    Python 3.x
    tkinter module (comes pre-installed with Python)

Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/file-organizer.git
cd file-organizer

Ensure tkinter is installed. On some systems, you might need to install it separately:

    For Ubuntu/Debian-based systems:

    bash

sudo apt-get install python3-tk

For Fedora/RHEL-based systems:

bash

        sudo dnf install python3-tkinter

Usage

    Run the script:

    bash

    python organize_files_gui.py

    Use the GUI to:
        Browse: Select the directory to organize.
        Ignore Files: Enter space-separated file names to ignore.
        Exclude Files: Display files in the selected directory, select files to exclude, and click "Exclude Selected" to add them to the exclude list.
        Move/Copy Files: Choose to move or copy the files into folders based on their extensions.
        Close: Exit the application.

Screenshot
    ![image](https://github.com/Exploser/sort--my-files/assets/126280113/2c711a92-073d-42e1-aef8-17a79544cac7)




License

This project is licensed under the MIT License.
