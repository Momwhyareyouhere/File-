import os
import subprocess

def delete_shortcuts():
    # Determine the directory containing the shortcuts
    desktop_dir = os.path.expanduser('~/.local/share/applications/')

    # List all files in the directory
    files = os.listdir(desktop_dir)

    # Iterate through each file
    for file_name in files:
        # Check if it's a file and ends with '.desktop'
        if os.path.isfile(os.path.join(desktop_dir, file_name)) and file_name.endswith('.desktop'):
            # Delete the file
            os.remove(os.path.join(desktop_dir, file_name))
            print(f"Shortcut '{file_name}' deleted successfully!")

def create_file_explorer_shortcut(script_path):
    # Construct the contents of the .desktop file for File Explorer
    shortcut_content = f"""[Desktop Entry]
Name=File Explorer
Exec=python3 {script_path}
Type=Application
Terminal=false
Icon=system-file-manager
"""

    # Determine the path for the shortcut file
    desktop_dir = os.path.expanduser('~/.local/share/applications/')
    shortcut_file = os.path.join(desktop_dir, "FileExplorer.desktop")

    # Write the contents to the shortcut file
    with open(shortcut_file, 'w') as f:
        f.write(shortcut_content)

    print("Shortcut 'File Explorer' created successfully!")

# Example usage
if __name__ == "__main__":
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the Python script (assuming it's named 'file.py' in the same directory)
    script_path = os.path.join(script_directory, 'file.py')

    # Delete existing shortcuts
    delete_shortcuts()

    # Create File Explorer shortcut
    create_file_explorer_shortcut(script_path)
