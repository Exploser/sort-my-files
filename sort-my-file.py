import os
import shutil
import argparse

def organize_files(directory, ignore_files):
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
            if not file_extension:
                continue  # Skip files without extension

            # Create the directory for the file extension if it doesn't exist
            extension_dir = os.path.join(abs_directory, file_extension)
            if not os.path.exists(extension_dir):
                os.makedirs(extension_dir)

            # Move the file to the new directory
            source_path = os.path.join(root, file)
            destination_path = os.path.join(extension_dir, file)
            shutil.move(source_path, destination_path)
            print(f'Moved {file} to {extension_dir}')

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Organize files by extension in a directory tree.')
    parser.add_argument('directory', help='The directory to organize')
    parser.add_argument('--ignore', nargs='*', default=[], help='Files to ignore')
    args = parser.parse_args()

    organize_files(args.directory, args.ignore)

