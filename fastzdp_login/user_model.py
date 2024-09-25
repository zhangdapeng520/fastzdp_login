from sqlmodel import SQLModel, Field
from typing import Optional


class FastZdpUserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)  # 用户名, unique会自动添加索引
    password: str  # 密码
    phone: str = Field(max_length=11, nullable=True, unique=True)  # 手机号
