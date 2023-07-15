class UrlManager:
    """
    url管理器
    """

    def __init__(self, processed_url_set=set(), unprocessed_url_set=set()):
        """
        初始化url管理器
        :param process_url_set: 已经处理过了的url集合
        """
        self._NewUrl = unprocessed_url_set  # 新url集合
        self._OldUrl = processed_url_set  # 旧url集合

    def has_new_url(self):
        """
        判断是否有新的url
        """
        return len(self._NewUrl) != 0

    def add_new_url(self, url):
        """
        获取新的url
        :param url:
        :return: None or url
        """
        if url == None or len(url) == 0:  # 如果url为空或者长度为0，返回None
            return None
        if url in self._NewUrl or url in self._OldUrl:  # 如果url在新旧url集合中，返回None
            return None
        self._NewUrl.add(url)  # 如果url不在新旧url集合中，将url添加到新url集合中
        return url

    def add_new_urls(self, urls):
        """
        将新的url添加到新url集合中
        :param urls:
        :return:
        """
        if urls == None or len(urls) == 0:
            return None
        for url in urls:
            self.add_new_url(url)  # 将urls中的url添加到新url集合中

    def get_new_url(self):
        """
        获取新的url
        :return: url or None
        """
        if self.has_new_url():
            url = self._NewUrl.pop()
            self._OldUrl.add(url)
            return url  # 如果有新的url，返回url
        else:
            return None  # 如果没有新的url，返回None

    def get_unprocessed_url_set(self):
        """
        获取未处理的url集合
        :return: url集合
        """
        return self._NewUrl


if __name__ == '__main__':
    pre = set()
    pre.add('http://www.baidu.com')
    unprocessed_url_set = set()
    unprocessed_url_set.add('http://www.roxylib.com')
    test = UrlManager(processed_url_set=pre, unprocessed_url_set=unprocessed_url_set)
    test.add_new_url('http://www.baidu.com')
    # st.add_new_url('http://www.roxylib.com')

    print(test.get_unprocessed_url_set())
