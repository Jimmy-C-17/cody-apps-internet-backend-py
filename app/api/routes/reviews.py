from typing import Any
from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser
from app.models.review import ReviewPublic, ReviewCreate
from app.services import review_service, product_service

router = APIRouter()

@router.post("/{product_id}/reviews", response_model=ReviewPublic)
def create_review_for_product(
    product_id: int,
    review_in: ReviewCreate,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    product = product_service.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado ❌")
        
    return review_service.create_review(
        session=session,
        review_in=review_in,
        user_id=current_user.id,
        product_id=product_id
    )

@router.get("/{product_id}/reviews", response_model=list[ReviewPublic])
def read_reviews_for_product(
    product_id: int,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    product = product_service.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado ❌")
        
    return review_service.get_reviews_by_product(session=session, product_id=product_id)
