from datetime import datetime
from typing import List
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from api.cart.schemas import CartItem
from api.cart.models import CartUser

router = APIRouter()


@router.post("/{user_id}/carts/{meals_id}", status_code=status.HTTP_201_CREATED, summary="Добавление в корзину")
async def add_to_cart(meals_id: PydanticObjectId, user_id: int):
    try:

        cart = await CartUser.find_one({"user_id": user_id})

        if cart is None:

            cart = CartUser(
                user_id=user_id,
                items=[CartItem(id=meals_id, quantity=1)]
            )
            await cart.save()
            return cart

        else:

            cart.items.append(CartItem(id=meals_id, quantity=1))
            cart.updated_at = datetime.now()
            await cart.save()

            return cart

    except HTTPException as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/carts/{user_id}", status_code=status.HTTP_200_OK, summary="Корзина пользователя",
            response_model=List[CartItem])
async def get_cart(user_id: int):
    try:

        cart = await CartUser.find_one({"user_id": user_id})

        if cart:

            return cart.items

    except HTTPException as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{user_id}/carts/{meals_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удаление блюда из корзины")
async def delete_meals_to_cart(user_id: int, meals_id: PydanticObjectId):
    try:
        cart = await CartUser.find_one({"user_id": user_id})

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

        cart.items = [item for item in cart.items if item.id != meals_id]
        cart.updated_at = datetime.now()

        await cart.save()


    except HTTPException as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{user_id}/carts/{meals_id}", status_code=status.HTTP_200_OK,
            summary="Обновление количества блюд в корзине")
async def update_cart_item_quantity(user_id: int, meals_id: PydanticObjectId, quantity: int):
    try:
        cart = await CartUser.find_one({"user_id": user_id})

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

        for item in cart.items:
            if item.id == meals_id:
                item.quantity = quantity
                cart.updated_at = datetime.now()
                break
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart")

        await cart.save()

        return cart

    except HTTPException as e:
        return JSONResponse(content=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

