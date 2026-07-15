from fastapi import FastAPI, HTTPException, APIRouter


from database import engine, Base


Base.metadata.create_all(bind=engine)
app=FastAPI(title="To-Do List Api", description="Для заметок")
@app.get("/")
def home():
    return {"message": "To-Do List Api"}