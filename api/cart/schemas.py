from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel



class CartItem(BaseModel):
    id: PydanticObjectId
    quantity: Optional[int] = 1
