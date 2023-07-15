# 一个监听键盘输入的类
import re
import time

from webcrawler.NovelPassageCrawler import NovelPassageCrawler
from pynput.keyboard import Key, Listener
import os


class KeyboardListener:
    def __init__(self, prev_page_func, next_page_func):
        self.esc_flag = False  # ESC键的标志

        # 上一页和下一页的函数
        self.prev_page_func = prev_page_func
        self.next_page_func = next_page_func

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)  # 创建监听器

    def __enter__(self):
        # 在进入上下文之前执行的操作
        # 初始化键盘监听器等
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 在退出上下文时执行的操作
        # 关闭键盘监听器等
        pass

    def on_press(self, key):
        """
        按键按下的时候执行的函数
        :param key:
        :return:
        """
        # 检测到ESC键输入的时候,终止监听
        if key == Key.esc:
            self.esc_flag = True
            self.listener.stop()

        # 如果检测到上箭头键或者回车输入的时候,则执行上一页的函数
        if key == Key.up or key == Key.enter:
            self.prev_page_func()

        # 如果检测到下箭头键输入的时候,则执行下一页的函数
        if key == Key.down:
            self.next_page_func()

    def on_release(self, key):
        pass

    def start(self):
        """
        开始监听
        :return:
        """
        self.listener.start()  # 开始监听
        self.listener.join()  # 阻塞线程，直到监听器停止

    # 终止监听
    def stop(self):
        """
        停止监听
        :return:
        """
        self.listener.stop()  # 停止监听


if __name__ == '__main__':
    def prev_page():
        print("上一页")


    def next_page():
        print("下一页")


    test = KeyboardListener(prev_page_func=prev_page, next_page_func=next_page)
    test.start()
