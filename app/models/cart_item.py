from typing import Optional
from sqlmodel import Field, SQLModel

# Esquema base para el Carrito
class CartItemBase(SQLModel):
    quantity: int = Field(default=1, ge=1)

# Modelo de Base de Datos
class CartItem(CartItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")

# Esquema para Agregar al Carrito (el cliente envía product_id y opcionalmente quantity)
class CartItemCreate(CartItemBase):
    product_id: int

# Esquema para Respuesta Pública
class CartItemPublic(CartItemBase):
    id: int
    user_id: int
    product_id: int

# Esquema para Actualizar Cantidad
class CartItemUpdate(SQLModel):
    quantity: Optional[int] = Field(default=None, ge=1)
