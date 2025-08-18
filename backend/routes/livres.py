from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import backend.schemas
import backend.crud
import backend.database

router = APIRouter(
    prefix="/api/livres",
    tags=["livres"]
)

# Récupérer tous les livres
@router.get("/", response_model=list[backend.schemas.LivreResponse])
def get_all_livres(db: Session = Depends(backend.database.get_db)):
    return backend.crud.get_all_livres(db)

# Récupérer un livre par ID
@router.get("/{book_id}", response_model=backend.schemas.LivreResponse)
def get_livre(book_id: int, db: Session = Depends(backend.database.get_db)):
    livre = backend.crud.get_livre(db, book_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return livre
