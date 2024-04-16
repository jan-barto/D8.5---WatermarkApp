from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk, ImageGrab


class WaterMarkingManager:
    def __init__(self):
        self.window = Tk()
        self.window.title("Watermarking Desktop App")
        self.window.config(padx=30, pady=30)
        self.canvas = Canvas(width=900, height=700)

        # images handling
        self.default_img = PhotoImage(file='logo.png')
        self.canvas_picture = self.canvas.create_image(400, 300, image=self.default_img)
        self.canvas.grid(row=0, column=0, rowspan=12)
        self.uploaded_img = None

        # control widgets
        label_file = Label(text="Soubor pro vodoznak:")
        label_file.grid(row=0, column=1, sticky="w", columnspan=2)

        button_load = Button(text="Načíst", width=7, command=self.load_file)
        button_load.grid(row=1, column=1, sticky="w", columnspan=2)

        button_reset = Button(text="Resetovat", command=self.reset_app)
        button_reset.grid(row=1, column=2, sticky="w")

        label_path = Label(text="Cesta k souboru:")
        label_path.grid(row=2, column=1, sticky="w", columnspan=2)

        self.label_path_file = Label(text="C:/ ???:", wraplength=200)
        self.label_path_file.grid(row=3, column=1, sticky="w", columnspan=2)

        label_text = Label(text="Text vodoznaku:")
        label_text.grid(row=8, column=1, sticky="w", columnspan=2)
        label_text.focus()

        self.entry_text = Entry(width=40)
        self.entry_text.grid(row=9, column=1, sticky="w", columnspan=2)
        self.entry_text.insert(END, "jan-barto")

        button_preview = Button(text="Přidat", command=self.add_mark)
        button_preview.grid(row=10, column=1, sticky="w")

        button_perform = Button(text="Uložit", command=self.save_file)
        button_perform.grid(row=10, column=2, sticky="w")

        # watermark text
        self.watermark = self.canvas.create_text(400, 300, text="", font=("Verdana", 80, "italic"), fill="gray",
                                                 angle=45)

        self.window.mainloop()

    def reset_app(self):
        self.canvas.itemconfig(self.canvas_picture, image=self.default_img)
        self.label_path_file.config(text="C:/ ???:", fg="BLACK")
        self.canvas.itemconfig(self.watermark, text="")

    def load_file(self):
        file_path = filedialog.askopenfilename()

        try:
            pil_img = Image.open(file_path)  # opening with Pillow (tkinter doesnt like jpg)
            resized_img = pil_img.resize(size=(800, 600))
            self.uploaded_img = ImageTk.PhotoImage(resized_img)
            self.canvas.itemconfig(self.canvas_picture, image=self.uploaded_img)
        except (PermissionError, PIL.UnidentifiedImageError):
            messagebox.showerror(title="Chyba při načítání.", message="Vyskytla se chyba. Zkuste to znovu.")
            self.reset_app()
        else:
            copied_image = pil_img.copy()
            self.label_path_file.config(text=file_path, fg="GREEN")

    def add_mark(self):
        mark_text = self.entry_text.get()
        self.canvas.itemconfig(self.watermark, text=mark_text)


    def save_file(self):
        x = self.window.winfo_rootx() + self.canvas.winfo_x() + 1
        y = self.window.winfo_rooty() + self.canvas.winfo_y() + 1

        x1 = x + 800
        y1 = y + 600

        screenshot = ImageGrab.grab(bbox=(x, y, x1, y1))
        screenshot.save("new_img.jpg")
        messagebox.showinfo(title="Hotovo.", message="Úspěšně uloženo.")


app = WaterMarkingManager()
