import time
import random
import fastzdp_sqlmodel as fasm
from fastapi import APIRouter, status, Body, HTTPException
from sqlalchemy import Engine
from .jwt_util import get_jwt
from .passlib_util import hash_256, verify_256
from .user_model import FastZdpUserModel
from .user_schema import SendCodeSchema

def get_user_router(
        engine: Engine,
        jwt_key="zhangdapeng520",
        jwt_algorithm="HS256",
        jwt_token_expired=3 * 60 * 60,
        prefix="/fastzdp_login",
        get_phone_code_func=None,
):
    """
    获取用户相关的路由
    - get_phone_code_func 用来获取手机验证码的函数, 如果为空, 我们则返回随机的数字
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

        # 生成Token
        data = {
            "username": user.username,
            "id": user.id,
            "time": time.time(),
            "expired": jwt_token_expired,
        }
        access_token = get_jwt(data, jwt_key, jwt_algorithm)

        # 返回
        return {"access_token": access_token, "token_type": "bearer"}

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

        # TODO: 发送验证码
        code = None
        if get_phone_code_func is not None:
            code = get_phone_code_func()
        else:
            code = random.randint(1000, 9999)
        # 返回
        return {"code": code}

    return user_router
