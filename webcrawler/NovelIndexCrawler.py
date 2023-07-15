from webcrawler.HTMLGetter import HTMLGetter
from bs4 import BeautifulSoup as bs
import re


class NovelIndexCrawler(HTMLGetter):
    def __init__(self, url):
        """
        小说目录页的爬虫
        :param url: 小说目录页的链接(necessary)
        """
        self.url = url  # 小说目录页的链接
        self.main_url = self.get_main_url(url)  # 取得主要的域名
        self.html = self.get_html(url)  # 取得網頁原始碼
        self.next_page_url = None  # 下一页的链接

    def get_while_url(self, url):
        if url is None:
            return None  # 如果url是None，则返回None

        # 当URL缺少main_url时，自动添加主链接
        if not self.main_url in url:  # 如果主链接不在url中
            # 如果url的第一个字符不是/,则在url前面添加/
            if url[0] != '/':
                url = '/' + url

            url = self.main_url + url  # 将主链接添加到url中

        # 如果使用'//'作为开头，则将'//'替换为'https://'
        if url[:2] == '//':
            url = 'https:' + url  # 将'//'替换为'https://'

        # 当URL不是用'https://'开头时，自动添加'https://'开头
        if url[:8] != 'https://':
            url = 'https://' + url

        return url

    # 从<a>标签中获取下一页的链接
    def get_next_page_url_from_a(self, html=None, a_text='下一页'):
        """
        从<a>标签中获取下一页的链接
        :param html: 网页原始码
        :return: 下一页的链接
        """
        if html is None:  # 如果html是None，则获取html
            html = self.html

        if html is None:  # 如果html是None，则返回None
            return None

        try:
            # 获取下一页的链接，下一页的链接在text是`下一页`的a标签中
            soup = bs(html.text, 'lxml')
            next_page_url = soup.find('a', string=a_text).get('href')
            # 补全链接
            next_page_url = self.get_while_url(next_page_url)
        # 捕获任意异常
        except Exception as e:
            next_page_url = None

        return next_page_url  # 返回下一页的链接

    # 从<a>中获取每个章节的链接,可能在<ul>标签中找<a>
    def _get_chapter_url_from_a(self, html=None, ul_class=None):
        """
        从<a>中获取每个章节的链接
        :param html: 网页原始码
        :return: 每个章节的链接
        """
        if html is None:  # 如果html是None，则获取html
            html = self.html

        if html is None:  # 如果html是None，则返回None
            return None

        # 如果ul_class不是None，则使用ul_class
        if ul_class is not None:
            try:
                # 找所有的<a>标签,它的text是章节名,格式是`第一章 章节名`
                soup = bs(html.text, 'lxml')
                a_list = soup.find('ul', class_=ul_class).find_all('a')
                # 使用正则表达式匹配章节名
                chapter_url_list = [self.get_while_url(a.get('href')) for a in a_list if
                                    re.match(r'^第.+章.*', a.text)]
            # 捕获任意异常
            except Exception as e:
                chapter_url_list = None

        # 如果ul_class是None，则找到全部的<a>标签
        try:
            # 找到全部的<a>标签
            soup = bs(html.text, 'lxml')
            a_list = soup.find_all('a')
            # 使用正则表达式匹配章节名
            chapter_url_list = [self.get_while_url(a.get('href')) for a in a_list if re.match(r'^第.+章.*', a.text)]
        # 捕获任意异常
        except Exception as e:
            print(e)
            chapter_url_list = None

        return chapter_url_list  # 返回每个章节的链接

    # 获取每个章节的名字,可能在<ul>标签中找<a>
    def _get_chapter_name_from_a(self, html=None, ul_class=None):
        """
        获取每个章节的名字
        :param html:
        :param ul_class:
        :return:
        """
        if html is None:  # 如果html是None，则获取html
            html = self.html

        if html is None:  # 如果html是None，则返回None
            return None

        # 如果ul_class不是None，则使用ul_class
        if ul_class is not None:
            try:
                # 找所有的<a>标签,它的text是章节名,格式是`第一章 章节名`
                soup = bs(html.text, 'lxml')
                a_list = soup.find('ul', class_=ul_class).find_all('a')
                # 使用正则表达式匹配章节名
                chapter_name_list = [a.text for a in a_list if re.match(r'^第.+章.*', a.text)]
            # 捕获任意异常
            except Exception as e:
                print(e)
                chapter_name_list = None

        # 如果ul_class是None，则找到全部的<a>标签
        try:
            # 找到全部的<a>标签
            soup = bs(html.text, 'lxml')
            a_list = soup.find_all('a')
            # 使用正则表达式匹配章节名,格式是`第一章 章节名`,不符合的不要
            chapter_name_list = [a.text for a in a_list if re.match(r'^第.+章.*', a.text)]

        # 捕获任意异常
        except Exception as e:
            print(e)
            chapter_name_list = None

        return chapter_name_list  # 返回每个章节的名字

    # 当一个页面中的章节个数不足时，使用这个函数获取下一页的链接
    # 直到返回的下一页的链接为None
    def get_next_page_url_list_from_a_until_none(self, html=None, a_text='下一页'):
        """
        当一个页面中的章节个数不足时，使用这个函数获取下一页的链接
        :param html: 网页原始码
        :return: 下一页的链接(列表)
        """
        if html is None:  # 如果html是None，则获取html
            html = self.html

        if html is None:  # 如果html是None，则返回None
            return None

        next_page_url_list = [self.url]  # 下一页的链接列表

        try:
            # 不断获取下一页的链接，直到返回的下一页的链接为None
            while True:
                next_page_url = self.get_next_page_url_from_a(html, a_text)
                if next_page_url is None:
                    break
                next_page_url_list.append(next_page_url)
                html = self.get_html(next_page_url)
        # 捕获任意异常
        except Exception as e:
            next_page_url_list = None

        return next_page_url_list  # 返回下一页的链接列表

    # 获取全部章节的URL,使用auto_next_page标记是否自动获取下一页的链接
    def get_all_chapter_url_from_a(self, html=None, auto_next_page=True, a_text='下一页', ul_class=None):
        """
        获取全部章节的URL,使用auto_next_page标记是否自动获取下一页的链接
        :param html:
        :param auto_next_page: 是否自动获取下一页的链接
        :param a_text:
        :param ul_class:
        :return:
        """
        if html is None:  # 如果html是None，则获取html
            html = self.html

        if html is None:  # 如果html是None，则返回None
            return None

        page_list = []  # 页面的URL
        # 获取需要爬取的页面的URL
        try:
            # 如果auto_next_page是True，则获取全部的下一页的链接
            if auto_next_page:
                page_list = self.get_next_page_url_list_from_a_until_none(html, a_text)  # 获取全部的下一页的链接
            else:
                page_list.append(self.url)  # 将当前页的链接添加到列表中
        # 捕获任意异常
        except Exception as e:
            print(e)  # 打印异常
            page_list = None

        if page_list is None:
            return None

        chapter_url_list = []  # 全部章节的URL列表
        # 获取全部章节的URL
        try:
            # 遍历每个页面的URL
            for page_url in page_list:
                # 获取当前页面的全部章节的URL
                chapter_url_list.extend(self._get_chapter_url_from_a(self.get_html(page_url), ul_class))
        # 捕获任意异常
        except Exception as e:
            print(e)
            chapter_url_list = None

        return chapter_url_list  # 返回全部章节的URL列表

    # 获取全部章节的name和URL,使用auto_next_page标记是否自动获取下一页的链接
    def get_all_chapter_infor(self, get_name_func=None, get_url_func=None, html=None, auto_next_page=True,
                              a_text='下一页',
                              ul_class=None):
        """
        获取全部章节的name和URL,使用auto_next_page标记是否自动获取下一页的链接
        :param html:
        :param auto_next_page: 是否自动获取下一页的链接
        :param a_text:
        :param ul_class:
        :return: 返回的是[(name,url),()]的形式
        """
        # 初始化两个函数
        get_name_func = self._get_chapter_name_from_a if get_name_func is None else get_name_func
        get_url_func = self._get_chapter_url_from_a if get_url_func is None else get_url_func

        if html is None:  # 如果html是None，则获取html
            html = self.html

        if html is None:  # 如果html是None，则返回None
            return None

        page_list = []  # 页面的URL
        # 获取需要爬取的页面的URL
        try:
            # 如果auto_next_page是True，则获取全部的下一页的链接
            if auto_next_page:
                page_list = self.get_next_page_url_list_from_a_until_none(html, a_text)  # 获取全部的下一页的链接
            else:
                page_list.append(self.url)  # 将当前页的链接添加到列表中
        # 捕获任意异常
        except Exception as e:
            print(e)  # 打印异常
            page_list = None

        if page_list is None:
            return None

        chapter_infor_list = []  # 全部章节的URL列表
        # 获取全部章节的name和URL
        try:
            # 遍历每个页面的URL
            for page_url in page_list:
                html = self.get_html(page_url)
                # 获取当前页面的全部章节的name
                name_list = get_name_func(html, ul_class=ul_class)
                # 获取当前页面的全部章节的URL
                url_list = get_url_func(html, ul_class=ul_class)
                # 将当前页面的全部章节的name和URL添加到列表中
                chapter_infor_list.extend(zip(name_list, url_list))
        # 捕获任意异常
        except Exception as e:
            print(e)
            chapter_infor_list = None

        return chapter_infor_list  # 返回全部章节的URL列表


