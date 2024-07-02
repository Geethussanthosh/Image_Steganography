import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk 
import os

def hide_message(image_path, message, output_path):
    img = Image.open(image_path)
    width, height = img.size
    message += "$"  # Adding a delimiter to indicate the end of the message

    # Convert each character of message to 8-bit binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Check if message can fit in the image
    if len(binary_message) > width * height:
        messagebox.showerror("Error", "Message is too long for this image.")
        return

    index = 0
    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))

            # Hide message in LSB of each RGB value
            for i in range(3):
                if index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[index])
                    index += 1

            img.putpixel((x, y), tuple(pixel))

    img.save(output_path)
    messagebox.showinfo("Success", "Message hidden successfully.")

def extract_message(image_path):
    img = Image.open(image_path)
    width, height = img.size

    binary_message = ""
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))

            # Extract LSB from each RGB value
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    # Extracting characters from binary message
    message = ""
    for i in range(0, len(binary_message), 8):
        char = chr(int(binary_message[i:i+8], 2))
        if char == "$":
            break
        message += char

    return message

def hide_message_gui():
    image_path = filedialog.askopenfilename(title="Select Image")
    if not image_path:
        return

    message = entry.get("1.0", tk.END)
    output_path = filedialog.asksaveasfilename(title="Save Image As", defaultextension=".png")
    if not output_path:
        return

    hide_message(image_path, message, output_path)

def extract_message_gui():
    image_path = filedialog.askopenfilename(title="Select Image")
    if not image_path:
        return

    extracted_message = extract_message(image_path)
    messagebox.showinfo("Extracted Message", extracted_message)

gui = ctk.CTk()
gui.geometry("400x400")
gui.title("LSB Image Steganography")
 # Load background image
bg_path =r'C:\Users\geeth\Downloads\image-steganography\bg.png'
if os.path.exists(bg_path):
     bg_img = Image.open(bg_path)
     bg_photo = ImageTk.PhotoImage(bg_img)
     bgl = tk.Label(gui, image=bg_photo)
     bgl.place(x=0, y=0)
else:
     messagebox.showerror("Error", "Background image not found.")
 
label = ctk.CTkLabel(gui, text="Enter message to hide:")

label.configure(font=("Times New Roman", 25))
label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
entry = ctk.CTkTextbox(gui, height=15, width=100)
entry.configure(font=("Times New Roman", 16))
entry.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
hide_button = ctk.CTkButton(gui, text="Hide Message", command=hide_message_gui)
hide_button.configure(font=("Times New Roman", 16))
hide_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
extract_button = ctk.CTkButton(gui, text="Extract Message", command=extract_message_gui)
extract_button.configure(font=("Times New Roman", 16))
extract_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
gui.mainloop()
