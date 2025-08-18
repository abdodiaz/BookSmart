from sqlalchemy.orm import Session
from backend import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hasher le mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Vérifier le mot de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Créer un nouvel adhérent
def create_adherent(db: Session, adherent: schemas.AdherentCreate):
    hashed_pw = hash_password(adherent.password)
    db_adherent = models.Adherent(
        nom=adherent.nom,
        email=adherent.email,
        password_hash=hashed_pw,
        role="adherent"
    )
    db.add(db_adherent)
    db.commit()
    db.refresh(db_adherent)
    return db_adherent

# Rechercher un adhérent par email
def get_adherent_by_email(db: Session, email: str):
    return db.query(models.Adherent).filter(models.Adherent.email == email).first()
