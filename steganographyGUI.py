from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import steganographyBackEnd as steg

def browse_file(entry):
    """Opens a file dialog to select an image file."""
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.bmp")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def drag_and_drop(event, entry):
    """Handles drag-and-drop events to populate file paths."""
    file_path = event.data.strip()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def encode_action():
    """Handles encoding a message into an image."""
    try:
        image_path = encode_image_entry.get()
        message = message_entry.get("1.0", tk.END).strip()
        output_path = output_file_entry.get()
        if not image_path or not message or not output_path:
            raise ValueError("All fields are required.")
        steg.embed_message(image_path, message, output_path)
        messagebox.showinfo("Success", "Message encoded and saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_action():
    """Handles decoding a message from an image."""
    try:
        image_path = decode_image_entry.get()
        if not image_path:
            raise ValueError("Image file is required.")
        message = steg.decode_message(image_path)
        decoded_message_label.config(text=f"Decoded Message:\n{message}")
        decoded_message_label.update()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Initialize the main window with drag-and-drop support
root = TkinterDnD.Tk()
root.title("Steganography Tool")
root.geometry("600x400")
root.resizable(True, True)

# Style Configuration
style = ttk.Style()
style.configure("TFrame", padding=10)
style.configure("TLabel", padding=5)
style.configure("TButton", padding=5)

# Encoding Frame
encode_frame = ttk.Frame(root)
encode_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

ttk.Label(encode_frame, text="Encode Message", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

ttk.Label(encode_frame, text="Image File:").grid(row=1, column=0, sticky="e")
encode_image_entry = ttk.Entry(encode_frame, width=40)
encode_image_entry.grid(row=1, column=1)
encode_image_entry.drop_target_register(DND_FILES)
encode_image_entry.dnd_bind("<<Drop>>", lambda event: drag_and_drop(event, encode_image_entry))
ttk.Button(encode_frame, text="Browse", command=lambda: browse_file(encode_image_entry)).grid(row=1, column=2)

ttk.Label(encode_frame, text="Message:").grid(row=2, column=0, sticky="ne")
message_entry = tk.Text(encode_frame, width=40, height=5, wrap="word", font=("Helvetica", 10))
message_entry.grid(row=2, column=1, columnspan=2, pady=5)

ttk.Label(encode_frame, text="Output File:").grid(row=3, column=0, sticky="e")
output_file_entry = ttk.Entry(encode_frame, width=40)
output_file_entry.grid(row=3, column=1)
ttk.Button(encode_frame, text="Encode", command=encode_action).grid(row=3, column=2)

# Separator
ttk.Separator(root, orient="horizontal").grid(row=1, column=0, sticky="ew", padx=20, pady=10)

# Decoding Frame
decode_frame = ttk.Frame(root)
decode_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

ttk.Label(decode_frame, text="Decode Message", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

ttk.Label(decode_frame, text="Image File:").grid(row=1, column=0, sticky="e")
decode_image_entry = ttk.Entry(decode_frame, width=40)
decode_image_entry.grid(row=1, column=1)
decode_image_entry.drop_target_register(DND_FILES)
decode_image_entry.dnd_bind("<<Drop>>", lambda event: drag_and_drop(event, decode_image_entry))
ttk.Button(decode_frame, text="Browse", command=lambda: browse_file(decode_image_entry)).grid(row=1, column=2)

ttk.Button(decode_frame, text="Decode", command=decode_action).grid(row=2, column=1, pady=5)
decoded_message_label = ttk.Label(decode_frame, text="Decoded Message: ", wraplength=500, font=("Helvetica", 10), anchor="w", justify="left")
decoded_message_label.grid(row=3, column=0, columnspan=3, pady=10, sticky="w")

# Run the main loop
root.mainloop()
