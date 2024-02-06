import logging
from itertools import tee
from typing import Annotated

import uvicorn
from fastapi import BackgroundTasks, Body, Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from logger.custom_logger import (
    InterceptHandler,
    logger_bind,
    logger,
)
from server.auth import get_current_username
from server.id import generate_id
from server.middlewares import RequestIdInjectionMiddleware
from server.utils import (
    extract_response_source,
    log_response,
    remove_embeddings,
    stream_response,
)
from utils.files import compute_docs_path, do_delete_file, do_get_files, do_upsert_file
from utils.query import query_by_term

# Configure logging
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

from .api import FeedbackRequest, QueryRequest, SentimentRequest

app = FastAPI()
app.add_middleware(RequestIdInjectionMiddleware)


@app.get("/hello")
async def hello(
    username: Annotated[str, Depends(get_current_username)],
):
    return "Hello " + username


@app.post("/conversation")
async def post_conversation(
    username: Annotated[str, Depends(get_current_username)],
):
    # Generate new conversation ID
    conversation_id = generate_id()

    # Create a new conversation logger
    logger = logger_bind(conversation_id)
    logger.info("Username: {} started new conversation with ID {}", username)

    # TODO: create folder for conversation

    return conversation_id


@app.post("/query/{conversation_id}")
async def post_query(
    username: Annotated[str, Depends(get_current_username)],
    background_tasks: BackgroundTasks,
    conversation_id: str,
    request: QueryRequest = Body(...),
):
    # Generate new query ID
    query_id = generate_id()

    # Use the conversation logger
    logger = logger_bind(conversation_id, query_id)
    try:
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
    username: Annotated[str, Depends(get_current_username)],
    files: list[UploadFile],
):
    try:
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
    username: Annotated[str, Depends(get_current_username)],
):
    try:
        return do_get_files(username)
    except Exception as e:
        logger.error("---------Error get_files---------")
        logger.exception(e)
        logger.error("---------Error get_files end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.get("/files/{filename}")
async def get_file(
    username: Annotated[str, Depends(get_current_username)], filename: str
):
    try:
        path = compute_docs_path(username, filename)
        return FileResponse(path=path, filename=filename)
    except Exception as e:
        logger.error("---------Error get_file---------")
        logger.exception(e)
        logger.error("---------Error get_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.delete("/files/{filename}")
async def delete_file(
    username: Annotated[str, Depends(get_current_username)], filename: str
):
    try:
        do_delete_file(username, filename)
        return "OK"
    except Exception as e:
        logger.error("---------Error delete_file---------")
        logger.exception(e)
        logger.error("---------Error delete_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.post("/sentiment/{conversation_id}/{query_id}")
async def post_sentiment(
    username: Annotated[str, Depends(get_current_username)],
    conversation_id: str,
    query_id: str,
    request: SentimentRequest = Body(...),
):
    logger = logger_bind(conversation_id, query_id)
    logger.info("Sentiment: {}", request.sentiment)
    return "OK"


@app.post("/feedback/{conversation_id}/{query_id}")
async def post_feedback(
    username: Annotated[str, Depends(get_current_username)],
    conversation_id: str,
    query_id: str,
    request: FeedbackRequest = Body(...),
):
    logger = logger_bind(conversation_id, query_id)
    logger.info("Feedback: {}", request.feedback)
    return "OK"


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
