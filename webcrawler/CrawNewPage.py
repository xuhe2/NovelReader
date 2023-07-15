from webcrawler.UrlManager import UrlManager
import requests as req
from bs4 import BeautifulSoup as bs
import re


class CrawNewPage(object):
    """
    This class is used to craw a new page
    """

    def __init__(self, RootUrl, FileName, Pattern):  # RootUrl is the url of the root page
        """
        :param RootUrl: the url of the root page
        :param RootUrl: the url of the root page
        :param FileName: the name of the file that you want to save the data
        :param Pattern: the pattern of the url that you want to craw
        """
        if RootUrl is None or len(RootUrl) == 0:  # if url is empty
            print("Url is wrong")
            return
        self._Urls = UrlManager()
        self._Urls.add_new_url(RootUrl)
        self._Pattern = Pattern

        if FileName is None or len(FileName) == 0:  # if file name is empty
            print("File name is wrong")
            return
        self._File = open(FileName, "w", encoding="utf-8")

    def __del__(self):  # when the object is deleted
        """
        close the file
        :return:
        """
        self._File.close()

    def _get_new_url(self, MyUrl, MySoup):
        """
        get the new url
        :param MyUrl: the url of the page
        :param MySoup: the soup of the page
        :return: None
        """
        if MyUrl is None or len(MyUrl) == 0:  # if url is empty
            return
        if MySoup is None:  # if soup is empty
            return

        links = MySoup.find_all("a", href=True)  # find all the links
        for link in links:
            MyRef = link["href"]
            if re.match(self._Pattern, MyRef):  # if the url matches the pattern
                self._Urls.add_new_url(MyRef)

    def func(self):
        while self._Urls.has_new_url():  # if there is a new url
            MyUrl = self._Urls.get_url()  # get the url
            MyData = req.get(MyUrl, timeout=5)

            if MyData.status_code != 200:  # 200 means success
                print("Error!")  # 404 means not found
                continue

            MySoup = bs(MyData.text, "html.parser")
            if MySoup is None:  # if soup is empty
                print("Soup is empty")
                continue

            MyTitle = MySoup.title.getText()
            if MyTitle is None or len(MyTitle) == 0: # if title is empty
                print("Title is empty")
                continue
            # write the title and url to the file
            self._File.write(MyTitle + "\t" + MyUrl + "\n")
            # get new url
            self._get_new_url(MyUrl, MySoup)


if __name__ == '__main__':
    test = CrawNewPage("https://www.roxylib.com/", "../CrawNewPageClass/text.txt", r"https://www.roxylib.com/.*")
    test.func()

# RootUrl = "https://www.roxylib.com"
# MyUrlManager = UrlManager()
# MyUrlManager.add_new_url(RootUrl)
# MyFile = open("text.txt", "w")
#
# while MyUrlManager.has_new_url():  # if there is a new url
#     MyUrl = MyUrlManager.get_url()
#     MyData = req.get(MyUrl, timeout=3)
#
#     if MyData.status_code != 200:  # 200 means success
#         print("Error!")  # 404 means not found
#         continue
#
#     MySoup = bs(MyData.text, "html.parser")
#     MyTitle = MySoup.title.getText()
#     print(MyTitle)
