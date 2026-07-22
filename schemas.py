from pydantic import BaseModel
from typing import Optional, List


class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    password_repeat: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    role: str="user"
    class Config:
        from_attributes=True

class UserAdminResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    is_active: bool
    class Config:
        from_attributes=True


class UserAdminUpdate(BaseModel):
    email: Optional[str]=None
    name: Optional[str]=None
    password: Optional[str]=None
    role: Optional[str]=None
    is_active: Optional[bool]=None


class Token(BaseModel):
    access_token: str
    token_type: str

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]=None
    price: int
    stock_quantity: int=0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    stock_quantity: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    stock_quantity: int
    class Config:
        from_attributes=True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int=1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes=True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: int
    quantity: int
    class Config:
        from_attributes=True

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: int
    items: List[OrderItemResponse]

    class Config:
        from_attributes=True
