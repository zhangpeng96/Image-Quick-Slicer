import tkinter as tk
from PIL import Image, ImageTk

class App():
    def __init__(self, root):
        self.win = root
        self.win.configure(bg='white')
        self.win.geometry("1920x460")
        self.image = tk.Label(self.win)
        # self.image.place(x=0, y=0, width=300, height=200)
        self.initial()
        # self.win.mainloop()

    def initial(self):        
        # img = Image.open("2.jpg")
        # photo = ImageTk.PhotoImage(img)
        # photo = ImageTk.PhotoImage(file="2.jpg")
        photo = ImageTk.PhotoImage(Image.open("2.jpg"))
        self.image.config(image=photo)
        self.image.image = photo    # Importance
        # self.image.image = photo
        self.image.place(x=0, y=0, width=300, height=200)
        # img.show()
        # self.image.config(image=photo)
        # image = tk.Label(self.win, image=photo, width=800, height=400)


root = tk.Tk()
app = App(root)
root.mainloop()
