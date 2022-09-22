import tkinter as tk
from PIL import Image, ImageTk

from bisect import bisect_left

import win32gui
import win32con
import win32api

class App():
   def __init__(self):
      self.win = tk.Tk()
      self.canvas = None

      self.TRP_COLOR = '#ffffff'
      self.MODE_COUNT = 3

      self.mode = 1
      self.text_pos = None
      self.image = Image.new('RGB', (260,100), color="#ff0000")
      self.image_frame = tk.Label(self.win)
      self.imaging = None
      self.frame_pos = [0, 0, 0, 0]
      self.frame_rect = None
      self.frame_state = 0
      self.cursor_x, self.cursor_y = None, None
      self.draw_lines = []
      self.slices = {
         'ColumnMisplace': {
            'record': { 'column': [], 'row': [] }
         }
      }
      self.width, self.height = 0, 0
      self.scale = 1
      self.initial()

   def initial(self):
      self.win.configure(bg='white')
      self.win.geometry("1920x460")
      # photo = ImageTk.PhotoImage(file="2.jpg")
      # im = ImageTk.PhotoImage(Image.open("1.jpg"))
      # self.image_frame.config(image=im)
      # self.image_frame.image = im
      self._resize_image('1.jpg')
      self.image_frame.place(x=0, y=0)

      self.canvas = tk.Canvas(self.win, width=1920, height=960, bg=self.TRP_COLOR)
      self.canvas.place(x=0, y=0)

      self._canvas_transparent()
      self._controller_bind()
      self._update_window_attr()
      # self._refresh_image()

   def _resize_image(self, path):
      imaging = Image.open(path)
      self.scale = 1360 / imaging.width
      width_r = int( imaging.width * self.scale )
      height_r = int( imaging.height * self.scale )
      self.imaging = ImageTk.PhotoImage(imaging.resize((width_r, height_r), Image.ANTIALIAS))
      self.image_frame.config(image=self.imaging)
      self.image_frame.image = self.imaging

   def _update_window_attr(self):
      self.width = self.win.winfo_width()
      self.height = self.win.winfo_height()

   def _refresh_cursor(self):      
      self.canvas.delete(self.cursor_x)
      self.canvas.delete(self.cursor_y)
      self.canvas.delete(self.text_pos)

   def _draw_lines(self, e):
      x, y = e.x, e.y
      w, h = self.win.winfo_width(), self.win.winfo_height()
      if self.mode == 1:
         self.draw_lines.append( self.canvas.create_line(x, 0, x, h, width=2, fill="#cc0000") )
         self.slices['ColumnMisplace']['record']['column'].append(x)
         self.slices['ColumnMisplace']['record']['column'].sort()
         print(self.slices['ColumnMisplace']['record'])
      elif self.mode == 2:
         border = bisect_left(self.slices['ColumnMisplace']['record']['column'], x)
         border_left = self.slices['ColumnMisplace']['record']['column'][border-1]
         border_right = self.slices['ColumnMisplace']['record']['column'][border]
         self.draw_lines.append( self.canvas.create_line(border_left, y, border_right, y, width=2, fill="#0000cc") )
      elif self.mode == 3:
         if self.frame_state == 0:
            self.frame_pos[0], self.frame_pos[1] = x, y
         self.frame_state = (self.frame_state + 1) % 3

      # if x == None or x == 0:
         # self.draw_lines.append( self.canvas.create_line(0, y, w, y, width=3, fill="#cc0000") )
      # else:
         # self.draw_lines.append( self.canvas.create_line(x, 0, x, h, width=3, fill="#cc0000") )

   def _remove_lines(self, e):
      if self.mode == 1 or self.mode == 2:
         if self.draw_lines:
            self.canvas.delete(self.draw_lines.pop())
      elif self.mode == 3:
         if self.frame_rect:
            self.canvas.delete(self.frame_rect)
            self.frame_rect = None
            self.frame_state = 0

   def _move_cursor(self, e):
      self._refresh_cursor()
      x, y = e.x, e.y
      px, py = int(e.x / self.scale), int(e.y / self.scale)
      w, h = self.win.winfo_width(), self.win.winfo_height()
      self.text_pos = self.canvas.create_text(x+80, y+10, text="(x={}, y={})".format(px, py))
      if self.mode == 1:
         self.cursor_y = self.canvas.create_line(0, y, w, y, width=1, dash=(3,3))
         self.cursor_x = self.canvas.create_line(x, 0, x, h, width=1)
      elif self.mode == 2:
         border = bisect_left(self.slices['ColumnMisplace']['record']['column'], x)
         border_left = self.slices['ColumnMisplace']['record']['column'][border-1]
         border_right = self.slices['ColumnMisplace']['record']['column'][border]
         self.cursor_y = self.canvas.create_line(border_left, y, border_right, y, width=1)
         # self.cursor_y = self.canvas.create_line(0, y, w, y, width=1)
         self.cursor_x = self.canvas.create_line(x, 0, x, h, width=1, dash=(3,3))
      elif self.mode == 3:
         if self.frame_state == 0:
            self.canvas.itemconfig(self.text_pos, text="设定边框A点(x={}, y={})".format(px, py))
         if self.frame_state == 1:
            self.canvas.itemconfig(self.text_pos, text="设定边框B点(x={}, y={})".format(px, py))
            x1, y1, _, _ = self.frame_pos
            self.canvas.delete(self.frame_rect)
            self.frame_rect = self.canvas.create_rectangle(x1, y1, x, y, width=2, outline="#cc0000")
         # self.text_pos.config(text="??")

   def _test(self, e):
      if e.delta > 0:
         self.mode = (self.mode + 1) % self.MODE_COUNT + 1
      else:
         self.mode = (self.mode - 1) % self.MODE_COUNT + 1
      self._move_cursor(e)
      print(e, e.delta, self.mode)

   def _change_cursor(self, e):
      self.mode = (self.mode + 1) % self.MODE_COUNT + 1
      self._move_cursor(e)
      print(e, e.delta, self.mode)

   def _controller_bind(self):
      self.win.bind('<Motion>', self._move_cursor)
      self.win.bind('<ButtonPress-1>', self._draw_lines)
      self.win.bind('<ButtonPress-2>', self._change_cursor)
      self.win.bind('<ButtonPress-3>', self._remove_lines)
      # self.win.bind('<MouseWheel>', self._test)

   def _canvas_transparent(self):
      hwnd = self.canvas.winfo_id()
      colorkey = win32api.RGB(255,255,255)
      wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
      new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
      win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
      win32gui.SetLayeredWindowAttributes(hwnd,colorkey, 255, win32con.LWA_COLORKEY)

   def _image_slice(self, left, top, right, bottom):
      return self.image.crop(left, top, right, bottom)

   def start(self):
      self.win.mainloop()


