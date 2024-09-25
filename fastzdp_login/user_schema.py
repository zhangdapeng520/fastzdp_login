from pydantic import BaseModel, Field


class SendCodeSchema(BaseModel):
    phone: str = Field(min_length=11, max_length=11)
