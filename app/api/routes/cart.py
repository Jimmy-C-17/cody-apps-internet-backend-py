from typing import Any
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.models.cart_item import CartItemPublic, CartItemCreate
from app.services import cart_service, product_service

router = APIRouter()

@router.post("/", response_model=CartItemPublic)
def add_item_to_cart(
    cart_in: CartItemCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    # Validar que el producto realmente existe en la base de datos
    product = product_service.get_product_by_id(session=session, product_id=cart_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado ❌")
        
    # Inyectar el user_id de forma segura extraído del JWT del usuario autenticado
    return cart_service.add_to_cart(
        session=session,
        cart_in=cart_in,
        user_id=current_user.id
    )

@router.get("/", response_model=list[CartItemPublic])
def read_user_cart(
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    return cart_service.get_user_cart(session=session, user_id=current_user.id)

@router.delete("/{cart_item_id}")
def delete_cart_item(
    cart_item_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    deleted_item = cart_service.remove_from_cart(
        session=session, 
        cart_item_id=cart_item_id, 
        user_id=current_user.id
    )
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Elemento del carrito no encontrado ❌")
    return {"message": "Producto eliminado del carrito exitosamente"}
