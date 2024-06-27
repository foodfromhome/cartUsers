from beanie import Document, PydanticObjectId
from typing import Optional, List
from pydantic import Field
from datetime import datetime
from api.cart.schemas import CartItem


class CartUser(Document):
    id: PydanticObjectId = Field(None, alias="_id")
    user_id: int = Field(None, alias="user_id")
    items: List[CartItem] = Field(None, alias="items")
    updated_at: datetime = Field(default=datetime.now(), alias="updated_at")
    created_at: datetime = Field(default=datetime.now(), alias="created_at")
