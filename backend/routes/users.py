from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import backend.schemas
import backend.crud
import backend.database
import backend.auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/api",
    tags=["users"]
)

# Inscription
@router.post("/register", response_model=backend.schemas.AdherentResponse)
def register_user(adherent: backend.schemas.AdherentCreate, db: Session = Depends(backend.database.get_db)):
    existing = backend.crud.get_adherent_by_email(db, adherent.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà utilisé")
    return backend.crud.create_adherent(db, adherent)

# Connexion
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(backend.database.get_db)):
    user = backend.crud.get_adherent_by_email(db, form_data.username)
    if not user or not backend.auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants incorrects")
    access_token = backend.auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
