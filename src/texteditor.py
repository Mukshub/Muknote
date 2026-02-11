import tkinter as tk
from idlelib.configdialog import font_sample_text
from importlib.resources import contents
from os import write
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox


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



def main():
    # Making the Window itself
    window = tk.Tk()
    window.title("Muksnote")
    window.rowconfigure(0, minsize=25)
    window.columnconfigure(1, minsize=30)

    # Editable Text
    text_edit = tk.Text(window, font=("Minecraft", 12), undo=True, maxundo=-1,)
    text_edit.grid(row=0, column=1)

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

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_file(window, text_edit), accelerator="Ctrl+N")
    file_menu.add_command(label="Open", command=lambda: new_file(window, text_edit), accelerator="Ctrl+O")
    file_menu.add_command(label="New", command=lambda: save_file(window, text_edit), accelerator="Ctrl+S")
    file_menu.add_command(label="Close", command=window.quit, accelerator="Ctrl+W")

    # EDIT MENU
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    text_edit.event_generate("<<Undo>>")
    text_edit.event_generate("<<Redo>>")

    edit_menu.add_command(label="Undo", command=lambda: text_edit.event_generate("<<Undo>>"), accelerator="Ctrl+Z")
    edit_menu.add_command(label="Redo", command=lambda: text_edit.event_generate("<<Redo>>"), accelerator="Ctrl+Y")

    edit_menu.add_command(label="Cut", command=lambda: text_edit.event_generate("<<Cut>>"), accelerator="Ctrl+X")
    edit_menu.add_command(label="Copy", command=lambda: text_edit.event_generate("<<Copy>>"), accelerator="Ctrl+C")
    edit_menu.add_command(label="Cut", command=lambda: text_edit.event_generate("<<Paste>>"), accelerator="Ctrl+V")
    edit_menu.add_command(label="Delete", command=lambda: text_edit.event_generate("<<Paste>>"), accelerator="Del//BackSpace")











    window.bind("<Control-o>", lambda x: open_file(window, text_edit))
    window.bind("<Control-s>", lambda x: save_file(window, text_edit))
    window.bind("<Control-n>", lambda event: new_file(window, text_edit))
    window.bind("<Control-w>", lambda x: window.quit())

    window.mainloop()

main()