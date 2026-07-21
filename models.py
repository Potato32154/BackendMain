from sqlalchemy import String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from database import Base

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String(150),unique=True,index=True,nullable=False)
    name:Mapped[str]=mapped_column(String(100),unique=True,index=True,nullable=False)
    password_hash:Mapped[str]=mapped_column(String(255),nullable=False)
    role:Mapped[str]=mapped_column(String(20),default="user",nullable=False)
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)

    cart_items:Mapped[list["CartItem"]]=relationship(back_populates="user",cascade="all,delete-orphan")
    orders:Mapped[list["Order"]]=relationship(back_populates="user",cascade="all,delete-orphan")




class Product(Base):
    __tablename__ = 'products'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(150), nullable=False)
    description:Mapped[str| None]=mapped_column(String(500),nullable=True)
    price:Mapped[int]=mapped_column(Integer,nullable=False)
    stock_quantity:Mapped[int]=mapped_column(Integer,default=0,nullable=False)

    cart_items:Mapped[list["CartItem"]]=relationship(back_populates="product")
    order_items:Mapped[list["OrderItem"]]=relationship(back_populates="product")


class CartItem(Base):
    __tablename__ = 'cart_items'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey('users.id'),nullable=False)
    product_id:Mapped[int]=mapped_column(Integer,ForeignKey('products.id'),nullable=False)
    quantity:Mapped[int]=mapped_column(Integer,default=1,nullable=False)

    user:Mapped["User"]=relationship(back_populates="cart_items")
    product:Mapped["Product"]=relationship(back_populates="cart_items")



class Order(Base):
    __tablename__ = 'orders'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey('users.id'),nullable=False,index=True)
    total_amount:Mapped[int]=mapped_column(Integer,nullable=False)

    user:Mapped["User"]=relationship(back_populates="orders")
    items:Mapped[list["OrderItem"]]=relationship(back_populates="order",cascade="all,delete-orphan")



class OrderItem(Base):
    __tablename__ = 'order_items'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
    order_id:Mapped[int]=mapped_column(Integer,ForeignKey('orders.id'),nullable=False)
    product_id:Mapped[int]=mapped_column(Integer,ForeignKey('products.id'),nullable=False)
    product_name:Mapped[str]=mapped_column(String(150),nullable=False)
    product_price:Mapped[int]=mapped_column(Integer,nullable=False)
    quantity:Mapped[int]=mapped_column(Integer,nullable=False)

    order:Mapped["Order"]=relationship(back_populates="items")
    product:Mapped["Product"]=relationship(back_populates="order_items")
