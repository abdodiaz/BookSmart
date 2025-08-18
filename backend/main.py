from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import users, livres, reservations, admin, stats, recommandations
from backend.database import Base, engine

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookSmart API",
    description="API pour gestion bibliothèque avec recommandations",
    version="1.0.0"
)

# CORS
origins = ["http://localhost", "http://localhost:8000", "http://127.0.0.1:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(users.router)
app.include_router(livres.router)
app.include_router(reservations.router)
app.include_router(admin.router)
app.include_router(stats.router)
app.include_router(recommandations.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur BookSmart API"}
