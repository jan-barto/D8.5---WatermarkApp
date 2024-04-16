from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import PIL
from PIL import Image, ImageTk, ImageGrab

global img


def reset_app():
    canvas.itemconfig(picture, image=myimg)
    label_path_file.config(text="C:/ ???:", fg="BLACK")
    canvas.itemconfig(watermark, text="")


def load_file():
    global img
    file_path = filedialog.askopenfilename()

    try:
        pil_img = Image.open(file_path)  # opening with Pillow (tkinter doesnt like jpg)
        resized_img = pil_img.resize(size=(800, 600))
        img = ImageTk.PhotoImage(resized_img)
        canvas.itemconfig(picture, image=img)
    except (PermissionError, PIL.UnidentifiedImageError):
        messagebox.showerror(title="Chyba při načítání.", message="Vyskytla se chyba. Zkuste to znovu.")
        reset_app()
    else:
        label_path_file.config(text=file_path, fg="GREEN")


def preview():
    mark_text = entry_text.get()
    canvas.itemconfig(watermark, text=mark_text)


def perform():
    x = window.winfo_rootx() + canvas.winfo_x() + 1
    y = window.winfo_rooty() + canvas.winfo_y() + 1

    x1 = x + 800
    y1 = y + 600

    screenshot = ImageGrab.grab(bbox=(x, y, x1, y1))
    screenshot.save("new_img.jpg")
    messagebox.showinfo(title="Hotovo.", message="Úspěšně uloženo.")


window = Tk()
window.title("Watermarking Desktop App")
window.config(padx=30, pady=30)

canvas = Canvas(width=900, height=700)
myimg = PhotoImage(file='logo.png')
picture = canvas.create_image(400, 300, image=myimg)
canvas.grid(row=0, column=0, rowspan=12)

watermark = canvas.create_text(400, 300, text="", font=("Verdana", 80, "italic"), fill="gray", angle=45)
label_file = Label(text="Soubor pro vodoznak:")
label_file.grid(row=0, column=1, sticky="w", columnspan=2)

button_load = Button(text="Načíst", width=7, command=load_file)
button_load.grid(row=1, column=1, sticky="w", columnspan=2)

button_reset = Button(text="Resetovat", command=reset_app)
button_reset.grid(row=1, column=2, sticky="w")

label_path = Label(text="Cesta k souboru:")
label_path.grid(row=2, column=1, sticky="w", columnspan=2)

label_path_file = Label(text="C:/ ???:", wraplength=200)
label_path_file.grid(row=3, column=1, sticky="w", columnspan=2)

label_text = Label(text="Text vodoznaku:")
label_text.grid(row=8, column=1, sticky="w", columnspan=2)
label_text.focus()

entry_text = Entry(width=40)
entry_text.grid(row=9, column=1, sticky="w", columnspan=2)
entry_text.insert(END, "jan-barto")

button_preview = Button(text="Přidat", command=preview)
button_preview.grid(row=10, column=1, sticky="w")

button_perform = Button(text="Uložit", command=perform)
button_perform.grid(row=10, column=2, sticky="w")

window.mainloop()
