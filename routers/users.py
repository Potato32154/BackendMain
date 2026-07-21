from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import hash_password, verify_password, create_access_token
from database import get_db
from models import User
from schemas import UserResponse, UserCreate,Token

router=APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate,db:Session=Depends(get_db)):
    if user_data.password!=user_data.password_repeat:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    existing_user = db.query(User).filter((User.name==user_data.name)|(User.email==user_data.email)).first()
    if existing_user:
        if existing_user.name==user_data.name:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
        else:
            raise HTTPException(status_code=400,detail="пользователь с таким email уже существует")
    new_user = User(name=user_data.name,
                    email=user_data.email,
                    password_hash=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login", response_model=Token)
def login_user(from_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.name==from_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    if not verify_password(from_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь заблокирован")
    access_token=create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}