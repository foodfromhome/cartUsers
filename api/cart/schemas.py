from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class CartItem(BaseModel):
    meals_id: PydanticObjectId
    price: float
    quantity: Optional[int] = Field(1)
