from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

# Adherent (utilisateur)
class AdherentBase(BaseModel):
    nom: str = Field(..., example="Ahmed Benali")
    email: EmailStr

class AdherentCreate(AdherentBase):
    password: str = Field(..., min_length=6)

class AdherentOut(AdherentBase):
    id: int
    role: str
    date_inscription: Optional[date]

    class Config:
        orm_mode = True


# Livre
class LivreBase(BaseModel):
    titre: str
    description: Optional[str]
    image_url: Optional[str]
    stock: int
    rating: Optional[int]

class LivreOut(LivreBase):
    id: int

    class Config:
        orm_mode = True


# Réservation
class ReservationBase(BaseModel):
    id_adherent: int
    id_livre: int

class ReservationOut(ReservationBase):
    id: int
    date_reservation: Optional[date]
    statut: Optional[str]

    class Config:
        orm_mode = True


# Emprunt
class EmpruntBase(BaseModel):
    id_adherent: int
    id_livre: int
    date_emprunt: Optional[date]
    date_retour_prevue: date

# Emprunt avec retour effectif
class EmpruntOut(EmpruntBase):
    id: int
    date_retour_effectif: Optional[date]

    class Config:
        orm_mode = True