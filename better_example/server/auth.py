import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from log.custom_logger import logger

import json

fake_users_db = {
    "chris": {
        "username": "chris",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "nooneknows",
        "disabled": False,
    },
    "test": {
        "username": "test",
        "full_name": "test Doe",
        "email": "testdoe@example.com",
        "password": "123456",
        "disabled": False,
    },
}


security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    try:
        # This shortcut is problematic in terms of timing attacks
        user = fake_users_db.get(credentials.username)
        if user is None:
            raise Exception("User not found")

        logger.info("User found: {user}", user=user)

        # From here on it should be safe for timing attacks
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = user.get("username").encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        current_password_bytes = credentials.password.encode("utf8")
        correct_password_bytes = user.get("password").encode("utf8")
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # headers={"WWW-Authenticate": "Basic"},
        )

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            # headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
