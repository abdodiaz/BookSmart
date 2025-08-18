from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import backend.models
import backend.database

router = APIRouter(
    prefix="/api/stats",
    tags=["stats"]
)

@router.get("/")
def get_statistics(db: Session = Depends(backend.database.get_db)):
    # 5 livres les plus empruntés
    top_livres = db.query(
        backend.models.Livre.titre,
        func.count(backend.models.Emprunt.id).label("nb_emprunts")
    ).join(backend.models.Emprunt).group_by(backend.models.Livre.id).order_by(func.count(backend.models.Emprunt.id).desc()).limit(5).all()

    # Taux de disponibilité global
    total_livres = db.query(func.count(backend.models.Livre.id)).scalar()
    livres_disponibles = db.query(func.count(backend.models.Livre.id)).filter(backend.models.Livre.stock > 0).scalar()
    taux_disponibilite = (livres_disponibles / total_livres * 100) if total_livres else 0

    # Nombre de retards
    retards = db.query(func.count(backend.models.Emprunt.id)).filter(
        backend.models.Emprunt.date_retour_effectif != None,
        backend.models.Emprunt.date_retour_effectif > backend.models.Emprunt.date_retour_prevue
    ).scalar()

    return {
        "top_livres": [{"titre": l[0], "nb_emprunts": l[1]} for l in top_livres],
        "taux_disponibilite": taux_disponibilite,
        "nombre_retards": retards
    }
