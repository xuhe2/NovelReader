import csv
import random


class IPManager:
    """
    IP管理器
    初始化参数:CSV文件名
    """

    # 初始化,加入读取文件
    def __init__(self, filename='ip.csv'):
        """
        :param filename: CSV文件名
        """
        self._ip_list = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self._ip_list.append(row[0])

    # 随机获取一个IP
    def get_random_ip(self):
        """
        :return: 随机获取一个IP
        :return:
        """
        return random.choice(self._ip_list)

    def get_proxies(self):
        """
        获取适用于requests的proxies
        :return: proxies
        """
        proxies = {
            'http': self.get_random_ip()
        }
        return proxies


if __name__ == '__main__':
    ip_manager = IPManager('../IPManager/ip.csv')
    import requests
    html = requests.get('https://www.baidu.com', proxies=ip_manager.get_proxies()) # 使用代理
    print(html.status_code)
    print(html.text)