if __name__ == '__main__':
    test = NovelIndexCrawler('https://www.tasim.net/book/10967/')
    # test = NovelIndexCrawler('https://m.23wxx.com/xs/30316_1/')
    # print(test.get_next_page_url_from_a(a_text='下一页'))
    # print(test._get_chapter_url_from_a(ul_class='read'))
    # print(test.get_next_page_url_list_from_a_until_none())

    # name_list = test._get_chapter_name_from_a()
    # url_list = test._get_chapter_url_from_a()
    # for name, url in zip(name_list, url_list):
    #     print(name, url)

    print(test.main_url)
    data = test.get_all_chapter_infor(get_name_func=test._get_chapter_name_from_a,
                                     get_url_func=test._get_chapter_url_from_a, auto_next_page=True)

    info = ''
    for name, url in data:
        info += name + '\t' + url + '\n'

    import tkinter as tk
    from tkinter import messagebox


    def show_data_popup(data):
        popup = tk.Toplevel()
        popup.title("Data Popup")

        # 创建一个Label来展示数据
        label = tk.Label(popup, text=data)
        label.pack(padx=20, pady=20)

        # 创建一个按钮，关闭弹窗
        button = tk.Button(popup, text="关闭", command=popup.destroy)
        button.pack(pady=10)


    # 示例数据
    data = info

    # 创建主窗口
    root = tk.Tk()

    # 创建按钮，点击按钮时展示数据弹窗
    button = tk.Button(root, text="展示数据", command=lambda: show_data_popup(data))
    button.pack(pady=20)

    root.mainloop()

