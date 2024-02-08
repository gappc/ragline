import logging
from itertools import tee
from typing import Annotated

import uvicorn
from db import models
from db.database import engine
from fastapi import BackgroundTasks, Body, Depends, FastAPI, HTTPException
from logger.custom_logger import InterceptHandler, logger_bind
from server.auth import get_current_user
from server.id import generate_id
from server.middlewares import RequestIdInjectionMiddleware
from server.routers import files, users
from server.utils import (
    extract_response_source,
    log_response,
    remove_embeddings,
    stream_response,
)
from utils.query import query_by_term

# Configure logging
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

from .api import FeedbackRequest, QueryRequest, SentimentRequest

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(RequestIdInjectionMiddleware)
app.include_router(users.router)
app.include_router(files.router)


@app.get("/hello")
async def hello(
    user: Annotated[models.User, Depends(get_current_user)],
):
    return "Hello " + user.username


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
