from sqlmodel import SQLModel, Field
from typing import Optional


class FastZdpUserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