app = App()
app.start()


"""

def draw_cross(e):
   global line_x
   global line_y
   global text_pos
   x, y = e.x, e.y
   canvas.delete(line_x)
   canvas.delete(line_y)
   canvas.delete(text_pos)
   # line1 = canvas.create_line(x, 0, x, height, width=1)
   # line2 = canvas.create_line(0, y, width, y, width=1)
   line_x = canvas.create_line(0, y, width, y, width=1, dash=(3,3))
   line_y = canvas.create_line(x, 0, x, height, width=1)
   text_pos = canvas.create_text(x+80, y+10, text="(x={}, y={})".format(x, y))



# Window size


# photo = ImageTk.PhotoImage(file="D:\\0911\\ImageDownloader\\数学\\7ec5e14ae05a6ae93b8d2dabcbcc6c43.jpg")
# photo = ImageTk.PhotoImage(file="2.jpg")
photo = ImageTk.PhotoImage(file="2.jpg")
label = tk.Label(win, image=photo)
# label.pack()
label.place(x=0, y=0)



def sign_cross(e):
   x, y = e.x, e.y
   width, height = win.winfo_width(), win.winfo_height()
   sign = canvas.create_line(0, y, width, y, width=3, fill="#cc0000")


line_x = canvas.create_line(200, 0, 200, 200, width=1)
line_y = canvas.create_line(0, 200, 200, 200, width=1)
text_pos = canvas.create_text(0, 0, text="default")



# transparent

# canvas.old_coords = None


# Bind the left button the mouse.
# win.bind('<ButtonPress-1>', draw_line)


# text = tk.Text(win,height=2,width=30)
# text.pack()

# win.mainloop()

"""

