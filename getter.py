from proxyPool.crawler import Crawler
from proxyPool.db import RedisClient
from proxyPool.setting import (
    POOL_UPPER_THRESHOLD
)
import sys


class Getter:

    def __init__(self):
        self.db = RedisClient()
        self.crawl = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了临界值
        :return:
        """
        return self.db.count() >= POOL_UPPER_THRESHOLD

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawl.__CrawlCount__):
                callback = self.crawl.__CrawlFunc__[callback_label]

                proxy = self.crawl.get_proxies(callback)
                sys.stdout.flush()
                for i in proxy:
                    self.db.add(i)


if __name__ == '__main__':
    g = Getter()
    g.run()



