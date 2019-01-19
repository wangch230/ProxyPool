import redis
import re
from random import choice
from proxyPool.setting import (
    REDIS_KEY,
    REDIS_PASSWORD,
    INITIAL_SCORE,
    REDIS_PORT,
    REDIS_HOST,
    MAX_SCORE,
    MIN_SCORE
)
from proxyPool.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis地址
        :param port: Redis端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加队列，设置分数为最初的分数
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        #  a sorted set that score is their value
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取代理，获取最高分代理，如果不存在，则以此按排名获取
        :return:
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理不能用，减一分，减到最低分，删除
        :param proxy: 代理
        :return: 代理对象
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print(proxy, '当前分数', score, '减一')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print(proxy, '不可用移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def count(self):
        """
        获取数量
        :return:
        """
        return self.db.zcard(REDIS_KEY)

    def exit(self, proxy):
        """
        判断代理是否存在
        :param proxy:
        :return:
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        可用设置为max
        :param proxy:
        :return:
        """
        print(proxy, '可用设置为最大值', MAX_SCORE)

    def all(self):
        """
        获取所有的代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, end):
        """
        获取某一分段的代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, start, end-1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(50, 100)
    print(result)