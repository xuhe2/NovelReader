from webcrawler.HTMLGetter import HTMLGetter
import re
from bs4 import BeautifulSoup as bs
import requests as req


class NovelPassageCrawler(HTMLGetter):
    def __init__(self, url=None):
        super().__init__(url)

    def __getattr__(self, item):
        return None  # 如果沒有該屬性，則回傳None

    # 检查处理文章中段落的方法
    def _process_passage(self, url, passage, use_filter=None):
        """
        检查处理文章中段落的方法
        :param url:
        :param passage:
        :param use_filter:
        :return:
        """
        # 屏蔽存在主要URL的p標籤
        keyword_filter = None  # 作为关键词的过滤器
        if use_filter is not None and url is not None:
            keyword_filter = self.get_main_url(url, inclue_protocl_identifier=False)  # 作为关键词的过滤器

        # 如果存在主要URL
        if keyword_filter is not None and keyword_filter in passage:
            if use_filter == 'continue':
                return None
            elif use_filter == 'break':
                return None
            elif use_filter == 'replace':
                passage = passage.replace(keyword_filter, '')
                # 如果替换之后,是空字符串,则返回None
                if passage == '':
                    return None

        return passage

    def get_passage_content_from_p(self, html=None, use_filter=None, url=None, div_class=None):
        """
        取得文章內容
        :param html:
        :param use_filter: 对过滤进行的操作(continue/break/replace)
        :param url:
        :return:
        """
        p_list = self.get_p(html, div_class=div_class)
        if p_list is None:
            return None

        if url is None:  # 如果網址是None，則使用初始化的網址
            url = self.url

        passage_content = ''  # 儲存文章內容
        for p in p_list:
            # 去除p標籤中的空白
            p_text = p.text.strip()
            # 去除\xa0
            p_text = re.sub('\xa0', '', p_text)
            # 如果存在內容
            if p_text:
                p_text = self._process_passage(url, p_text, use_filter=use_filter)
                if p_text is not None:
                    passage_content += p_text + '\n'
                    continue

                # 返回的是None，进行操作
                if use_filter == 'continue':  # 如果是continue，則跳过
                    continue
                elif use_filter == 'break':  # 如果是break，則跳出
                    break

                passage_content += p_text + '\n'

        return passage_content

    # 从<div>中获取文章的内容
    def get_passage_content_from_div(self, html=None, use_filter=None, url=None, div_class=None,
                                     use_tab_separator=None):
        """
        从<div>中获取文章的内容
        :param html:
        :param use_filter:
        :param url:
        :param div_class:
        :param use_tab_separator: 使用什么分割
        :return:
        """
        # 获取<div>标签
        try:
            div_list = self.get_div(html, div_class=div_class)
        except Exception as e:
            print(e)
            return None

        if div_list is None:
            return None

        if url is None:  # 如果網址是None，則使用初始化的網址
            url = self.url

        div_text_list = []
        for div in div_list:
            # 去除p標籤中的空白
            div_text = div.text.strip()
            # 去除\xa0
            div_text = re.sub('\xa0', '', div_text)
            # 如果不存在內容
            if not div_text:
                continue

            if use_tab_separator:  # 如果使用制表符分割
                div_text = div_text.split(use_tab_separator)  # 使用制表符分割
                # 去除空字符串
                div_text = [text for text in div_text if text != '']
            # 如果存在內容,加入列表,注意list和str的區別

            if div_text:  # 如果存在內容
                if use_tab_separator:  # 如果使用制表符分割
                    div_text_list.extend(div_text)
                else:
                    div_text_list.append(div_text)

        passage_content = ''  # 儲存文章內容
        for div_text in div_text_list:
            div_text = self._process_passage(url, div_text, use_filter=use_filter)
            if div_text is not None:
                passage_content += div_text + '\n'
                continue

            # 返回的是None，进行操作
            if use_filter == 'continue':  # 如果是continue，則跳过
                continue
            elif use_filter == 'break':  # 如果是break，則跳出
                break

        return passage_content

    def get_passage_title(self, html=None):
        if html is None and hasattr(self, 'html'):
            html = self.html  # 如果網址是None，則使用初始化的網址

        if html is None and self.url is not None:
            html = self.get_html(url=self.url)  # 如果網址是None，則使用初始化的網址
            self.html = html  # 儲存網頁原始碼

        if html is None:
            return None  # 如果網址是None，則回傳None

        soup = bs(html.text, 'html.parser')  # 創建BeautifulSoup物件
        try:
            # 从head的title标签中获取标题
            title = soup.head.title.text

            # 去除標題中的空白
            title = title.strip()
            # 去除\xa0
            title = re.sub('\xa0', '', title)

        except:
            title = None

        return title  # 回傳標題


if __name__ == '__main__':
    # test = NovelPassageCrawler('https://m.23wxx.com/xs/30316/4368683.html')
    # print(test.get_passage_content_from_p(use_filter='break', div_class='content'))
    #
    test = NovelPassageCrawler('https://www.tasim.net/book/10967/195.html')
    print(test.get_passage_content_from_div(use_filter='break', div_class='Readarea ReadAjax_content',
                                            use_tab_separator='\u3000'))
