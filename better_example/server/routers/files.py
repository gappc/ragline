from typing import Annotated

from db import models
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from logger.custom_logger import logger
from server.auth import get_current_user
from utils.files import do_delete_file, do_get_files, do_upsert_file
from utils.paths import compute_docs_path

router = APIRouter()


@router.post("/files")
async def upsert_files(
    user: Annotated[models.User, Depends(get_current_user)],
    files: list[UploadFile],
):
    try:
        username = user.username
        for file in files:
            do_upsert_file(username, file.filename, file.file)
        return "OK"
    except Exception as e:
        logger.error("---------Error upsert_file---------")
        logger.exception(e)
        logger.error("---------Error upsert_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")
    finally:
        file.file.close()


@router.get("/files")
async def get_files(
    user: Annotated[models.User, Depends(get_current_user)],
):
    try:
        username = user.username
        return do_get_files(username)
    except Exception as e:
        logger.error("---------Error get_files---------")
        logger.exception(e)
        logger.error("---------Error get_files end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@router.get("/files/{filename}")
async def get_file(
    user: Annotated[models.User, Depends(get_current_user)], filename: str
):
    try:
        username = user.username
        path = compute_docs_path(username, filename)
        return FileResponse(path=path, filename=filename)
    except Exception as e:
        logger.error("---------Error get_file---------")
        logger.exception(e)
        logger.error("---------Error get_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@router.delete("/files/{filename}")
async def delete_file(
    user: Annotated[models.User, Depends(get_current_user)], filename: str
):
    try:
        username = user.username
        do_delete_file(username, filename)
        return "OK"
    except Exception as e:
        logger.error("---------Error delete_file---------")
        logger.exception(e)
        logger.error("---------Error delete_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")
