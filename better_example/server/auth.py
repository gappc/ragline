import secrets
from typing import Annotated, List

from db import crud
from db.database import get_db
from db.models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from logger.custom_logger import logger
from passlib.context import CryptContext
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


security = HTTPBasic()


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Session = Depends(get_db),
):
    user: User | None = None
    try:
        # This shortcut is problematic in terms of timing attacks
        # user = fake_users_db.get(credentials.username)
        user = crud.get_user_by_username(db, username=credentials.username)
        if user is None:
            raise Exception("User not found")

        logger.info("User found: {username}", username=credentials.username)

        # From here on it should be safe for timing attacks
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = user.username.encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )

        is_correct_password = Hasher.verify_password(
            credentials.password, user.password
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not (is_correct_username and is_correct_password):
        logger.error(
            "is_correct_username {}, is_correct_password {}",
            is_correct_username,
            is_correct_password,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        user_roles: List[str] = user.roles.split(",")
        logger.debug(f"User roles: {user_roles}")
        logger.debug(f"Allowed roles: {self.allowed_roles}")
        is_allowed = self.has_any_roles(user_roles, self.allowed_roles)
        logger.debug(f"Is allowed: {is_allowed}")
        if not is_allowed:
            logger.debug(f"User with role {user.roles} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")

    def has_any_roles(self, list1: List[str], list2):
        logger.debug(f"Checking if {list1} has any roles in {list2}")
        for val in list1:
            if val in list2:
                return True
        return False
