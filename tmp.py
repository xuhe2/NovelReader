# 这是一个学习tkinter的文件

# no.1

# import tkinter as tk
# from tkinter import messagebox
#
# root = tk.Tk()
# root.geometry("800x600")
# root.title("小说阅读器")
#
# # 起始frame
# frame_start = tk.Frame(root)  # 创建Frame
# frame_start.pack()  # 将Frame添加到主窗口
#
# # 布置一个label,和别的控件存在间隔
# tk.Label(frame_start, text="欢迎使用小说阅读器", font=("Arial", 20)).pack(padx=30, pady=30)
#
# # # 把label放在左上角
# # tk.Label(frame_start, text="欢迎使用小说阅读器", font=("Arial", 20)).pack(side="top", anchor="nw")
#
# # 设置按钮
# # btn_start = tk.Button(frame_start, text="开始阅读", font=("Arial", 20))
# # btn_start.pack(side="top", anchor="nw")
#
# # 设置按钮,放在frame的底部
# btn_start = tk.Button(frame_start, text="开始阅读", font=("Arial", 20))
# btn_start.pack(side="bottom", anchor="se")
#
# # 设置退出按钮,放在root的底部
# btn_exit = tk.Button(root, text="退出", font=("Arial", 20), command=root.quit)
# btn_exit.pack(side="bottom", anchor="se")
#
# frame_start.pack_forget()  # 隐藏frame_start
#
# root.mainloop()  # 进入消息循环

# no.2 笔记本

# import tkinter as tk
#
# root = tk.Tk()
# root.title("小说阅读器")
# root.geometry("800x500+100+100")
#
# # 创建一个菜单栏
# menu = tk.Menu(root)  # 创建一个菜单栏
# filemenu = tk.Menu(menu, tearoff=0)  # 创建一个文件菜单
# filemenu.add_command(label="打开", command=None)
# filemenu.add_command(label="保存", command=None)
# menu.add_cascade(label="文件", menu=filemenu)
#
# # 创建一个状态栏
# status_var = tk.StringVar()  # 创建一个状态栏的变量
# status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)  # 创建一个状态栏的label
# status_label.pack(side=tk.BOTTOM, fill=tk.X)  # 把状态栏放在root的底部,并且填充整个root
#
# status_var.set("欢迎使用小说阅读器")  # 设置状态栏的内容
#
# # 创建一个标签栏
# column_var = tk.StringVar()
# column_label = tk.Label(root, textvariable=column_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="gray",
#                         width=8)  # 创建一个标签栏的label
# column_label.pack(side=tk.LEFT, fill=tk.Y)  # 把标签栏放在root的左边,并且填充整个root
#
# column_var.set("第一列")  # 设置标签栏的内容
#
# text_pad = tk.Text(root, undo=True, font=25, bg='#FFFFCC')  # undo=True,可以撤销, font=25,字体大小为25,背景色为淡黄色
# text_pad.pack(expand=True, fill=tk.BOTH)  # expand=True,可以随着窗口的变化而变化, fill=tk.BOTH,可以填充整个窗口
#
#
# def change_font_size(font_size=12):
#     """
#     改变字体大小
#     :param font_size:
#     :return:
#     """
#     text_pad.config(font=("Arial", font_size))  # 设置字体大小
#
#
# # 使用一个二级菜单来设置字体大小
# fontmenu = tk.Menu(menu, tearoff=0)
# fontmenu.add_command(label="12", command=lambda: change_font_size(12))
# fontmenu.add_command(label="14", command=lambda: change_font_size(14))
# fontmenu.add_command(label="16", command=lambda: change_font_size(16))
# fontmenu.add_command(label="18", command=lambda: change_font_size(18))
# fontmenu.add_command(label="20", command=lambda: change_font_size(20))
#
# # 把这个二级菜单添加到菜单栏
# menu.add_cascade(label="字体大小", menu=fontmenu)
#
# # 创建一个scroller
# scroller = tk.Scrollbar(text_pad, width=20)  # 把scroller添加到text_pad
# text_pad.config(yscrollcommand=scroller.set)  # 设置text_pad的yscrollcommand为scroller.set
# scroller.config(command=text_pad.yview)  # 设置scroller的command为text_pad.yview
# scroller.pack(side=tk.RIGHT, fill=tk.Y)  # 把scroller放在text_pad的右边,并且填充整个text_pad
#
# # 把菜单栏添加到root
# root.config(menu=menu)
#
# root.mainloop()


# no.3 entry 和 text 练习

# import tkinter as tk
#
# root = tk.Tk()
# root.title("小说阅读器")
# root.geometry("800x500+100+100")
#
# entry = tk.Entry(root, font=("Arial", 20))  # 创建一个entry
# # entry = tk.Entry(root, font=("Arial", 20),show="*")  # show="*" 代表输入的内容用*代替
# entry.pack()
#
# text = tk.Text(root, font=("Arial", 20), height=5, bg='#FFFFCC', bd=1)  # 创建一个text, height=5,高度为5行
# text.pack()
#
#
# def insert_point():
#     """
#     在光标处插入内容
#     :return:
#     """
#     var = entry.get()  # 获取entry的内容
#     text.insert("insert", var)  # 在光标处插入内容
#
#
# def insert_end():
#     """
#     在最后插入内容
#     :return:
#     """
#     var = entry.get()  # 获取entry的内容
#     text.insert("end", var)  # 在最后插入内容
#
#
# def delete():
#     """
#     删除内容
#     :return:
#     """
#     text.delete(1.0, "end")  # 删除从第一行第0列到最后一行最后一列的内容
#
#
# # 创建一个按钮,点击按钮,在光标处插入内容
# btn_insert_point = tk.Button(root, text="在光标处插入内容", font=("Arial", 20),
#                              command=insert_point)  # command=insert_point,点击按钮,执行insert_point函数
# btn_insert_point.pack()
#
# root.mainloop()

def move_cursor_up(passage):
    """
    光标上移动n行
    :param n:
    :return:
    """
    # 找到`\n`的个数
    n = passage.count('\n')
    # 光标上移动n行
    print(f'\x1b[{n}A')


passage = """
    1. 你好
    2. 你好
"""

print("\x1b[10;1H")  # 光标移动到第10行,第20列
