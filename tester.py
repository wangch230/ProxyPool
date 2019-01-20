import asyncio
import aiohttp
import time
import sys
from aiohttp import ClientError
from proxyPool.db import RedisClient
from proxyPool.setting import *


class Tester():

    def __init__(self):
        self.db = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param self:
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=True)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        print('代理可用，'+ proxy +'设置为最高分')
                        self.db.max(proxy)

                    else:
                        print('代理相应不合法' + response.status + 'IP' +proxy + '分数减一')
                        self.db.decrease(proxy)
            except ClientError as e:
                print('代理无法响应', e)
                self.db.decrease(proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试开始执行')
        try:
            count = self.db.count()
            print('共有' + count + '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.db.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)

        except Exception as e:
            print('测试器发生错误', e.args)


