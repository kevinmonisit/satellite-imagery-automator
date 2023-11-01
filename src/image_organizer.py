import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import shutil


class ImageOrganizer(tk.Tk):
    def __init__(self, image_dir, dir_y, dir_z):
        super().__init__()

        self.image_dir = image_dir
        self.dir_y = dir_y
        self.dir_z = dir_z
        self.image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
        self.undo_stack = []

        self.title('Image Organizer')
        self.geometry('800x600')

        self.label = tk.Label(self, text="Press L or R to move the image, Z to undo", font=("Helvetica", 16))
        self.label.pack()

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()

        self.bind("<Key>", self.key_pressed)
        self.load_image()

    def load_image(self):
        if self.image_files:
            image_path = os.path.join(self.image_dir, self.image_files[0])
            image = Image.open(image_path)
            image.thumbnail((500, 500))
            self.current_image = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(250, 250, anchor=tk.CENTER, image=self.current_image)
        else:
            messagebox.showinfo("Info", "No more images to display.")
            self.destroy()

    def key_pressed(self, event):
        if event.char == 'l':
            self.move_image(self.dir_y, prefix="0_")
        elif event.char == 'r':
            self.move_image(self.dir_z, prefix="1_")
        elif event.char == 'z':
            self.undo_move()

    def move_image(self, target_dir, prefix=""):
        if self.image_files:
            src_path = os.path.join(self.image_dir, self.image_files.pop(0))

            new_file_name = prefix + os.path.basename(src_path)
            shutil.move(src_path, os.path.join(target_dir, new_file_name))

            self.undo_stack.append((src_path, target_dir))
            self.canvas.delete("all")
            self.load_image()

    def undo_move(self):
        if self.undo_stack:
            src_path, target_dir = self.undo_stack.pop()
            shutil.move(os.path.join(target_dir, os.path.basename(src_path)), src_path)
            self.image_files.insert(0, os.path.basename(src_path))
            self.canvas.delete("all")
            self.load_image()


if __name__ == '__main__':
    import argparse

    class_0_foldername = '0'
    class_1_foldername = '1'

    parser = argparse.ArgumentParser(description='Move images between directories based on user input.')
    parser.add_argument('image_dir', help='Path to the directory containing images.')

    args = parser.parse_args()

    class_0_dir = os.path.join(args.image_dir, class_0_foldername)
    class_1_dir = os.path.join(args.image_dir, class_1_foldername)

    app = ImageOrganizer(args.image_dir, class_0_dir, class_1_dir)
    app.mainloop()
