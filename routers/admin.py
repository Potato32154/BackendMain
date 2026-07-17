from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session


from database import get_db
from models import User
from schemas import UserResponse

router=APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/all_users", response_model=list[UserResponse])
def get_all_users(db:Session=Depends(get_db)):
    all_users=db.query(User).all()
    return all_users