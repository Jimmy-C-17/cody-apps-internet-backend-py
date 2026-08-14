from sqlmodel import Session, select
from app.models.cart_item import CartItem, CartItemCreate, CartItemUpdate

def add_to_cart(session: Session, cart_in: CartItemCreate, user_id: int) -> CartItem:
    # Verificar si el producto ya está en el carrito del usuario
    statement = select(CartItem).where(
        CartItem.user_id == user_id, 
        CartItem.product_id == cart_in.product_id
    )
    existing_item = session.exec(statement).first()
    
    if existing_item:
        # Si ya existe, incrementamos la cantidad
        existing_item.quantity += cart_in.quantity
        session.add(existing_item)
        session.commit()
        session.refresh(existing_item)
        return existing_item
    
    # Si no existe, creamos un nuevo registro inyectando user_id
    db_item = CartItem(
        product_id=cart_in.product_id,
        quantity=cart_in.quantity,
        user_id=user_id
    )
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def get_user_cart(session: Session, user_id: int) -> list[CartItem]:
    statement = select(CartItem).where(CartItem.user_id == user_id)
    return list(session.exec(statement).all())

def remove_from_cart(session: Session, cart_item_id: int, user_id: int) -> CartItem | None:
    statement = select(CartItem).where(
        CartItem.id == cart_item_id, 
        CartItem.user_id == user_id
    )
    cart_item = session.exec(statement).first()
    if not cart_item:
        return None
    session.delete(cart_item)
    session.commit()
    return cart_item
