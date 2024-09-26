import time
import random
import fastzdp_sqlmodel as fasm
import fastzdp_redis as fzr
from fastapi import APIRouter, status, Body, HTTPException
from sqlalchemy import Engine
from starlette.responses import JSONResponse

from .jwt_util import get_jwt, get_user_token
from .passlib_util import hash_256, verify_256
from .user_model import FastZdpUserModel
from .user_schema import SendCodeSchema, PhoneLoginSchema


def get_user_router(
        engine: Engine,
        jwt_key="zhangdapeng520",
        jwt_algorithm="HS256",
        jwt_token_expired=3 * 60 * 60,
        prefix="/fastzdp_login",
        get_phone_code_func=None,
        rdb: fzr.FastZDPRedisClient = None,
        code_expired: int = 60,
):
    """
    获取用户相关的路由
    - get_phone_code_func 用来获取手机验证码的函数, 如果为空, 我们则返回随机的数字
    - rdb Redis客户端对象
    - code_expired 验证码过期时间
    """
    user_router = APIRouter(prefix=prefix, tags=["fastzdp_login"])

    @user_router.post("/register/", summary="用户注册")
    def register_user(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
    ):
        """
        用户注册接口
        """
        # 检查用户名是否已存在
        users = fasm.get_by_dict(engine, FastZdpUserModel, {"username": username})
        if users and len(users) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

        # 创建新用户
        new_user = FastZdpUserModel(username=username, password=hash_256(password))
        fasm.add(engine, new_user)
        return {}

    # 登录接口
    @user_router.post("/login/", summary="用户登录")
    async def login_for_access_token(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
    ):
        """
        根据用户名和密码登录接口
        """
        # 查找
        users = fasm.get_by_dict(engine, FastZdpUserModel, {"username": username})
        if not users or len(users) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")

        # 校验密码
        user = users[0]
        if not verify_256(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")

        # 返回
        return get_user_token(
            jwt_key,
            jwt_algorithm,
            user.id,
            user.username,
            user.phone,
            jwt_token_expired,
        )

    @user_router.post("/code/", summary="发送验证码")
    async def send_code(schema: SendCodeSchema):
        """
        发送验证码
        - phone 手机号,长度是11位,不能为空
        """
        # 查找
        users = fasm.get_by_dict(engine, FastZdpUserModel, {"phone": schema.phone})
        if not users or len(users) == 0:
            # 不存在就新增
            fasm.add(engine, FastZdpUserModel(phone=schema.phone))

        # 发送验证码
        code = None
        if get_phone_code_func is not None:
            code = get_phone_code_func()
        else:
            code = random.randint(1000, 9999)

        # 缓存验证码
        if rdb is not None:
            rdb.set(schema.phone, code, code_expired)

        # 返回
        return {"code": code}

    @user_router.post("/phone_login/", summary="通过手机号登录")
    async def phone_login(schema: PhoneLoginSchema):
        """
        通过手机号登录
        - phone 手机号,长度是11位,不能为空
        """
        # 查找
        users = fasm.get_by_dict(engine, FastZdpUserModel, {"phone": schema.phone})
        if not users or len(users) == 0:
            return JSONResponse(status_code=404, content="不存在该用户")

        # 判断rdb是否存在
        if rdb is None:
            return JSONResponse(status_code=500, content="缓存对象不存在")

        # 校验验证码
        cache_code = rdb.get(schema.phone)
        if not cache_code:
            return JSONResponse(status_code=400, content="验证码已过期")
        if cache_code != str(schema.code):
            return JSONResponse(status_code=400, content="验证码不正确")

        # 返回
        user = users[0]
        return get_user_token(
            jwt_key,
            jwt_algorithm,
            user.id,
            user.username,
            user.phone,
            jwt_token_expired,
        )

    return user_router
