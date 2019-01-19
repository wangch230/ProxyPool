
class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__()

    def __str__(self):
        print('代理池枯竭了')

