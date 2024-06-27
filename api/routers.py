from fastapi import APIRouter
from api.cart.api import router

cart_router = APIRouter(
    prefix='/api/v1',
    tags=['Корзина пользователя'],
)

cart_router.include_router(router)
