import os
import subprocess
import sys
from tkinter import Tk, Text, END, Button, Toplevel, Label, Scrollbar, Frame, StringVar, Radiobutton
import re  

def install_missing_package(packageName):
    subprocess.check_call([sys.executable, "-m", "pip", "install", packageName])

# Attempt to import tkinterdnd2, install it if import fails
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    install_missing_package("tkinterdnd2")
    from tkinterdnd2 import DND_FILES, TkinterDnD
    
# this allows the copied contenst to remain present in the Windows environment even after you close the interface
# Attempt to import pyperclip, install it if import fails
try:
    import pyperclip
except ImportError:
    install_missing_package("pyperclip")
    import pyperclip

import re

def convert_filename_to_lora(filename):
    
    match = re.search(r'step\d+', filename)
    if match:
        return match.group() 
    else:
        return ""

def drop(event):
    # Check if the event.data contains curly braces indicating the presence of spaces in file paths
    if "{" in event.data and "}" in event.data:
        # Use a regular expression to find all file paths enclosed in curly braces
        file_paths = re.findall(r'\{(.*?)\}', event.data)
    else:
        # If no curly braces are found, split the string by spaces
        file_paths = event.data.split()

    file_info = []
    for file_path in file_paths:
        # Strip leading and trailing whitespace and braces, if any
        cleaned_file_path = file_path.strip().strip("{}")
        mod_time = os.path.getmtime(cleaned_file_path)
        file_info.append((cleaned_file_path, mod_time))

    # Sort files by modification time (oldest first)
    file_info.sort(key=lambda x: x[1])

    # Use the selected fileType
    selected_fileType = fileTypeVar.get()    

    file_names = ','.join(convert_filename_to_lora(os.path.basename(file_path)) for file_path, _ in file_info)
    
    text_box.delete(1.0, END)  # Clear the text box before adding new content
    text_box.insert(END, file_names)

    # Automatically copy the contents to clipboard
    copy_to_clipboard()


def copy_to_clipboard():
    text_to_copy = text_box.get("1.0", END)
    pyperclip.copy(text_to_copy.strip())
    show_tooltip("Copied")    

def show_tooltip(text):
    tooltip = Toplevel(root)
    tooltip.wm_overrideredirect(True)
    x = root.winfo_x()
    y = root.winfo_y()
    tooltip.geometry(f"+{x + 50}+{y + 50}")
    label = Label(tooltip, text=text, font=("Arial", 10), bg="yellow")
    label.pack()
    root.after(1500, tooltip.destroy)

# Initialize the main TkinterDnD window
root = TkinterDnD.Tk()
root.title("File Drag and Drop")
root.geometry('500x500')

# Define a StringVar to hold the selected fileType for radio buttons
fileTypeVar = StringVar(value="lora")

# Create a "Copy" button and place it below the radio buttons
copy_button = Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=1, column=0, columnspan=2, pady=5, sticky='ew')

# Create a Frame to hold the Text widget and Scrollbars, and place it below the "Copy" button
frame = Frame(root)
frame.grid(row=2, column=0, sticky='nsew', columnspan=2)

# Configure the grid layout
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a Text widget to display file names
text_box = Text(frame, wrap='none')  # Set wrap to 'none' for horizontal scrolling
text_box.grid(row=0, column=0, sticky='nsew')

# Create a vertical scrollbar
v_scroll = Scrollbar(frame, orient='vertical', command=text_box.yview)
v_scroll.grid(row=0, column=1, sticky='ns')
text_box['yscrollcommand'] = v_scroll.set

# Create a horizontal scrollbar
h_scroll = Scrollbar(frame, orient='horizontal', command=text_box.xview)
h_scroll.grid(row=1, column=0, sticky='ew')
text_box['xscrollcommand'] = h_scroll.set

# Configure the frame layout
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Configure TkinterDnD
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Run the GUI
root.mainloop()