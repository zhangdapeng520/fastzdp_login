import fastzdp_login
import fastzdp_api as api
import fastzdp_redis as fzr
from sqlmodel import create_engine

# 创建数据库引擎
db_url = "mysql+pymysql://root:zhangdapeng520@127.0.0.1:3306/fastzdp_login?charset=utf8mb4"
engine = create_engine(db_url, echo=True)
rdb = fzr.FastZDPRedisClient()

app = api.Api()

# 伪造一个密钥，实际使用时应该使用安全的方式存储
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 令牌有效期
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 这是一段模拟获取真实验证码的功能
def send_phone_code():
    """模拟发送验证码的功能"""
    import random
    return random.randint(100000, 999999)

app.include_router(fastzdp_login.get_user_router(
    engine,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    get_phone_code_func=send_phone_code,
    rdb=rdb, # 缓存对象
))

if __name__ == '__main__':
    app.run(port=8889)
