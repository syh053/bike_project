from sqlalchemy.orm import Session

from app.models.favorite import Favorite


def list_favorites(db: Session, *, user_id: int) -> list[Favorite]:
    return db.query(Favorite).filter(Favorite.user_id == user_id).order_by(Favorite.created_at.desc()).all()


def get_favorite(db: Session, *, user_id: int, station_no: str) -> Favorite | None:
    return (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.station_no == station_no)
        .first()
    )


def create_favorite(db: Session, *, user_id: int, station_no: str, station_name: str | None) -> Favorite:
    favorite = Favorite(user_id=user_id, station_no=station_no, station_name=station_name)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def delete_favorite(db: Session, *, favorite: Favorite) -> None:
    db.delete(favorite)
    db.commit()
