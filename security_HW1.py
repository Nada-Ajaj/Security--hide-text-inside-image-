import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
restoreimage =None
coverage_image = None
secrete_text = ""
updated_image = None

def select_coverage_image():
    global coverage_image
    image_path = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("BMP files", "*.bmp")])
    if image_path:
        try:
            coverage_image = Image.open(image_path)
            coverage_image=coverage_image.resize((800, 500))
            resized_image = coverage_image.resize((800, 500))
            resized_image2 = coverage_image.resize((420, 230), Image.LANCZOS)  
            tk_img = ImageTk.PhotoImage(resized_image2)
            label_1.config(image=tk_img, text="Coverage Image")
            label_1.image = tk_img
           
        except Exception as e:
            messagebox.showerror("Error", f"Could not load the image: {str(e)}")


def embed_hidden_text(bits_count):
    global updated_image
    if coverage_image is None or not secrete_text:
        messagebox.showerror("Error", "Please choose a cover image and provide a hidden text first!")
        return

    text_with_delimiter = secrete_text + '#'
    binary_text = ''.join(format(ord(char), '08b') for char in text_with_delimiter)

    output_image = coverage_image.copy()
    pixel_data = list(output_image.getdata())

    new_pixel_data = []
    text_index = 0
    for pixel in pixel_data:
        if text_index < len(binary_text):
            new_pixel = list(pixel)
            for i in range(3):  # RGB channels
                if text_index < len(binary_text):
                    new_pixel[i] = (new_pixel[i] & ~(1 << (bits_count - 1))) | (int(binary_text[text_index]) << (bits_count - 1))
                    text_index += 1
            new_pixel_data.append(tuple(new_pixel))
        else:
            new_pixel_data.append(pixel)

    output_image.putdata(new_pixel_data)
    updated_image = output_image
    display_updated_image()

def display_updated_image():
    global updated_image
    if updated_image is None:
        messagebox.showerror("Error", "There is no modified image to display!")
        return

    resized_image2 = updated_image.resize((420, 230), Image.LANCZOS)  # Adjust dimensions to fit label size
    tk_img = ImageTk.PhotoImage(resized_image2)
    label_2.config(image=tk_img, text="Result Image")
    label_2.image = tk_img
    

def restore_hidden_text(bits_count):
    if restoreimage is None:
        messagebox.showerror("Error", "Please load an image with hidden text before attempting to restore it!")
        return

    restored_bits = []
    dataPixel = list(restoreimage.getdata())

    for pixel in dataPixel:
        for channel in pixel[:3]:
            restored_bits.append((channel >> (bits_count - 1)) & 1)

    binary_string = ''.join(str(bit) for bit in restored_bits)
    byte_segments = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    extracted_chars = []
    for byte in byte_segments:
        if len(byte) < 8:
            continue
        char = chr(int(byte, 2))
        if char == '#':
            break
        extracted_chars.append(char)

    restored_text = ''.join(extracted_chars)
    hidden_label.config(text=f"The Secret Text:\n{restored_text}")
    


def selsect_restored_image():
    global restoreimage
    image_path = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("BMP files", "*.bmp")])
    if image_path:
        try:
            restoreimage = Image.open(image_path)
            resized_image = restoreimage.resize((800, 500))
            resized_image2 = restoreimage.resize((420, 230), Image.LANCZOS)  # Adjust dimensions to fit label size
            tk_img = ImageTk.PhotoImage(resized_image2)
            label_2.config(image=tk_img, text="Result Image")
            label_2.image = tk_img

        except Exception as e:
            messagebox.showerror("Error", f"Could not load the image: {str(e)}")

def embed_text_wrapper():
    bits_num = get_selected_bits()
    if bits_num is not None:
        embed_hidden_text(bits_num)

def restore_text_wrapper():
    bits_num = get_selected_bits_restore()
    if bits_num is not None:
        restore_hidden_text(bits_num)

def get_selected_bits():
    if bits_selection.get() == 1:
        return 1
    elif bits_selection.get() == 2:
        return 2
    elif bits_selection.get() == 3:
        return 3
    else:
        messagebox.showerror("Error", "You need to select the number of bits.")
        return None

def get_selected_bits_restore():
    if bits_selection_restore.get() == 1:
        return 1
    elif bits_selection_restore.get() == 2:
        return 2
    elif bits_selection_restore.get() == 3:
        return 3
    else:
        messagebox.showerror("Error", "You need to select the number of bits.")
        return None

def clear_all():
    global coverage_image, secrete_text, updated_image
    coverage_image = None
    secrete_text = ""
    updated_image = None
    cover_label.config(text="Cover")
    if bits_selection_restore.get() == 0:
        label_1.config(image=None, text="Cover")
        label_1.image=None

    
    cover_label.config(text="Coverage image")
    label_2.config(image=None, text="Cover")
    label_2.image=None
    hidden_label.config(text="Secrete Text")
    bits_selection.set(0)
    bits_selection_restore.set(0)

    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

def save_updated_image():
    if updated_image is None:
        messagebox.showerror("Error", "No modified image to save!")
        return
    
    image_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp"), ("All files", "*.*")])
    if image_path:
        try:
            updated_image.save(image_path)
            messagebox.showinfo("Success", "Image saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the image: {str(e)}")

