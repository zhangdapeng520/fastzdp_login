from pydantic import BaseModel, Field


class SendCodeSchema(BaseModel):
    phone: str = Field(min_length=11, max_length=11)


class PhoneLoginSchema(BaseModel):
    """手机号登录校验"""
    phone: str = Field(min_length=11, max_length=11)
    code: int = Field(gt=999, lt=1000000)
