import os

def delete_shortcut(shortcut_name):
    # Determine the path for the shortcut file
    desktop_dir = os.path.expanduser('~/.local/share/applications/')
    shortcut_file = os.path.join(desktop_dir, f"{shortcut_name}.desktop")

    # Check if the shortcut file exists
    if os.path.exists(shortcut_file):
        # Delete the shortcut file
        os.remove(shortcut_file)
        print(f"Shortcut '{shortcut_name}' deleted successfully!")
    else:
        print(f"Shortcut '{shortcut_name}' does not exist!")

# Example usage
if __name__ == "__main__":
    shortcut_name = "FileExplorer"
    delete_shortcut(shortcut_name)
