import logging
from itertools import tee
from typing import Annotated

import uvicorn
from utils.paths import create_user_paths, delete_user_paths
from db import crud, models, schemas
from db.database import get_db, engine
from fastapi import BackgroundTasks, Body, Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from logger.custom_logger import InterceptHandler, logger, logger_bind
from server.auth import RoleChecker, get_current_user
from server.id import generate_id
from server.middlewares import RequestIdInjectionMiddleware
from server.utils import (
    extract_response_source,
    log_response,
    remove_embeddings,
    stream_response,
)
from sqlalchemy.orm import Session
from utils.files import compute_docs_path, do_delete_file, do_get_files, do_upsert_file
from utils.query import query_by_term

# Configure logging
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

from .api import FeedbackRequest, QueryRequest, SentimentRequest

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(RequestIdInjectionMiddleware)

allow_create_user = RoleChecker(["admin"])
allow_delete_user = RoleChecker(["admin"])


@app.get("/hello")
async def hello(
    user: Annotated[models.User, Depends(get_current_user)],
):
    return "Hello " + user.username


@app.post(
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


@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Reading users")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete(
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


@app.post("/conversation")
async def post_conversation(
    user: Annotated[models.User, Depends(get_current_user)],
):
    # Generate new conversation ID
    conversation_id = generate_id()

    # Create a new conversation logger
    logger = logger_bind(conversation_id, None)
    logger.info("Username: {} started new conversation with ID {}", user.username)

    # TODO: create folder for conversation

    return conversation_id


@app.post("/query/{conversation_id}")
async def post_query(
    user: Annotated[models.User, Depends(get_current_user)],
    background_tasks: BackgroundTasks,
    conversation_id: str,
    request: QueryRequest = Body(...),
):
    # Generate new query ID
    query_id = generate_id()

    # Use the conversation logger
    logger = logger_bind(conversation_id, query_id)
    try:
        username = user.username
        logger.info("Username: {}", username)
        logger.info("Request: {}", request)

        # Do the query
        response = query_by_term(username, request.queries[0].query)

        logger.info("Source nodes: {}", remove_embeddings(response.source_nodes))

        response_source = extract_response_source(response.source_nodes)

        logger.info("Response Source nodes short: {}", response_source)

        logger.info("Metadata: {}", response.metadata)

        # Create one stream for the response and one for logging
        [response_stream, response_stream_log] = (
            # If no documents were found, return the streams from string
            [
                "No documents found that match your query. Maybe you need to upload some documents first?",
                "No documents found that match your query",
            ]
            if response.source_nodes is None
            # Otherwise, duplicate the streaming response
            else tee(response.response_gen, 2)
        )

        # Log the response after the response was send
        background_tasks.add_task(
            log_response, conversation_id, query_id, response_stream_log
        )

        # Return response stream
        return stream_response(query_id, response_stream, response_source)
    except Exception as e:
        logger.error("---------Error post_query---------")
        logger.exception(e)
        logger.error("---------Error post_query end---------")
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post("/files")
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


@app.get("/files")
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


@app.get("/files/{filename}")
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


@app.delete("/files/{filename}")
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


@app.post("/sentiment/{conversation_id}/{query_id}")
async def post_sentiment(
    user: Annotated[models.User, Depends(get_current_user)],
    conversation_id: str,
    query_id: str,
    request: SentimentRequest = Body(...),
):
    logger = logger_bind(conversation_id, query_id)
    logger.info("Sentiment: {}", request.sentiment)
    return "OK"


@app.post("/feedback/{conversation_id}/{query_id}")
async def post_feedback(
    user: Annotated[models.User, Depends(get_current_user)],
    conversation_id: str,
    query_id: str,
    request: FeedbackRequest = Body(...),
):
    logger = logger_bind(conversation_id, query_id)
    logger.info("Feedback: {}", request.feedback)
    return "OK"


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
