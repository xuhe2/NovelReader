# 使用组合模式，将小说的索引页和章节页的爬虫组合起来

from webcrawler.NovelPassageCrawler import NovelPassageCrawler
from webcrawler.NovelIndexCrawler import NovelIndexCrawler


class NovelCrawler:
    def __init__(self, url, name='unknown', from_tag='p', auto_next_page=True):
        self.indexCrawler = NovelIndexCrawler(url=url)
        self.passageCrawler = NovelPassageCrawler(url=url)

        # 设置auto_next_page
        self.auto_next_page = auto_next_page

        # 设置url
        self.url = url

        # 获取mian_url
        self.main_url = self.indexCrawler.get_main_url(url)

        # 设置小说名字
        self.name = name

        # 设置小说的来源标签
        self.from_tag = from_tag

        # 获取小说的章节信息
        self.chapter_info = self.indexCrawler.get_all_chapter_infor(
            get_name_func=self.indexCrawler._get_chapter_name_from_a,
            get_url_func=self.indexCrawler._get_chapter_url_from_a,
            auto_next_page=auto_next_page)

        # 获取最大的章节索引
        self.max_chapter_index = len(self.chapter_info)

    # 获取小说的章节内容
    def get_chapter_content_by_index(self, index, use_filter=None, div_class=None, user_tab_separator='\u3000'):
        """
        根据章节的索引获取章节的内容
        :param index: 下标从0开始
        :return:
        """
        if index < 0 or index >= self.max_chapter_index:  # 如果超出限制，則返回None
            return None

        url = self.chapter_info[index][1]  # 获取章节的url
        html = self.passageCrawler.get_html(url)

        if html is None:  # 如果html是None，則返回None
            return None

        if self.from_tag == 'p':
            return self.passageCrawler.get_passage_content_from_p(html=html, use_filter=use_filter, div_class=div_class)
        else:
            return self.passageCrawler.get_passage_content_from_div(html=html, use_filter=use_filter,
                                                                    div_class=div_class,
                                                                    use_tab_separator=user_tab_separator)

    # 获取这个类的主要信息
    @property
    def info(self):
        return {
            'name': self.name,
            'url': self.url,
            'main_url': self.main_url,
            'from_tag': self.from_tag,
            'auto_next_page': self.auto_next_page,
            'max_chapter_index': self.max_chapter_index,
            'chapter_info': self.chapter_info
        }

    # 获取阅读进度
    def get_read_progress(self, index):
        """
        获取阅读进度
        :param index: 章节的索引
        :return: 进度
        """
        # 如果超出限制，則返回None
        if index < 1 or index > self.max_chapter_index:
            return None

        # 保留两位小数
        return round(index / self.max_chapter_index, 2) * 100


if __name__ == '__main__':
    test = NovelCrawler('https://www.tasim.net/book/104311/', from_tag='div')
    print(test.chapter_info)

    print(test.get_chapter_content_by_index(1, use_filter='break', div_class='Readarea ReadAjax_content'))

    print(test.info)

    print(test.indexCrawler.main_url)