def selecttext():
    global secrete_text
    hidden_text_file = filedialog.askopenfilename(title="Select Secret Text", filetypes=[("Text files", "*.txt")])
    if hidden_text_file:
        try:
            with open(hidden_text_file, 'r') as file:
                secrete_text = file.read()
            hidden_label.config(text=f"The Secret Text:\n{secrete_text}")
        except Exception as e:
            messagebox.showerror("Error", f"Theres an error to read file: {str(e)}")

root = tk.Tk()
root.title("(Steganography) Hide Text In Image")
root.geometry("800x500")

bg_color = "#D3D3D3"  #  black color
label_bg_color = "#E6E6FA"  #  purple for labels
button_bg_color = "#6A5ACD"  # SlateBlue for buttons
button_fg_color = "white"

root.configure(bg=bg_color)

# Create header labels
cover_label = tk.Label(root, text="Coverage Image", bg=label_bg_color, width=35, height=10, font=('Arial', 14, 'bold'))
label_1 = tk.Label(root,text="Coverage Image", bg=label_bg_color, font=('Arial', 14, 'bold'))
hidden_label = tk.Label(root, text="Secrete Text", bg=label_bg_color, width=30, height=10, font=('Arial', 14, 'bold'))
result_label = tk.Label(root, text="Result Image", bg=label_bg_color, width=35, height=10, font=('Arial', 14, 'bold'))
label_2 = tk.Label(root,text="Result Image", bg=label_bg_color, font=('Arial', 14, 'bold'))
# Arrange header labels
cover_label.grid(row=0, column=0, padx=30, pady=15)
label_1.grid(row=0, column=0, padx=30, pady=15)
hidden_label.grid(row=0, column=1, padx=30, pady=15)
result_label.grid(row=0, column=2, padx=30, pady=15)
label_2.grid(row=0, column=2, padx=30, pady=15)

# Buttons for selecting image and secret text
select_secret_button = tk.Button(root, text="Uploade Secret Text", command=selecttext, width=20, height=2, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))
select_image_button = tk.Button(root, text="Select Coverage Image", command=select_coverage_image, width=20, height=2, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))

# Arrange buttons in a single row
select_image_button.grid(row=1, column=0, padx=10, pady=15)
select_secret_button.grid(row=1, column=1, padx=10, pady=15)

# Bits selection for embedding
bits_label = tk.Label(root, text="Select Number of Bits:", bg=label_bg_color, font=('Arial', 12))
bits_selection = tk.IntVar()
bit_option1 = tk.Radiobutton(root, text="1 Bit", variable=bits_selection, value=1, bg=bg_color, font=('Arial', 12))
bit_option2 = tk.Radiobutton(root, text="2 Bits", variable=bits_selection, value=2, bg=bg_color, font=('Arial', 12))
bit_option3 = tk.Radiobutton(root, text="3 Bits", variable=bits_selection, value=3, bg=bg_color, font=('Arial', 12))

# Arrange bits selection
bits_label.grid(row=2, column=0, padx=30, pady=5, columnspan=3)  # Centered over options
bit_option1.grid(row=3, column=0, padx=30, pady=5)
bit_option2.grid(row=3, column=1, padx=30, pady=5)
bit_option3.grid(row=3, column=2, padx=30, pady=5)



embed_text_button = tk.Button(root, text="Hide Text", command=embed_text_wrapper, width=15, height=1, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))
save_button = tk.Button(root, text="Save Updated Image", command=save_updated_image, width=15, height=1, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))
reset_button = tk.Button(root, text="Clear All", command=clear_all, width=15, height=1, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))


embed_text_button.grid(row=4, column=0, padx=10, pady=15)
reset_button.grid(row=4, column=1, padx=10, pady=15)
save_button.grid(row=4, column=2, padx=10, pady=15)

# Restore Bits selection (for restoring hidden text)
bits_label_restore = tk.Label(root, text="Select Number of Bits (Restore):", bg=label_bg_color, font=('Arial', 12))
bits_selection_restore = tk.IntVar()
bit_option1_restore  = tk.Radiobutton(root, text="1 Bit", variable=bits_selection_restore, value=1, bg=bg_color, font=('Arial', 12))
bit_option2_restore  = tk.Radiobutton(root, text="2 Bits", variable=bits_selection_restore, value=2, bg=bg_color, font=('Arial', 12))
bit_option3_restore  = tk.Radiobutton(root, text="3 Bits", variable=bits_selection_restore, value=3, bg=bg_color, font=('Arial', 12))

# Load Image to Restore button
loadrestoreimg = tk.Button(root, text="upload Image to Restore", command=selsect_restored_image, width=20, height=1, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))
loadrestoreimg.grid(row=5, column=1, padx=10, pady=15)  # Positioned below the restore text button
# Arrange restore bits selection
bits_label_restore.grid(row=6, column=0, padx=30, pady=5, columnspan=3)  # Centered over options
bit_option1_restore.grid(row=7, column=0, padx=30, pady=5)
bit_option2_restore.grid(row=7, column=1, padx=30, pady=5)
bit_option3_restore.grid(row=7, column=2, padx=30, pady=5)

# Restore Text button under restore options
retrieve_button = tk.Button(root, text="Restore Text", command=restore_text_wrapper, width=15, height=1, bg=button_bg_color, fg=button_fg_color, font=('Arial', 12))
retrieve_button.grid(row=8, column=1, padx=10, pady=15)  # Positioned directly below the restore bit options





root.mainloop()
