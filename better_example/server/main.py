import logging
from typing import Annotated

import uvicorn
from fastapi import Body, Depends, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from log.custom_logger import build_stdout_handler, logger
from server.auth import get_current_username
from server.middlewares import RequestIdInjectionMiddleware
from utils.files import compute_docs_path, do_delete_file, do_get_files, do_upsert_file
from utils.index import index_query_by_term

# Configure logging
logging.basicConfig(level=logging.DEBUG, handlers=[build_stdout_handler()])
logging.getLogger().addHandler(build_stdout_handler())


from .api import QueryRequest

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
    request: QueryRequest = Body(...),
):
    try:
        logger.info("-----------------got request-----------------")
        logger.info(request)
        logger.info("-----------------got response-----------------")
        response = index_query_by_term(username, request.queries[0].query)
        logger.info("-------------------------------------------")
        logger.info("response source nodes length: {}", len(response.source_nodes))

        # We assume that there is a streamable response if there are source nodes
        if len(response.source_nodes) > 0:
            return StreamingResponse(
                response.response_gen, media_type="text/event-stream"
            )

        async def gen():
            yield b"No documents found that match your query. Maybe you need to upload some documents first?"

        return StreamingResponse(gen(), media_type="text/event-stream", status_code=500)

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


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
