import os
from tkinter import *
from tkinter import filedialog, messagebox

CONFIG_FILE = "config.txt"

# Function to load the saved file path
def load_saved_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config:
            path = config.read().strip()
            if os.path.exists(path):
                file_path_var.set(path)

# Function to save the file path for future use
def save_path(file_path):
    with open(CONFIG_FILE, "w") as config:
        config.write(file_path)

# Function to browse and select the license file
def browse_file():
    file_path = filedialog.askopenfilename(title="Select License File",
                                           filetypes=(("License Files", "*.lic"), ("All Files", "*.*")))
    if file_path:
        file_path_var.set(file_path)
        save_path(file_path)

# Function to extract license information
def check_expiration():
    file_path = file_path_var.get()
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Error", "Invalid file path. Please select a valid file.")
        return

    try:
        # Read the file content
        with open(file_path, "r") as file:
            content = file.readlines()

        # Regex pattern to match INCREMENT lines
        import re
        pattern = r"^INCREMENT\s+(\S+)\s+(\S+)\s+\S+\s+(\d{1,2}-\w{3}-\d{4})"

        results = []
        for line in content:
            match = re.match(pattern, line)
            if match:
                bundle_name = match.group(1)
                vendor = match.group(2)
                expire_date = match.group(3)
                results.append(f"Bundle: {bundle_name}, Vendor: {vendor}, Expiry: {expire_date}")

        # Display results in the text area
        text_area.delete(1.0, END)
        if results:
            text_area.insert(END, "\n".join(results))
            print(results)
        else:
            text_area.insert(END, "No license information found.")

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please check the file path.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        


# Create the main GUI window
window = Tk()
window.title("License Expiration Checker")
window.geometry("700x400")

# File path input
file_path_var = StringVar()

file_path_label = Label(window, text="License File Path:")
file_path_label.pack(pady=5)
file_path_entry = Entry(window, textvariable=file_path_var, width=50)
file_path_entry.pack(pady=5)

browse_button = Button(window, text="Browse", command=browse_file)
browse_button.pack(pady=5)

# Button to check license expiration
check_button = Button(window, text="Check Expiration", command=check_expiration)
check_button.pack(pady=10)

# Text area to display results
text_area = Text(window, wrap=WORD, height=15, width=80)
text_area.pack(pady=10)

# Load saved path if available
load_saved_path()

# Start the main GUI loop
window.mainloop()
