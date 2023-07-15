# 这是我用来处理HTML文件中的passage和别的东西的class

import json

from bs4 import BeautifulSoup as bs


class HTMLParser:
    """
    HTML解析器
    """

    def __init__(self, url=None, tag=None, html=None):
        """
        初始化参数
        :param url:
        :param tag:
        :param html:
        """
        self.url = url
        self.tag = tag
        self.html = html

    def get_title(self, html):
        """
        取得文章標題
        :param html: 網頁原始碼
        :return: 回傳文章標題, 如果出現錯誤, 回傳None
        """
        try:
            if hasattr(html, 'text'):  # 如果html有text屬性
                soup = bs(html.text, 'html.parser')
            else:
                soup = bs(html, 'html.parser')
            title = soup.select_one('title').text  # 取得文章標題
            title = title.strip()  # 去掉空白
        except Exception as e:
            print('get title error: ', e)  # 如果出現錯誤，印出錯誤訊息
            title = None

        return title

    def get_content(self, html):
        """
        取得文章內容
        :param html: 網頁原始碼
        :return: 回傳文章內容, 如果出現錯誤, 回傳None
        """
        try:
            if hasattr(html, 'text'):  # 如果html有text屬性
                soup = bs(html.text, 'html.parser')
            else:
                soup = bs(html, 'html.parser')
            # 先找到div標籤，再找到class為artText clearfix的div標籤
            passages = soup.find('div', class_='artText clearfix').find_all('p')
            result = []  # 建立一個空串列
            for p in passages:
                result.append(p.text)  # 將文章內容加入串列

            # 去掉空白和无意义的字符
            result = [x.strip() for x in result if x.strip() != '']
            # 把串列中的元素用\n連接起來
            result = '\n'.join(result)
        except Exception as e:
            print('get content error: ', e)  # 如果出現錯誤，印出錯誤訊息
            result = None

        return result

    def get_data_dict(self):
        title = self.get_title(self.html)  # 取得文章標題
        content = self.get_content(self.html)  # 取得文章內容
        if title is None or content is None:
            return None  # 如果文章標題或文章內容為None，回傳None

        try:
            # 我的dict格式，包含source(url), tag, title, content
            data_dict = {
                'source': self.url,
                'tag': self.tag,
                'title': title,
                'content': content
            }  # 建立一個字典
        except Exception as e:
            print('get data dict error: ', e)
            data_dict = None

        return data_dict  # 回傳字典

    def get_data_json(self):
        """
        將資料轉換成JSON格式
        :return: 回傳JSON格式的資料
        """
        data_dict = self.get_data_dict()  # 取得字典格式的資料
        if data_dict is None:
            return None  # 如果data_dict為None，回傳None

        try:
            data_json = json.dumps(data_dict, ensure_ascii=False, indent=4)  # 將字典轉換成JSON格式
        except Exception as e:
            print('get data json error: ', e)
            data_json = None

        return data_json  # 回傳JSON格式的資料

    def write_to_file(self, path):
        """
        將資料寫入檔案
        :param path: 檔案路徑
        :return: 当写入成功时，回傳True，否则回傳False
        """
        data_json = self.get_data_json()
        if data_json is None:
            return False  # 如果data_json為None，回傳None

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data_json)  # 將資料寫入檔案
        except Exception as e:
            print('write to file error: ', e)
            return False

        return True  # 回傳True
