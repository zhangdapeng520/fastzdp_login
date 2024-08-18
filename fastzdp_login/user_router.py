import time
import fastzdp_sqlmodel as fs
from fastapi import APIRouter, status, Body, HTTPException
from sqlalchemy import Engine
from .jwt_util import get_jwt
from .passlib_util import hash_256, verify_256
from .user_model import FastZdpUserModel


def get_user_router(
        engine: Engine,
        jwt_key="zhangdapeng520",
        jwt_algorithm="HS256",
        jwt_token_expired=3 * 60 * 60,
        prefix="/fastzdp_login",
):
    user_router = APIRouter(prefix=prefix, tags=["fastzdp_login"])

    @user_router.post("/register/", summary="用户注册")
    def register_user(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
    ):
        # 检查用户名是否已存在
        users = fs.get_by_dict(engine, FastZdpUserModel, {"username": username})
        if users and len(users) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

        # 创建新用户
        new_user = FastZdpUserModel(username=username, password=hash_256(password))
        fs.add(engine, new_user)
        return {}

    # 登录接口
    @user_router.post("/login/", summary="用户登录")
    async def login_for_access_token(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
    ):
        # 查找
        users = fs.get_by_dict(engine, FastZdpUserModel, {"username": username})
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

    return user_router
