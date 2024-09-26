# fastzdp_login

专为Fast API打造的用户登录注册相关功能的微代码框架

Github地址：https://github.com/zhangdapeng520/fastzdp_login

## 特性

- 1、微代码开发
- 2、自动拥有注册接口，会对密码进行加密处理
- 3、自动拥有登录接口，会返回JWT Token

## 安装

```bash
pip install fastzdp_login
```

## 使用教程

### 快速入门

通过下面的代码，你会自动拥有fastzdpusermodel这张数据库表，同时还会自动拥有登录和注册等接口。

示例代码：

```python
import fastzdp_login
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

# 创建数据库引擎
sqlite_url = "mysql+pymysql://root:root@127.0.0.1:3306/fastzdp_login?charset=utf8mb4"
engine = create_engine(sqlite_url, echo=True)

# 确保表存在
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# 伪造一个密钥，实际使用时应该使用安全的方式存储
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 令牌有效期
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app.include_router(fastzdp_login.get_user_router(
    engine,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES * 60
))

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8888)
```

测试注册接口：

```bash
req -X POST -H 'Content-Type:application/json' -d '{\"username\":\"zhangdapeng\",\"password\":\"zhangdapeng520\"}' http://127.0.0.1:8888/fastzdp_login/register/
```

测试登录接口：

```bash
req -X POST -H 'Content-Type:application/json' -d '{\"username\":\"zhangdapeng\",\"password\":\"zhangdapeng520\"}' http://127.0.0.1:8888/fastzdp_login/login/
```

## 版本历史

### v0.1.3

- 代码改造，迁移至Github

### v0.1.4

- 整合fastzdp_sqlmodel

### v0.1.5

- 新增发送验证码接口
- 新增手机号登录接口
- 整合fastzdp_redis框架
