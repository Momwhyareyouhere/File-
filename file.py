import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import shutil
import subprocess

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.intro_label = tk.Label(root, text="Loading", font=("Arial", 24))
        self.intro_label.pack(pady=50)
        
        self.root.after(2000, self.start_app)
        
        self.context_menu = None
        self.file_to_copy = None
    
    def start_app(self):
        self.intro_label.destroy()
        
        self.current_directory = os.getcwd()
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.listbox.bind("<Double-Button-1>", self.open_item)
        self.listbox.bind("<Button-3>", self.show_context_menu)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Create File", command=self.create_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Create Folder", command=self.create_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Fullscreen", command=self.toggle_fullscreen).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Rename", command=self.rename_file).pack(side=tk.LEFT, padx=5)
        
        self.arrow_label = tk.Label(self.root, text="←", font=("Arial", 16))
        self.arrow_label.place(relx=0.98, rely=0.02, anchor="ne")
        self.arrow_label.bind("<Button-1>", self.go_back)
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Resize Window", command=self.resize_window)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        self.refresh_list()
        
    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
    
    def resize_window(self):
        size_str = simpledialog.askstring("Resize Window", "Enter width x height (e.g., 800x600):")
        if size_str:
            try:
                width, height = map(int, size_str.split("x"))
                self.root.geometry(f"{width}x{height}")
            except ValueError:
                messagebox.showerror("Error", "Invalid input format. Please use 'width x height' format (e.g., 800x600).")
    
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        files = os.listdir(self.current_directory)
        for file in files:
            if os.path.isdir(os.path.join(self.current_directory, file)):
                self.listbox.insert(tk.END, "📁 " + file)
            else:
                self.listbox.insert(tk.END, "📄 " + file)
            
    def delete_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            filename = self.listbox.get(selected_index[0])
            filename = filename.split(" ", 1)[1]
            full_path = os.path.join(self.current_directory, filename)
            if os.path.isdir(full_path):
                confirmation = messagebox.askyesno("Delete Directory", f"Are you sure you want to delete the directory '{filename}'?")
                if confirmation:
                    os.rmdir(full_path)
            else:
                confirmation = messagebox.askyesno("Delete File", f"Are you sure you want to delete the file '{filename}'?")
                if confirmation:
                    os.remove(full_path)
            self.refresh_list()
    
    def rename_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            filename = self.listbox.get(selected_index[0])
            filename = filename.split(" ", 1)[1]
            new_name = simpledialog.askstring("Rename File", "Enter new name:", initialvalue=filename)
            if new_name:
                os.rename(os.path.join(self.current_directory, filename), os.path.join(self.current_directory, new_name))
                self.refresh_list()

    def create_file(self):
        filename = simpledialog.askstring("Create File", "Enter file name:")
        if filename:
            with open(os.path.join(self.current_directory, filename), "w"):
                pass
            self.refresh_list()
    
    def create_folder(self):
        foldername = simpledialog.askstring("Create Folder", "Enter folder name:")
        if foldername:
            os.makedirs(os.path.join(self.current_directory, foldername))
            self.refresh_list()
    
    def edit_file(self, filename):
        try:
            subprocess.run(["code", "--version"], check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["code", filename])
        except FileNotFoundError:
            self.open_text_editor(filename)

    def open_text_editor(self, filename):
        text_editor_window = tk.Toplevel(self.root)
        text_editor_window.title(f"Text Editor - {filename}")
        
        webview.create_window("Text Editor", html=f"<textarea id='editor'></textarea>", width=800, height=600)
        webview.start()
        
        with open(os.path.join(self.current_directory, filename), "r") as file:
            content = file.read()
            webview.evaluate_js(f"document.getElementById('editor').value = {content!r}")
        
        def save_callback(editor_content):
            with open(os.path.join(self.current_directory, filename), "w") as file:
                file.write(editor_content)
            messagebox.showinfo("Save", "File saved successfully.")
            text_editor_window.destroy()
        
        webview.expose(save_callback, "save_callback")
        
    def open_item(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            item = self.listbox.get(selected_index[0])
            item_name = item.split(" ", 1)[1]
            full_path = os.path.join(self.current_directory, item_name)
            if "📁" in item:
                self.current_directory = full_path
                self.refresh_list()
            else:
                self.edit_file(item_name)

    def go_back(self, event=None):
        self.current_directory = os.path.dirname(self.current_directory)
        self.refresh_list()
        
    def show_context_menu(self, event):
        if self.context_menu:
            self.context_menu.destroy()
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Refresh", command=self.refresh_list)
        menu.add_command(label="Go Back", command=self.go_back)
        menu.add_command(label="Create File", command=self.create_file)
        menu.add_command(label="Create Folder", command=self.create_folder)
        menu.add_command(label="Paste", command=self.paste_file)
        
        selected_index = self.listbox.nearest(event.y)
        if selected_index:
            item = self.listbox.get(selected_index)
            if "📄" in item:
                menu.add_command(label="Copy", command=self.copy_file)
                menu.add_command(label="Rename", command=self.rename_file)
                menu.add_command(label="Edit", command=lambda: self.edit_file(item.split(" ", 1)[1]))
                menu.add_command(label="Delete", command=self.delete_file)
            elif "📁" in item:
                menu.add_command(label="Look Inside", command=lambda: self.look_inside(item))
        
        menu.post(event.x_root, event.y_root)
        self.context_menu = menu
        
    def look_inside(self, foldername):
        foldername = foldername.split(" ", 1)[1]
        self.current_directory = os.path.join(self.current_directory, foldername)
        self.refresh_list()
        
    def copy_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.file_to_copy = self.listbox.get(selected_index[0])
            self.file_to_copy = self.file_to_copy.split(" ", 1)[1]
    
    def paste_file(self):
        if self.file_to_copy:
            selected_index = self.listbox.curselection()
            if selected_index:
                destination = self.listbox.get(selected_index[0])
                destination = destination.split(" ", 1)[1]
                full_path_to_copy = os.path.join(self.current_directory, self.file_to_copy)
                destination_path = os.path.join(self.current_directory, destination)
                if full_path_to_copy != destination_path:
                    if os.path.isfile(full_path_to_copy):
                        shutil.copy(full_path_to_copy, destination_path)
                elif os.path.isdir(full_path_to_copy):
                    shutil.copytree(full_path_to_copy, os.path.join(destination_path, os.path.basename(full_path_to_copy)))
                self.refresh_list()
            else:
                messagebox.showerror("Error", "Cannot paste file to itself.")

                
if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
