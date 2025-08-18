from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import AdherentResponse, AdherentCreate, LivreResponse, LivreCreate
from backend.auth import get_current_admin

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

# --- Gérer les adhérents ---
@router.get("/adherents", response_model=list[AdherentResponse])
def get_all_adherents(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.get_all_adherents(db)

@router.put("/adherents/{adherent_id}")
def modify_adherent(adherent_id: int, adherent: AdherentCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.update_adherent(db, adherent_id, adherent)

@router.delete("/adherents/{adherent_id}")
def delete_adherent(adherent_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    crud.delete_adherent(db, adherent_id)
    return {"message": "Adhérent supprimé"}


# --- Gérer les livres ---
@router.get("/livres", response_model=list[LivreResponse])
def get_all_livres(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.get_livres(db)

@router.post("/livres", response_model=LivreResponse)
def add_livre(livre: LivreCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.create_livre(db, livre)

@router.put("/livres/{livre_id}", response_model=LivreResponse)
def modify_livre(livre_id: int, livre: LivreCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.update_livre(db, livre_id, livre)

@router.delete("/livres/{livre_id}")
def delete_livre(livre_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    crud.delete_livre(db, livre_id)
    return {"message": "Livre supprimé"}


# --- Gérer les emprunts et retours ---
@router.post("/emprunts")
def create_emprunt(adherent_id: int, livre_id: int, date_retour_prevue: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.create_emprunt(db, adherent_id, livre_id, date_retour_prevue)

@router.put("/retours/{emprunt_id}")
def enregistrer_retour(emprunt_id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.enregistrer_retour(db, emprunt_id)


# --- Statistiques ---
@router.get("/statistiques")
def get_stats(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.get_statistics(db)
    
@router.get("/statistiques")
def get_stats(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return crud.get_statistics(db)