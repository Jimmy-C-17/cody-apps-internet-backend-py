from typing import Optional
from sqlmodel import Field, SQLModel

# Esquema base
class ProductBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    price: float
    stock: int = Field(default=0)
    category_id: int = Field(foreign_key="category.id")

# Modelo de Base de Datos
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Esquemas para la API (Pydantic / DTO)
class ProductCreate(ProductBase):
    pass

class ProductPublic(ProductBase):
    id: int

class ProductUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    stock: Optional[int] = Field(default=None)
    category_id: Optional[int] = Field(default=None)
