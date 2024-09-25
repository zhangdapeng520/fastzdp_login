from sqlmodel import SQLModel, Field
from typing import Optional


class FastZdpUserModel(SQLModel, table=True):
    """用户模型表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=True)  # 用户名
    password: str = Field(nullable=True)  # 密码
    phone: str = Field(max_length=11, nullable=True, index=True)  # 手机号
