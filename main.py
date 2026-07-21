from fastapi import FastAPI, HTTPException, APIRouter

from routers.users import router as users_router
from routers.admin import router as admin_router
from database import engine, Base


Base.metadata.create_all(bind=engine)
app=FastAPI(title="To-Do List Api", description="Для заметок")
@app.get("/")
def home():
    return {"message": "To-Do List Api"}

app.include_router(users_router)
app.include_router(admin_router)