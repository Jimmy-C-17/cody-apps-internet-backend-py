from typing import Optional
from sqlmodel import Field, SQLModel

# Esquema base para Reseña
class ReviewBase(SQLModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(min_length=1)

# Modelo de Base de Datos
class Review(ReviewBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")

# Esquema para Crear (el cliente solo envía rating y comment)
class ReviewCreate(ReviewBase):
    pass

# Esquema para Lectura Pública
class ReviewPublic(ReviewBase):
    id: int
    user_id: int
    product_id: int
