from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import backend.schemas
import backend.crud
import backend.database
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api",
    tags=["reservations"]
)

# Réserver un livre
@router.post("/")
def reserve_book(book_id: int, db: Session = Depends(backend.database.get_db), current_user=Depends(get_current_user)):
    livre = backend.crud.get_livre(db, book_id)
    if not livre:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    if livre.stock <= 0:
        raise HTTPException(status_code=400, detail="Livre non disponible")
    # Vérifier si l'utilisateur a déjà réservé
    existing = backend.crud.get_reservation(db, current_user.id, book_id)
    if existing:
        raise HTTPException(status_code=400, detail="Vous avez déjà réservé ce livre")
    # Créer réservation
    return backend.crud.create_reservation(db, current_user.id, book_id)
