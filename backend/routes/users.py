from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend import schemas, crud, database
from backend.auth import verify_password, create_access_token

router = APIRouter(
    prefix="/api",
    tags=["users"]
)

# Dépendance pour sécuriser les routes plus tard
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


@router.post("/register", response_model=schemas.AdherentOut)
def register_user(adherent: schemas.AdherentCreate, db: Session = Depends(database.get_db)):
    existing = crud.get_adherent_by_email(db, adherent.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà utilisé"
        )
    return crud.create_adherent(db, adherent)


@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_adherent_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}
