import logging
from itertools import tee
from typing import Annotated

import uvicorn
from fastapi import BackgroundTasks, Body, Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from logger.custom_logger import (
    build_stdout_handler,
    logger,
    new_query_logger,
    query_logger_for_qid,
)
from server.auth import get_current_username
from server.middlewares import RequestIdInjectionMiddleware
from server.utils import extract_response_source, log_response, stream_response
from utils.files import compute_docs_path, do_delete_file, do_get_files, do_upsert_file
from utils.query import query_by_term

# Configure logging
logging.basicConfig(level=logging.DEBUG, handlers=[build_stdout_handler()])
logging.getLogger().addHandler(build_stdout_handler())


from .api import FeedbackRequest, QueryRequest, SentimentRequest

app = FastAPI()
app.add_middleware(RequestIdInjectionMiddleware)


@app.get("/hello")
async def hello(
    username: Annotated[str, Depends(get_current_username)],
):
    return "Hello " + username


@app.post("/query")
async def post_query(
    username: Annotated[str, Depends(get_current_username)],
    background_tasks: BackgroundTasks,
    request: QueryRequest = Body(...),
):
    # Create a new query logger
    [query_id, query_logger] = new_query_logger()
    try:
        query_logger.info("Username: {}", username)
        query_logger.info("Request: {}", request)

        # Do the query
        response = query_by_term(username, request.queries[0].query)

        query_logger.info("Source nodes: {}", response.source_nodes)

        response_source = extract_response_source(response.metadata)

        query_logger.info("Response Source nodes short: {}", response_source)

        query_logger.info("Metadata: {}", response.metadata)

        # Create one stream for the response and one for logging
        [response_stream, response_stream_log] = (
            # If no documents were found, return the streams from string
            [
                "No documents found that match your query. Maybe you need to upload some documents first?",
                "No documents found that match your query",
            ]
            if response.metadata is None
            # Otherwise, duplicate the streaming response
            else tee(response.response_gen, 2)
        )

        # Log the response after the response was send
        background_tasks.add_task(log_response, query_id, response_stream_log)

        # Return response stream
        return stream_response(query_id, response_stream, response_source)
    except Exception as e:
        query_logger.error("---------Error post_query---------")
        query_logger.exception(e)
        query_logger.error("---------Error post_query end---------")
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


@app.post("/sentiment/{query_id}")
async def post_sentiment(
    username: Annotated[str, Depends(get_current_username)],
    query_id: str,
    request: SentimentRequest = Body(...),
):
    query_logger = query_logger_for_qid(query_id)
    query_logger.info("Sentiment: {}", request.sentiment)
    return "OK"


@app.post("/feedback/{query_id}")
async def post_feedback(
    username: Annotated[str, Depends(get_current_username)],
    query_id: str,
    request: FeedbackRequest = Body(...),
):
    query_logger = query_logger_for_qid(query_id)
    query_logger.info("Feedback: {}", request.feedback)
    return "OK"


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
