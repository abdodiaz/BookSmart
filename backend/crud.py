# crud.py
from sqlalchemy.orm import Session
from backend.models import Adherent, Livre, Emprunt, Reservation, HistoriqueEmprunt, Notification
from backend.schemas import AdherentCreate, LivreCreate  # utiliser les bons schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------- ADHERENTS --------

def get_adherent_by_email(db: Session, email: str):
    return db.query(Adherent).filter(Adherent.email == email).first()


def create_adherent(db: Session, adherent: AdherentCreate):
    hashed_password = pwd_context.hash(adherent.password)
    db_adherent = Adherent(
        nom=adherent.nom,
        email=adherent.email,
        hashed_password=hashed_password
    )
    db.add(db_adherent)
    db.commit()
    db.refresh(db_adherent)
    return db_adherent


def get_all_adherents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Adherent).offset(skip).limit(limit).all()


# -------- LIVRES --------

def get_all_livres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Livre).offset(skip).limit(limit).all()


def get_livre(db: Session, livre_id: int):
    return db.query(Livre).filter(Livre.id == livre_id).first()


def create_livre(db: Session, livre: LivreCreate):
    db_livre = Livre(
        titre=livre.titre,
        prix=livre.prix,
        description=livre.description,
        image_url=livre.image_url,
        stock=livre.stock,
        rating=livre.rating
    )
    db.add(db_livre)
    db.commit()
    db.refresh(db_livre)
    return db_livre


def update_livre_stock(db: Session, livre_id: int, stock: int):
    db_livre = db.query(Livre).filter(Livre.id == livre_id).first()
    if db_livre:
        db_livre.stock = stock
        db.commit()
        db.refresh(db_livre)
    return db_livre


def delete_livre(db: Session, livre_id: int):
    db_livre = db.query(Livre).filter(Livre.id == livre_id).first()
    if db_livre:
        db.delete(db_livre)
        db.commit()
    return db_livre
