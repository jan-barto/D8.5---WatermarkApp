from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk


class WaterMarkingManager:
    def __init__(self):
        self.window = Tk()
        self.window.title("Watermarking Desktop App")
        self.window.config(padx=30, pady=10)
        self.canvas = Canvas(width=850, height=610)

        # images handling
        self.default_img = PhotoImage(file='start.png')
        self.canvas_picture = self.canvas.create_image(400, 300, image=self.default_img)
        self.canvas.grid(row=0, column=0, rowspan=10)
        self.uploaded_img = None
        self.combined = None
        self.combined_tk = None
        self.file_path = None

        # control and display widgets
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
        label_text.grid(row=5, column=1, sticky="w", columnspan=2)
        label_text.focus()

        self.entry_text = Entry(width=40)
        self.entry_text.grid(row=6, column=1, sticky="w", columnspan=2)
        self.entry_text.insert(END, "©jan-barto")

        button_preview = Button(text="Přidat", command=self.add_mark_pil)
        button_preview.grid(row=7, column=1, sticky="w")

        button_perform = Button(text="Uložit", command=self.save_file)
        button_perform.grid(row=7, column=2, sticky="w")

        self.window.mainloop()

    def reset_app(self):
        self.canvas.itemconfig(self.canvas_picture, image=self.default_img)
        self.label_path_file.config(text="C:/ ???:", fg="BLACK")

    def load_file(self):
        self.file_path = filedialog.askopenfilename()

        try:
            pil_img = Image.open(self.file_path)  # opening with Pillow (tkinter doesnt like jpg)
            resized_img = pil_img.resize(size=(800, 600))
            self.uploaded_img = ImageTk.PhotoImage(resized_img)
            self.canvas.itemconfig(self.canvas_picture, image=self.uploaded_img)
        except (PermissionError, PIL.UnidentifiedImageError):
            messagebox.showerror(title="Chyba při načítání.", message="Vyskytla se chyba. Zkuste to znovu.")
            self.reset_app()
        else:
            self.label_path_file.config(text=self.file_path, fg="GREEN")

    def add_mark_pil(self):
        from PIL import Image, ImageFont, ImageDraw
        original_image = Image.open(self.file_path).convert("RGBA")
        copied_image = original_image.copy()

        image_width = original_image.size[0]
        image_height = original_image.size[1]

        # virtual layer for the text
        txt = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)

        text = self.entry_text.get()
        font = ImageFont.truetype('verdana.ttf', image_height / 5)
        _, _, w, h = d.textbbox((0, 0), text, font=font)

        d.text(((image_width - w) / 2, (image_height - h) / 2), text, fill=(0, 0, 0, 100), font=font)
        self.combined = Image.alpha_composite(copied_image, txt)

        # prepare for canvas preview
        target_resolution = (800, 600)
        combined_res = self.combined.resize(target_resolution)
        self.combined_tk = ImageTk.PhotoImage(combined_res)
        self.canvas.itemconfig(self.canvas_picture, image=self.combined_tk)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPG files", "*.jpg"),
                                                            ("All Files", "*.*")])
        if file_path:
            # Save the image
            to_save = self.combined.convert("RGB")
            to_save.save(file_path)
            messagebox.showinfo(title="Hotovo.", message="Úspěšně uloženo.")


app = WaterMarkingManager()
