from typing import Any
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.models.product import ProductPublic, ProductCreate, ProductUpdate
from app.services import product_service

router = APIRouter()

@router.get("/", response_model=list[ProductPublic])
def read_products(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    return product_service.get_products(session=session, skip=skip, limit=limit)

@router.post("/", response_model=ProductPublic)
def create_product(*, session: SessionDep, current_user: CurrentUser, product_in: ProductCreate) -> Any:
    return product_service.create_product(session=session, product_in=product_in)

@router.get("/{product_id}", response_model=ProductPublic)
def read_product(product_id: int, session: SessionDep, current_user: CurrentUser) -> Any:
    product = product_service.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado ❌")
    return product

@router.put("/{product_id}", response_model=ProductPublic)
@router.patch("/{product_id}", response_model=ProductPublic)
def update_product(product_id: int, product_in: ProductUpdate, session: SessionDep, current_user: CurrentUser) -> Any:
    product = product_service.update_product(session=session, product_id=product_id, product_in=product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado ❌")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: SessionDep, current_user: CurrentUser) -> Any:
    product = product_service.delete_product(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado ❌")
    return {"message": "Producto eliminado exitosamente"}
