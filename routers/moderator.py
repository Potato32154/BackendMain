from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth import get_current_user, hash_password
from database import get_db
from models import User, Product, Order
from schemas import ProductResponse, ProductCreate, ProductUpdate, OrderResponse

router=APIRouter(prefix="/moderator", tags=["Moderator"])

def moderator_required(current_user:User=Depends(get_current_user)):
    if current_user.role!="moderator":
        raise HTTPException(status_code=403,detail="Недостаточно прав. Требуется роль moderator")
    return current_user

@router.get("/products", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db),_:User=Depends(moderator_required)):
    return db.query(Product).all()

@router.get("/product/{product_id}", response_model=ProductResponse)
def get_product_detail(product_id: int,_:User=Depends(moderator_required),db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Товар не найден")
    return product

@router.post("/products_new",response_model=ProductResponse, status_code=201)
def create_new_product(product_data:ProductCreate, db: Session = Depends(get_db),_:User=Depends(moderator_required)):
    new_product =Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock_quantity=product_data.stock_quantity
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/product_update/{product_id}",response_model=ProductResponse)
def update_product(product_id: int,product_data:ProductUpdate,_:User=Depends(moderator_required),db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Товар не найден")
    if product_data.name is not None:
        product.name = product_data.name
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.stock_quantity is not None:
        product.stock_quantity = product_data.stock_quantity
    db.commit()
    db.refresh(product)
    return product

@router.delete("/product_delete/{product_id}")
def delete_product(product_id: int,_:User=Depends(moderator_required),db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(product)
    db.commit()
    return {"detail":"Товар удален","product_id":product_id}

#==========================Заказы============================
@router.get("/orders_all", response_model=list[OrderResponse])
def get_all_orders(db: Session = Depends(get_db),_:User=Depends(moderator_required)):
    return db.query(Order).all()

@router.get("/order/{orders_id}", response_model=OrderResponse)
def get_orders_detail(orders_id: int,_:User=Depends(moderator_required),db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.id == orders_id).first()
    if not orders:
        raise HTTPException(status_code=404,detail="Заказ не найден")
    return orders


