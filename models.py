from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ProductCreate(BaseModel):
    name: str = Field(..., example="T-shirt")
    size: Optional[str] = Field(None, example="large")
    price: float = Field(..., example=499.99)
    description: Optional[str] = Field(None, example="A comfortable cotton t-shirt")

class ProductInDB(ProductCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class ProductListResponse(BaseModel):
    products: List[ProductInDB]

class OrderItem(BaseModel):
    product_id: PyObjectId = Field(..., alias="product_id")
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    user_id: str = Field(..., example="user123")
    items: List[OrderItem]

class OrderInDB(OrderCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

class OrderListResponse(BaseModel):
    orders: List[OrderInDB]
