# Import the library
import tkinter as tk
from PIL import Image, ImageTk


import win32gui
import win32con
import win32api

# Create an instance of tkinter
win = tk.Tk()

win.configure(bg='yellow')

# Window size
win.geometry("1920x960")


# photo = ImageTk.PhotoImage(file="D:\\0911\\ImageDownloader\\数学\\7ec5e14ae05a6ae93b8d2dabcbcc6c43.jpg")
# photo = ImageTk.PhotoImage(file="2.jpg")
photo = ImageTk.PhotoImage(file="2.jpg")
label = tk.Label(win, image=photo)
# label.pack()
label.place(x=0, y=0)


# Method to draw line between two consecutive points
def draw_line(e):
   x, y = e.x, e.y
   if canvas.old_coords:
      x1, y1 = canvas.old_coords
      canvas.create_line(x, y, x1, y1, width=5)
   canvas.old_coords= x, y

def draw_cross(e):
   global line_x
   global line_y
   global text_pos
   x, y = e.x, e.y
   width, height = win.winfo_width(), win.winfo_height()
   canvas.delete(line_x)
   canvas.delete(line_y)
   canvas.delete(text_pos)
   # line1 = canvas.create_line(x, 0, x, height, width=1)
   # line2 = canvas.create_line(0, y, width, y, width=1)
   line_x = canvas.create_line(0, y, width, y, width=1, dash=(3,3))
   line_y = canvas.create_line(x, 0, x, height, width=1)
   text_pos = canvas.create_text(x+80, y+10, text="(x={}, y={})".format(x, y))

def sign_cross(e):
   x, y = e.x, e.y
   width, height = win.winfo_width(), win.winfo_height()
   sign = canvas.create_line(0, y, width, y, width=3, fill="#cc0000")



# TRANSCOLOUR = 'gray'
# win.wm_attributes('-transparentcolor', TRANSCOLOUR)

canvas = tk.Canvas(win, width=1920, height=960, bg='#ffffff')

line_x = canvas.create_line(200, 0, 200, 200, width=1)
line_y = canvas.create_line(0, 200, 200, 200, width=1)
text_pos = canvas.create_text(0, 0, text="default")

# transparent
hwnd = canvas.winfo_id()
colorkey = win32api.RGB(255,255,255)
wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_exstyle)
win32gui.SetLayeredWindowAttributes(hwnd,colorkey,255,win32con.LWA_COLORKEY)

canvas.pack()
canvas.place(x=0, y=0)
# canvas.old_coords = None


# Bind the left button the mouse.
# win.bind('<ButtonPress-1>', draw_line)

win.bind("<Motion>", draw_cross)
win.bind('<ButtonPress-1>', sign_cross)

# text = tk.Text(win,height=2,width=30)
# text.pack()

win.mainloop()