from webcrawler.IPManager import IPManager
import requests as req
import re
from bs4 import BeautifulSoup as bs


class HTMLGetter:
    def __init__(self, url=None):
        self.url = self.get_while_url(url)  # 如果網址缺少https，則補上

    def get_while_url(self, url):
        """
        如果網址缺少https，則補上
        :param url:
        :return:
        """
        if url is None:
            return None  # 如果網址是None，則回傳None

        if not re.match('https://.*', url):  # 如果網址缺少https
            url = 'https://' + url

        return url

    def get_main_url(self, html=None, inclue_protocl_identifier=True):
        """
        从url中找到主要的域名
        :param url:
        :return:
        """
        if html is None:  # 如果網頁原始碼是None
            if hasattr(self, 'html'):
                html = self.html  # 取得網頁原始碼
            elif hasattr(self, 'url'):
                html = self.get_html(self.url)  # 取得網頁原始碼
            else:
                return None  # 如果網頁原始碼是None，則回傳None

        if html is None:  # 如果網頁原始碼是None
            return None

        if hasattr(html, 'text'):
            html = html.text  # 如果網頁原始碼是requests的Response物件，則取得網頁原始碼的文字

        # url一般以https://或者http://开头，以/结尾,这个/在返回的时候需要去掉
        # 例如：https://www.baidu.com
        result = re.findall('https?://.*?/', html)  # 找到https://或者http://开头，以/结尾的url
        # 如果找到，則取得第一個,去掉/，否則回傳None
        result =  result[0][:-1] if result else None

        if result and not inclue_protocl_identifier:
            # 去除开头的http://或者https://
            result = re.sub('https?://', '', result)

        if result:
            return result
        else:
            return None

    def _get_html(self, url=None, params=None, endcoding='utf-8', use_proxy=False):
        """
        取得網頁原始碼
        :param url: 網址
        :return: 回傳網頁原始碼
        """
        if url is None:
            url = self.url  # 如果網址是None，則使用初始化的網址
        else:
            url = self.get_while_url(url)  # 如果網址缺少https，則補上

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43"
        }

        try:
            # 执行可能引发异常的代码
            if use_proxy:  # 如果使用代理
                self.ip_manager = IPManager()  # 初始化IP管理器
                html = req.get(url, headers=headers, proxies=self.ip_manager.get_proxies(), params=params)  # 取得網頁原始碼
            else:
                html = req.get(url, headers=headers, params=params)

            # 处理响应数据
        except Exception as e:
            # 捕获任意异常
            print("Error occurred:", e)
            return None  # 返回None或进行其他处理

        if html.status_code == 200:  # 如果狀態碼是200
            html.encoding = endcoding  # 設定編碼
            self.html = html  # 儲存網頁原始碼
            return html
        else:  # 如果狀態碼不是200
            return None  # 回傳None

    def get_html(self, url=None, params=None, endcoding='utf-8', use_proxy=False):
        """
        取得網頁原始碼
        :param url:
        :param params: 网页参数
        :param endcoding: 编码格式
        # :param use_proxy: 是否使用代理(True/False)
        :return: 回傳網頁原始碼
        """
        # 尝试三次
        if url is None:
            url = self.url  # 如果網址是None，則使用初始化的網址

        for i in range(3):
            html = self._get_html(url, params, endcoding, use_proxy)
            if html:
                return html
        return None

    def get_p(self, html=None, div_class=None):
        """
        获取网页代码中的所有的p标签
        :param html: 網頁原始碼, (requests物件,可以不傳入)
        :return: 返回所有的p标签(BeautifulSoup对象, list)
        """
        if html is None and hasattr(self, 'html'):
            html = self.html  # 如果網址是None，則使用初始化的網址

        if html is None and self.url is not None:
            html = self.get_html(url=self.url)  # 如果網址是None，則使用初始化的網址
            self.html = html  # 儲存網頁原始碼

        if html is None:
            return None  # 如果網址是None，則回傳None

        soup = bs(html.text, 'html.parser')  # 創建BeautifulSoup物件

        if div_class:
            p_list = soup.find('div', class_=div_class).find_all('p')  # 取得所有的p標籤
        else:
            p_list = soup.find_all('p')  # 取得所有的p標籤
        return p_list  # 回傳所有的p標籤

    # 获取<div>标签
    def get_div(self, html=None, div_class=None):
        """
        获取网页代码中的所有的div标签
        :param html:
        :param div_class:
        :return:
        """
        if html is None and hasattr(self, 'html'):
            html = self.html  # 如果網址是None，則使用初始化的網址

        if html is None and self.url is not None:
            html = self.get_html(url=self.url)  # 如果網址是None，則使用初始化的網址
            self.html = html  # 儲存網頁原始碼

        if html is None:
            return None  # 如果網址是None，則回傳None

        soup = bs(html.text, 'html.parser')  # 創建BeautifulSoup物件

        if div_class:
            # 找到全部的<div>标签
            div_list = soup.find_all('div', class_=div_class)
        else:
            # 找到全部的<div>标签
            div_list = soup.find_all('div')

        return div_list  # 回傳所有的<div>标签

    def get_passage_content(self, html=None):
        """
        取得文章內容
        :param html:
        :return:
        """
        p_list = self.get_p(html)
        if p_list is None:
            return None

        passage_content = ''  # 儲存文章內容
        for p in p_list:
            # 去除p標籤中的空白
            p_text = p.text.strip()
            # 去除\xa0
            p_text = re.sub('\xa0', '', p_text)
            # 如果存在內容
            if p_text:
                passage_content += p_text + '\n'  # 將內容加入文章內容

        return passage_content


if __name__ == '__main__':
    test = HTMLGetter('https://m.23wxx.com/xs/30316/4368683.html')
    print(test.get_passage_content())
