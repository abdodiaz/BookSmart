from fastapi import FastAPI
from backend.database import engine, Base
from backend import models
from backend.routes import users  # Import du routeur users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "API BookSmart fonctionne !"}
