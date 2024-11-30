import tkinter as tk
from tkinter import filedialog, messagebox
from steganographyBackEnd import embed_message, decode_message

def encode_message():
    image_path = filedialog.askopenfilename(title="Select Image")
    if not image_path:
        return
    message = message_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Message cannot be empty!")
        return
    output_path = filedialog.asksaveasfilename(title="Save Encoded Image")
    if not output_path:
        return
    try:
        embed_message(image_path, message, output_path)
        messagebox.showinfo("Success", "Message successfully embedded!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed message: {e}")

def decode_message_action():
    image_path = filedialog.askopenfilename(title="Select Encoded Image")
    if not image_path:
        return
    try:
        hidden_message = decode_message(image_path)
        decoded_text.delete("1.0", tk.END)
        decoded_text.insert(tk.END, hidden_message)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode message: {e}")

# Main Window
root = tk.Tk()
root.title("Steganography Tool")

# Encoding Frame
encode_frame = tk.LabelFrame(root, text="Encode Message")
encode_frame.pack(fill="both", expand="yes", padx=10, pady=10)

tk.Label(encode_frame, text="Message:").pack(anchor="w")
message_entry = tk.Text(encode_frame, height=5, width=40)
message_entry.pack(pady=5)

encode_button = tk.Button(encode_frame, text="Embed Message", command=encode_message)
encode_button.pack(pady=10)

# Decoding Frame
decode_frame = tk.LabelFrame(root, text="Decode Message")
decode_frame.pack(fill="both", expand="yes", padx=10, pady=10)

decode_button = tk.Button(decode_frame, text="Extract Message", command=decode_message_action)
decode_button.pack(pady=10)

decoded_text = tk.Text(decode_frame, height=5, width=40)
decoded_text.pack(pady=5)

# Run the application
root.mainloop()
