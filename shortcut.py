import os
import subprocess

def delete_file_explorer_shortcut():
    # Determine the directory containing the shortcuts
    desktop_dir = os.path.expanduser('~/.local/share/applications/')

    # Determine the path for the File Explorer shortcut
    shortcut_file = os.path.join(desktop_dir, "FileExplorer.desktop")

    # Check if the File Explorer shortcut exists
    if os.path.exists(shortcut_file):
        # Delete the shortcut file
        os.remove(shortcut_file)
        print("File Explorer shortcut deleted successfully!")
    else:
        print("File Explorer shortcut does not exist.")
        
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
