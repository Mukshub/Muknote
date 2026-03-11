import tkinter as tk
from tkinter import ttk

from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox

# The main window
window = tk.Tk()
window.iconbitmap("muknote.ico")

window.title("Muksnote")
window.rowconfigure(0, minsize=25)
window.columnconfigure(1, minsize=30)
window.config(background="white")


# Opening Files
def open_file(window, text_edit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return

    text_edit.delete(1.0, tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(tk.END, content)
    window.title(f"Open File: {filepath}")

# Saving Files
def save_file(window, text_edit):
    filepath= asksaveasfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return

    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content)
    window.title(f"Save File: {filepath}")

from tkinter import filedialog

def save_file_as(window, text_edit):

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    with open(file_path, "w") as f:
        text = text_edit.get("1.0", "end-1c")
        f.write(text)

    window.title(file_path)

# New File
def new_file(window, text_edit, event=None):
    if text_edit.edit_modified():
        text_edit.edit_modified(False)
        # save or overwrite current data
        response = messagebox.askyesnocancel("Confirm", "Do you want to save changes?")
        if response:
            save_file(window, text_edit)
        elif response is False:
            pass
        else:
            return
    text_edit.delete(1.0, tk.END)
    window.title("Untitled - Muknote")

# Preferences
def open_preferences():

    pref = tk.Toplevel(window)
    pref.title("Preferences")
    pref.geometry("400x300")

    pref.transient(window)
    pref.grab_set()

    notebook = ttk.Notebook(pref)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    #--Appearance--
    appearance_tab = ttk.Frame(notebook)
    notebook.add(appearance_tab, text="Appearance")

    theme = ttk.Combobox(appearance_tab, values=["Light", "Dark", "System"])
    theme.current(0)
    theme.pack(anchor="w", padx=20)

# Top bar
topbar = tk.Frame(window, bg="#e6e6e6", height=30)
topbar.pack(fill="x")

# Left side menus
file_btn = tk.Button(topbar, text="File", bd=0)
file_btn.pack(side="left", padx=5)

edit_btn = tk.Button(topbar, text="Edit", bd=0)
edit_btn.pack(side="left", padx=5)

# Spacer pushes gear right
spacer = tk.Frame(topbar)
spacer.pack(side="left", expand=True)

# Gear button
gear_btn = tk.Button(topbar, text="⚙", font=("Minecraft", 12),
                     bd=0, command=open_preferences)
gear_btn.pack(side="right", padx=8)

# Dark/Light modes
def switch():
    global switch_value
    if switch_value == True:
        switch.config(image=dark, bg="#26242f",
                      activebackground="#26242f")

        # Changes the window to dark theme
        window.config(bg="#26242f")
        switch_value = False

    else:
        switch.config(image=light, bg="white",
                      activebackground="white")

        # Changes the window to light theme
        window.config(bg="white")
        switch_value = True



def main():

    # Editable Text
    text_edit = tk.Text(window, font=("Minecraft", 12), undo=True, maxundo=-1,)
    text_edit.pack(fill="both", expand=True)

    # Buttons/Menu
    frame=tk.Frame(window, relief=tk.RAISED, bd=2)
    save_butt= (tk.Button
        (frame, text="Save", command=lambda: save_file(window, text_edit)))
    open_butt= (tk.Button
                (frame, text="Open", command=lambda: open_file(window, text_edit)))
    new_butt= (tk.Button
                (frame, text="New", command=lambda: new_file(window, text_edit)))

    # BUTTONS
    # save_butt.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    # open_butt.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    # new_butt.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    # frame.grid(row=0, column=0, sticky="ns")

    # FILE_MENU
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)

    # FILE MENU
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_file(window, text_edit), accelerator="Ctrl+N")
    file_menu.add_command(label="Open", command=lambda: new_file(window, text_edit), accelerator="Ctrl+O")
    file_menu.add_command(label="Save", command=lambda: save_file(window, text_edit), accelerator="Ctrl+S")
    file_menu.add_command(label="Save As", command=lambda: save_file_as(window, text_edit), accelerator="Ctrl+Shift+S")
    file_menu.add_command(label="Close", command=window.quit, accelerator="Ctrl+W")

    # EDIT MENU
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    text_edit.event_generate("<<Undo>>")
    text_edit.event_generate("<<Redo>>")

    edit_menu.add_separator()
    edit_menu.add_command(label="Undo", command=lambda: text_edit.event_generate("<<Undo>>"), accelerator="Ctrl+Z")
    edit_menu.add_command(label="Redo", command=lambda: text_edit.event_generate("<<Redo>>"), accelerator="Ctrl+Y")

    edit_menu.add_separator()
    edit_menu.add_command(label="Cut", command=lambda: text_edit.event_generate("<<Cut>>"), accelerator="Ctrl+X")
    edit_menu.add_command(label="Copy", command=lambda: text_edit.event_generate("<<Copy>>"), accelerator="Ctrl+C")
    edit_menu.add_command(label="Cut", command=lambda: text_edit.event_generate("<<Paste>>"), accelerator="Ctrl+V")
    edit_menu.add_command(label="Delete", command=lambda: text_edit.event_generate("<<Paste>>"), accelerator="Del//BackSpace")
    edit_menu.add_command(label="Select All", command=lambda: text_edit.event_generate("<<SelectAll>>"), accelerator="Ctrl+A")











    window.bind("<Control-o>", lambda x: open_file(window, text_edit))
    window.bind("<Control-s>", lambda x: save_file(window, text_edit))
    window.bind("<Control-Shift-s>", lambda x: save_file_as(window, text_edit))
    window.bind("<Control-n>", lambda event: new_file(window, text_edit))
    window.bind("<Control-w>", lambda x: window.quit())

    window.mainloop()

main()