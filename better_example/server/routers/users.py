from db import crud, schemas
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from logger.custom_logger import logger
from server.auth import RoleChecker
from sqlalchemy.orm import Session
from utils.paths import create_user_paths, delete_user_paths

router = APIRouter()

allow_create_user = RoleChecker(["admin"])
allow_delete_user = RoleChecker(["admin"])


@router.post(
    "/users",
    response_model=schemas.User,
    dependencies=[Depends(allow_create_user)],
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud.create_user(db=db, user=user)
    logger.info("User created: {}", new_user)
    create_user_paths(new_user.username)
    return new_user


@router.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Reading users")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete(
    "/users/{user_id}",
    dependencies=[Depends(allow_delete_user)],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    username = crud.delete_user(db, user_id)
    if username is None:
        logger.error(f"User with ID {user_id} not found")
        return "OK"

    logger.info(f"User with ID {user_id} deleted: {username}")
    delete_user_paths(username)
    logger.info(f"User folders for user with ID {user_id} and name {username} deleted")
    return "OK"
