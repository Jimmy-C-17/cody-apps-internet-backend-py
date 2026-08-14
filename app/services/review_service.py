from sqlmodel import Session, select
from app.models.review import Review, ReviewCreate

def create_review(
    session: Session, 
    review_in: ReviewCreate, 
    user_id: int, 
    product_id: int
) -> Review:
    db_item = Review(
        **review_in.model_dump(),
        user_id=user_id,
        product_id=product_id
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_reviews_by_product(session: Session, product_id: int) -> list[Review]:
    statement = select(Review).where(Review.product_id == product_id)
    return list(session.exec(statement).all())
