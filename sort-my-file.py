import os
import shutil
import argparse

def organize_files(directory, ignore_files, exclude_extensions, mode):
    # Get the absolute path of the directory
    abs_directory = os.path.abspath(directory)

    # Walk through the directory tree
    for root, dirs, files in os.walk(abs_directory):
        for file in files:
            # Skip files in the ignore list
            if file in ignore_files:
                continue
            
            # Get file extension
            file_extension = os.path.splitext(file)[1][1:]  # Remove the dot
            if not file_extension or file_extension in exclude_extensions:
                continue  # Skip files without extension or with excluded extensions

            # Create the directory for the file extension if it doesn't exist
            extension_dir = os.path.join(abs_directory, file_extension)
            if not os.path.exists(extension_dir):
                os.makedirs(extension_dir)

            # Move or copy the file to the new directory
            source_path = os.path.join(root, file)
            destination_path = os.path.join(extension_dir, file)
            if mode == 'move':
                shutil.move(source_path, destination_path)
                print(f'Moved {file} to {extension_dir}')
            elif mode == 'copy':
                shutil.copy2(source_path, destination_path)
                print(f'Copied {file} to {extension_dir}')

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Organize files by extension in a directory tree.')
    parser.add_argument('directory', help='The directory to organize')
    parser.add_argument('--ignore', nargs='*', default=[], help='Files to ignore')
    parser.add_argument('--exclude-extensions', nargs='*', default=[], help='File extensions to exclude')
    parser.add_argument('--mode', choices=['move', 'copy'], default='move', help='Mode to organize files: move or copy')
    args = parser.parse_args()

    organize_files(args.directory, args.ignore, args.exclude_extensions, args.mode)

