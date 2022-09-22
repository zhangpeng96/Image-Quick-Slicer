import tkinter as tk  
import tkinter.filedialog
from PIL import Image,ImageTk 
#选择并显示图片
def choosepic():
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    print(path)
    img_open = Image.open(entry.get())
    #img = ImageTk.PhotoImage(img_open.resize((200,200)))
    img = ImageTk.PhotoImage(img_open)
    lableShowImage.config(image=img)
    lableShowImage.image = img 
if __name__ == '__main__':
    #生成tk界面 app即主窗口
    app = tk.Tk()  
    #修改窗口titile
    app.title("显示图片")  
    #设置主窗口的大小和位置
    app.geometry("800x400+200+200")
    #Entry widget which allows displaying simple text.
    path = tk.StringVar()
    entry = tk.Entry(app, state='readonly', text=path,width = 100)
    entry.pack()
    #使用Label显示图片
    lableShowImage = tk.Label(app)
    lableShowImage.pack()
    #选择图片的按钮
    buttonSelImage = tk.Button(app, text='选择图片', command=choosepic)
    buttonSelImage.pack()
    #buttonSelImage.pack(side=tk.BOTTOM)
    #Call the mainloop of Tk.
    app.mainloop()
