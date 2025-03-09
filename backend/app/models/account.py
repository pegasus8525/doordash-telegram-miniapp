from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class Account(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    password: str
    chain_id: Optional[PyObjectId]
    position_in_chain: int
    referral_link: str
    status: str  # 'available', 'in_use', 'used'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used_at: Optional[datetime]

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
