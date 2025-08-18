# backend/schemas.py
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ------------------------
# Adherent
# ------------------------
class AdherentBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    role: Optional[str] = "user"


class AdherentCreate(AdherentBase):
    password: str


class AdherentResponse(AdherentBase):
    id: int
    date_inscription: datetime

    class Config:
        orm_mode = True


# ------------------------
# Livre
# ------------------------
class LivreBase(BaseModel):
    titre: str
    prix: float
    description: Optional[str] = None
    stock: int = 1
    rating: Optional[float] = 0.0
    image_url: Optional[str] = None


class LivreCreate(LivreBase):
    pass


class LivreResponse(LivreBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------
# Emprunt
# ------------------------
class EmpruntBase(BaseModel):
    date_emprunt: date
    date_retour_prevue: date
    date_retour_effectif: Optional[date] = None


class EmpruntCreate(EmpruntBase):
    id_adherent: int
    id_livre: int


class EmpruntResponse(EmpruntBase):
    id: int
    id_adherent: int
    id_livre: int

    class Config:
        orm_mode = True


# ------------------------
# Reservation
# ------------------------
class ReservationBase(BaseModel):
    statut: str = "en_attente"


class ReservationCreate(ReservationBase):
    id_adherent: int
    id_livre: int


class ReservationResponse(ReservationBase):
    id: int
    id_adherent: int
    id_livre: int
    date_reservation: datetime

    class Config:
        orm_mode = True


# ------------------------
# Historique Emprunt
# ------------------------
class HistoriqueEmpruntBase(BaseModel):
    date_emprunt: date
    note: Optional[int] = None


class HistoriqueEmpruntCreate(HistoriqueEmpruntBase):
    id_adherent: int
    id_livre: int


class HistoriqueEmpruntResponse(HistoriqueEmpruntBase):
    id: int
    id_adherent: int
    id_livre: int

    class Config:
        orm_mode = True


# ------------------------
# Notification
# ------------------------
class NotificationBase(BaseModel):
    message: str
    lu: bool = False


class NotificationCreate(NotificationBase):
    id_adherent: int


class NotificationResponse(NotificationBase):
    id: int
    id_adherent: int
    date: datetime

    class Config:
        orm_mode = True
