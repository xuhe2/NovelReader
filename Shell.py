# 实现小说阅读器的shell界面

from webcrawler.NovelCrawler import NovelCrawler
import csv
import os
import re
from KeyboardListener import KeyboardListener


class Shell:
    def __init__(self):
        # 历史命令记录
        self.command_history = []

        # 阅读方式
        self.read_mode = '-shell'  # 默认为shell模式

        self.books = []  # 书籍列表
        self.last_read_index = []  # 最后阅读的索引
        with open('books.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:  # 如果是空行，則跳过
                    continue

                # 文件的格式是 name, url, from_tag, auto_next_page, last_read_index
                self.books.append(NovelCrawler(name=row[0].strip(), url=row[1].strip(), from_tag=row[2],
                                               auto_next_page=bool(row[3].strip())))  # 书籍
                self.last_read_index.append(int(row[4]))  # 最后阅读的索引

        self.book_url = None  # 当前的书籍的url
        self.book_index = None  # 当前的书籍的下标
        self.book_chapter = 1  # 当前的书籍的章节

    # 展示当前的状态
    def print_head(self):
        """
        打印当前的状态
        :return:
        """
        if self.book_index is None:
            print("[no book]>> ", end='')  # 没有书籍
        else:
            print(f"[reading {self.books[self.book_index].info['name']}]>> ", end='')  # 有书籍

    # 获取阅读进度
    def get_progress(self, book_index):
        """
        获取阅读进度
        :return:
        """
        if self.book_index is None:
            return 0
        else:
            return self.books[book_index].get_read_progress(self.last_read_index[book_index])  # 获取阅读进度

    def _ls(self, command):
        # 返回值元素初始化
        res = []

        # 第一个参数是ls,后面的参数可能是`-book/-b`或者`-chapter/-c`

        # 如果没有参数,则显示所有的书籍
        if len(command) == 1:
            for i in range(len(self.books)):
                # 使用get_progress()方法获取进度
                res.append(
                    f'no.{i}\tname: {self.books[i].name}\tlast_read: {self.last_read_index[i]}\tprogress_rate: {self.get_progress(i)}')
            return res

        # 如果有参数,则显示对应的书籍
        if command[1] == '-book' or command[1] == '-b':
            for i in range(len(self.books)):  # 显示书籍列表
                # 使用get_progress()方法获取进度
                res.append(
                    f'no.{i}\tname: {self.books[i].name}\tlast_read: {self.last_read_index[i]}\tprogress_rate: {self.get_progress(i)}')
            return res

        elif command[1] == '-chapter' or command[1] == '-c':
            # 如果不存在当前的书籍,则显示错误信息
            if self.book_index is None:
                res.append('ls error: no book selected')
                return res

            # 显示当前书本章节列表,下标从1开始
            for i in range(self.books[self.book_index].max_chapter_index):
                # 如果不是当前阅读的章节
                if i + 1 != self.book_chapter:
                    res.append(f'       no.{i + 1}\t{self.books[self.book_index].chapter_info[i][0]}')  # 显示章节名字
                else:
                    res.append(f'now->>[no.{i + 1}\t{self.books[self.book_index].chapter_info[i][0]}]<<-')  # 显示章节名字

            # 显示上一次阅读的章节和进度
            res.append('\n')  # 空行
            res.append(f'last read chapter: 第{self.last_read_index[self.book_index]}章')
            res.append(f'progress rate: {self.get_progress(self.book_index)}%')

            return res

        # 如果参数不对,则显示错误信息
        res.append(f'ls error: no command named {command[1]}')
        return res

    # 获取history命令要显示的内容
    def _history(self):
        return self.command_history  # 返回历史命令记录

    # 获取read命令要显示的内容
    def _read(self, command):
        # 如果不存在选中的书籍,则显示错误信息
        if self.book_index is None:
            print('read error: no book selected')
            return None

        # 第二个参数是阅读方式,有`shell`和`window`两种
        if len(command) <= 1:
            print('read error: no read method')
            return None

        # 获取阅读方式
        if command[1] == '-shell' or command[1] == '-s':
            self.read_method = '-shell'  # 使用shell阅读
        elif command[1] == '-window' or command[1] == '-w':
            self.read_method = '-window'  # 使用window阅读
        else:
            print('read error: read method param error')  # 参数错误
            return None

        # 如果没有参数,则读取last_read_index对应的章节
        if len(command) == 2:
            index = self.last_read_index[self.book_index]
        else:
            # 如果参数不是数字,则显示错误信息
            if not re.match(r'^\d+$', command[2]):
                print('read error: chapter error')
                return None
            index = int(command[2])
            self.book_chapter = index  # 更新book_chapter
            self.last_read_index[self.book_index] = index  # 更新last_read_index

        # 如果章节不存在,则显示错误信息
        if index < 1 or index > self.books[self.book_index].max_chapter_index:
            print('read error: chapter not found')
            return None

        # 读取章节
        return self.books[self.book_index].get_chapter_content_by_index(index - 1, use_filter='break',
                                                                        div_class='Readarea ReadAjax_content')

    # prev_page_func函数实现翻页
    def _prev_page_func(self):
        # 如果不存在选中的书籍,则显示错误信息
        if self.book_index is None:
            print('prev_page error: no book selected')
            return

        # 如果翻到不存在的页面,则显示错误信息
        if self.book_chapter == 1:
            print('prev_page error: no prev page')
            return

        # 翻页
        self.book_chapter -= 1
        self.last_read_index[self.book_index] = self.book_chapter

        # 读取章节
        if self.read_method == '-shell':
            print(self._read(['read', self.read_method, str(self.book_chapter)]))

        # next_page_func函数实现翻页

    def _next_page_func(self):
        # 如果不存在选中的书籍,则显示错误信息
        if self.book_index is None:
            print('next_page error: no book selected')
            return

        # 如果翻到不存在的页面,则显示错误信息
        if self.book_chapter == self.books[self.book_index].max_chapter_index:
            print('next_page error: no next page')
            return

        # 翻页
        self.book_chapter += 1
        self.last_read_index[self.book_index] = self.book_chapter

        # 读取章节
        if self.read_method == '-shell':
            print(self._read(['read', self.read_method, str(self.book_chapter)]))


    # 获取命令,切分命令
    def get_command(self, command):
        """
        获取命令
        :return:
        """
        # 切分命令
        try:
            # 用空格分割,去掉空白内容
            info = command.split(' ')
            info = [i.strip() for i in info if i.strip() != '']

            # 把格式为`"XX`和`XX"`的内容合并
            for i in range(len(info)):
                if re.match(r'^".*', info[i]) and not re.match(r'.*"$', info[i]):
                    info[i] = info[i] + ' ' + info[i + 1]
                    info[i + 1] = ''
            # 把格式为`'XX`和`XX'`的内容合并
            for i in range(len(info)):
                if re.match(r"^'.*", info[i]) and not re.match(r".*'$", info[i]):
                    info[i] = info[i] + ' ' + info[i + 1]
                    info[i + 1] = ''
            # 去除空白内容
            info = [i for i in info if i != '']

            # 去除''和""
            info = [i.strip("'").strip('"') for i in info]
        except Exception as e:
            print('add error:', e)
            return

        return info

    """
    命令函数
    """

    # save命令
    def save(self):
        """
        将当前的书籍信息保存到文件中
        :return:
        """
        try:
            with open('books.csv', 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                for i in range(len(self.books)):
                    writer.writerow(
                        [self.books[i].info['name'], self.books[i].info['url'], self.books[i].info['from_tag'],
                         self.books[i].info['auto_next_page'], self.last_read_index[i]])

        except Exception as e:
            print('save error: ' + e)

    # help命令
    def help(self, command):
        # 第一个参数是`help`,可能存在第二个参数,第二个参数代表要访问的命令

        # 初始化所有的帮助信息
        helps = {
            'help': """
            help [command]
            显示帮助信息,如果有command参数,则显示command的帮助信息
            """,

            'add': """
            add url [-p/-d] [-n/-name name] [-c/-close-auto]
            添加书籍,第一个参数是书籍的URL,第二个参数是书籍的来源,默认是<p>标签,第三个参数是书籍的名字,默认是unknown,第四个参数是是否自动翻页,默认是True
            """,

            'rm': """
            rm index
            删除书籍,第一个参数是书籍的下标(从0开始)
            """,

            'ls': """
            ls [-book/-b] [-chapter/-c]
            显示书籍列表,第一个参数是显示书籍列表,第二个参数是显示章节列表
            """,

            'read': """
            read [-shell/-s]/[-window/-w] [index] 
            读取书籍,第一个参数是书籍章节的下标(从1开始),如果没有参数,则读取上一次阅读的书籍的章节
            使用-shell参数,则使用shell模式,使用-window参数,则使用窗口模式
            """,

            'choose': """
            choose [index]
            选择书籍,第一个参数是书籍的下标(从0开始)
            """,

            'clear': """
            clear
            清屏
            """,

            'history': """
            history
            显示历史命令
            """,

            'exit': """
            exit
            退出程序
            """
        }

        # 如果没有参数,则显示所有的帮助信息
        if len(command) == 1:
            for key in helps:
                print(helps[key])
            return
        else:
            # 如果有参数,则显示对应的帮助信息
            if command[1] in helps:
                print(helps[command[1]])
            else:
                print(f'no command named {command[1]}')

    # add命令
    def add(self, command):
        """
        添加书籍
        :param command:
        :return:
        """

        # 第一个参数是add,第二个参数是URL
        if len(command) < 2:
            print('add error: not enough parameters')
            return
        if not re.match(r'^https?://.*', command[1]):
            print('add error: url error')
            return

        # 初始化
        from_tag = 'p'
        auto_next_page = True
        name = 'unknown'

        for param in command:
            # 来源是<p>标签
            if param == '-p':
                from_tag = 'p'

            # 来源是<div>标签
            if param == '-d' or param == '-div':
                from_tag = 'div'

            # 当`-name/-n`的时候,下一个参数是书籍的名字
            if param == '-n' or param == '-name':
                # 如果下一个参数开头是`-`,说明没有书籍名字
                if command[command.index(param) + 1][0] == '-':
                    continue
                name = command[command.index(param) + 1]

            # 当`-close-auto/-c`的时候,不自动查找下一页的章节
            if param == '-c' or param == '-close-auto':
                auto_next_page = False

        # 加入books
        self.books.append(NovelCrawler(name=name, url=command[1], from_tag=from_tag, auto_next_page=auto_next_page))

        # 加入last_read_index
        self.last_read_index.append(1)

        # 保存
        self.save()

    # 删除书籍
    def rm(self, index):
        """
        删除书籍
        :param index:
        :return:
        """
        # 不在范围内
        if index < 0 or index >= len(self.books):
            print('rm error: index out of range')
            return

        # 删除
        try:
            self.books.pop(index)  # 删除书本
            self.last_read_index.pop(index)  # 删除最近阅读的下标

            # 如果删除的是当前的书籍,则重置当前的书籍
            if self.book_index == index:
                self.book_url = None
                self.book_index = None
                self.book_chapter = 1

        except Exception as e:
            print('rm error:', e)
            return

        # 保存
        self.save()

    # 获取ls命令要显示的书籍列表

    # ls命令
    def ls(self, command):
        # 获取要显示的列表
        res = self._ls(command)

        # 打印列表
        for i in res:
            print(i)

    # clear命令
    def clear(self):
        # 清屏
        os.system('cls')

    # history命令
    def history(self):
        # 打印历史记录
        index = 0
        for i in self.command_history:
            index += 1
            print(f'{index}: {i}')

    # exit命令
    def exit(self):
        # 保存
        self.save()
        # 退出程序具体实现在`run`函数中

    # choose命令
    def choose(self, command):
        """
        选择书籍
        :param command:
        :return:
        """
        # 如果没有参数,则显示错误信息
        if len(command) == 1:
            print('choose error: not enough parameters')
            return

        # 如果有参数,则选择书籍
        try:
            self.book_index = int(command[1])
            self.book_url = self.books[self.book_index].url
            self.book_chapter = self.last_read_index[self.book_index]

        except Exception as e:
            print('choose error:', e)
            return

    # read命令
    def read(self, command):
        # 使用_read函数读取
        print(self._read(command))

        # 使用KeyboardListener监听键盘输入
        with KeyboardListener(prev_page_func=self._prev_page_func, next_page_func=self._next_page_func) as listener:
            tmp = listener
            tmp.start()


if __name__ == '__main__':
    test = Shell()
    data = 'add https://www.tasim.net/book/10967/ -d -n "今天也没变成玩偶呢"'

    data = test.get_command(data)
    # print(data)
    #
    test.add(data)  # 添加书籍
    # print(test.books[0].info)

    test.choose(['choose', '0'])  # 选择书籍

    # test.print_head()
    # my_input = input()
    # test.ls(test.get_command(my_input))  # 显示书籍列表

    # test.clear()  # 清屏
    # test.help(test.get_command(my_input))

    test.read(test.get_command('read -s 1'))  # 读取书籍

    test.rm(0)  # 删除书籍
    print(len(test.books))
