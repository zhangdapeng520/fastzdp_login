import time
from fastapi import APIRouter, status, Body, Depends, HTTPException
from sqlalchemy.orm import Session as SASession
from sqlmodel import select
from .jwt_util import get_jwt
from .passlib_util import hash_256, verify_256
from .user_model import FastZdpUserModel


def get_user_router(
        get_db,
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
            db: SASession = Depends(get_db),
    ):
        # 检查用户名是否已存在
        user = db.exec(select(FastZdpUserModel).where(FastZdpUserModel.username == username)).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")

        # 创建新用户
        new_user = FastZdpUserModel(username=username, password=hash_256(password))
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            print(e)
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户注册失败")

        return {"message": "用户注册成功", "user_id": new_user.id}

    # 登录接口
    @user_router.post("/login/", summary="用户登录")
    async def login_for_access_token(
            username: str = Body(str, min_length=2, max_length=36),
            password: str = Body(str, min_length=6, max_length=128),
            db: SASession = Depends(get_db),
    ):
        user = db.exec(select(FastZdpUserModel).where(FastZdpUserModel.username == username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")
        if not verify_256(password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码错误")
        data = {"username": user.username, "id": user.id, "time": time.time(),
                "expired": jwt_token_expired}
        access_token = get_jwt(data, jwt_key, jwt_algorithm)
        return {"access_token": access_token, "token_type": "bearer"}

    return user_router
