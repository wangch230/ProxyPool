# max score
MAX_SCORE = 100
# min score
MIN_SCORE = 0
# initial score
INITIAL_SCORE = 10

REDIS_HOST = 'localhost'
# redis port
REDIS_PORT = 6379

REDIS_PASSWORD = None

REDIS_KEY = 'proxy'

POOL_UPPER_THRESHOLD = 100

TEST_URL = 'http://www.baidu.com'


VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10
