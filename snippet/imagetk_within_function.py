import tkinter as tk
from PIL import Image, ImageTk


win = tk.Tk()

win.configure(bg='white')
win.geometry("1920x460")
img = Image.open("1.jpg")  
photo = ImageTk.PhotoImage(img)
# photo = ImageTk.PhotoImage(file="2.jpg")
image = tk.Label(win, image=photo, width=800, height=400)
image.place(x=0, y=0)


win.mainloop()
