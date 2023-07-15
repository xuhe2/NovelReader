import tkinter as tk
# 使用多线程
from threading import Thread # 导入线程模块

class ContentDisplayGUI:
    def __init__(self, name='unkown'):
        self.root = tk.Tk()
        self.root.title("小说阅读器")
        self.root.geometry("800x500+100+100")
        # 创建一个菜单栏
        self.menu = tk.Menu(self.root)  # 创建一个菜单栏

        # filemenu = tk.Menu(menu, tearoff=0)  # 创建一个文件菜单
        # filemenu.add_command(label="打开", command=None)
        # filemenu.add_command(label="保存", command=None)
        # menu.add_cascade(label="文件", menu=filemenu)

        # 使用一个二级菜单来设置字体大小
        fontmenu = tk.Menu(self.menu, tearoff=0)
        fontmenu.add_command(label="12", command=lambda: self.change_font_size(12))
        fontmenu.add_command(label="14", command=lambda: self.change_font_size(14))
        fontmenu.add_command(label="16", command=lambda: self.change_font_size(16))
        fontmenu.add_command(label="18", command=lambda: self.change_font_size(18))
        fontmenu.add_command(label="20", command=lambda: self.change_font_size(20))

        # 把这个二级菜单添加到菜单栏
        self.menu.add_cascade(label="字体大小", menu=fontmenu)

        # 创建一个状态栏
        self.status_var = tk.StringVar()  # 创建一个状态栏的变量
        self.status_label = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN,
                                     anchor=tk.W)  # 创建一个状态栏的label
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)  # 把状态栏放在root的底部,并且填充整个root

        self.status_var.set("当前阅读章节: " + name)  # 设置状态栏的内容

        # 创建一个标签栏
        self.column_var = tk.StringVar()
        self.column_label = tk.Label(self.root, textvariable=self.column_var, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                     bg="gray",
                                     width=4)  # 创建一个标签栏的label
        self.column_label.pack(side=tk.LEFT, fill=tk.Y)  # 把标签栏放在root的左边,并且填充整个root

        self.text_pad = tk.Text(self.root, undo=True, font=25, bg='#FFFFCC')  # undo=True,可以撤销, font=25,字体大小为25,背景色为淡黄色
        self.text_pad.pack(expand=True, fill=tk.BOTH)  # expand=True,可以随着窗口的变化而变化, fill=tk.BOTH,可以填充整个窗口

        # 创建一个scroller
        scroller = tk.Scrollbar(self.text_pad, width=20)  # 把scroller添加到text_pad
        self.text_pad.config(yscrollcommand=scroller.set)  # 设置text_pad的yscrollcommand为scroller.set
        scroller.config(command=self.text_pad.yview)  # 设置scroller的command为text_pad.yview
        scroller.pack(side=tk.RIGHT, fill=tk.Y)  # 把scroller放在text_pad的右边,并且填充整个text_pad

        # 把菜单栏添加到root
        self.root.config(menu=self.menu)

    # 设置状态栏的内容
    def set_status(self, status):
        self.status_var.set(status)

    # 设置标签栏的内容
    def set_column(self, column):
        self.column_var.set(column)

    def change_font_size(self, font_size=12):
        """
        改变字体大小
        :param font_size:
        :return:
        """
        self.text_pad.config(font=("Arial", font_size))  # 设置字体大小

    # start the GUI
    def start(self):
        # 新开一个线程来运行GUI
        self.t = Thread(target=self.root.mainloop)
        self.t.start()

    # stop the GUI
    def stop(self):
        self.root.quit()

    def insert_text(self, text):
        """
        在文本框中插入文本
        :param text:
        :return:
        """
        self.text_pad.insert(tk.INSERT, text)

    def clear_text(self):
        """
        清空文本框
        :return:
        """
        self.text_pad.delete(1.0, tk.END)

if __name__ == '__main__':
    from KeyboardListener import KeyboardListener

    gui = ContentDisplayGUI()

    listener = KeyboardListener(prev_page_func=gui.start, next_page_func=gui.insert_text('xuhe'))
    listener.start()
