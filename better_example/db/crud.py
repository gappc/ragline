from logger.custom_logger import logger
from server.hasher import Hasher
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hasher.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, password=hashed_password, roles=user.roles
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    logger.debug("Deleting user {user_id}", user_id=user_id)
    db_user = get_user(db, user_id)
    if db_user is None:
        return None

    username = db_user.username
    logger.debug("Search user result: {}", username)
    db.delete(db_user)
    db.commit()
    logger.debug("Delete committed")
    return username
