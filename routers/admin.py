from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth import get_current_user, hash_password
from database import get_db
from models import User
from schemas import UserAdminResponse, UserAdminUpdate

router=APIRouter(prefix="/admin", tags=["Admin"])

def admin_required(current_user:User=Depends(get_current_user)):
    if current_user.role!="admin":
        raise HTTPException(status_code=403,detail="Недостаточно прав. Требуется роль")
    return current_user

@router.get("/all_users", response_model=list[UserAdminResponse])
def get_all_users(_:User=Depends(admin_required),db:Session=Depends(get_db)):
    return db.query(User).all()

@router.get("/user_detail/{user_id}", response_model=UserAdminResponse)
def get_user_detail(user_id: int,_:User=Depends(admin_required) ,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.put("/user_edits/{user_id}", response_model=UserAdminResponse)
def user_edits(user_id: int,user_data:UserAdminUpdate,_:User=Depends(admin_required) ,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Пользователь не найден")
    if user_data.name is not None and user_data.name != user.name:
        if db.query(User).filter(User.name==user_data.name,User.id!=user_id).first():
            raise HTTPException(status_code=400, detail="Имя уже используется")
        user.name = user_data.name

    if user_data.email is not None and user_data.email != user.email:
        if db.query(User).filter(User.email==user_data.email,User.id!=user_id).first():
            raise HTTPException(status_code=400, detail="Email уже используется")
        user.email = user_data.email

    if user_data.password is not None:
        user.password_hash = hash_password(user_data.password)

    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)
    return user

@router.delete("/user_delete/{user_id}")
def user_delete_user(user_id: int,admin:User=Depends(admin_required) ,db:Session=Depends(get_db)):
    if admin.id==user_id:
        raise HTTPException(status_code=400,detail="Нельзя удалить самого себя")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"detail":"Пользователь удален","user_id":user.id}

@router.patch("/user_block/{user_id}")
def block_user(user_id:int,block:bool,_:User=Depends(admin_required) ,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.is_active = not block
    db.commit()
    text_block="Заблокирован" if block else "разблокирован"
    return {"detail": f"Пользователь {text_block}","user_id":user.id}

@router.patch("/user_role/{user_id}")
def change_user_role(user_id: int, new_role:str,_:User=Depends(admin_required) ,db:Session=Depends(get_db)):
    all_roles={"admin","user","moderator"}
    if new_role not in all_roles:
        raise HTTPException(status_code=400, detail=f"Недоступная роль. Разрешены: {', '.join(all_roles)}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.role = new_role
    db.commit()
    return {"detail": f"Роль изменена на {new_role}","user_id":user.id}
