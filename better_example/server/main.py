import os

from pathlib import Path
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Body, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from server.middlewares import RequestIdInjectionMiddleware

from vector_store.weaviate_client import client, weaviate_collection_name
from llama_index.vector_stores.weaviate_utils import (
    parse_get_response,
)
import json

import logging
from log.custom_logger import logger, build_stdout_handler

# Configure logging
logging.basicConfig(level=logging.DEBUG, handlers=[build_stdout_handler()])
logging.getLogger().addHandler(build_stdout_handler())

from .files import do_get_files, do_delete_file
import shutil

from .api import (
    QueryRequest,
)

from dotenv import load_dotenv

load_dotenv()

DOCS_PATH = os.getenv("DOCS_PATH", "./.cache/docs")
TMP_PATH = os.getenv("TMP_PATH", "./.cache/tmp")

Path(DOCS_PATH).mkdir(exist_ok=True)
Path(TMP_PATH).mkdir(exist_ok=True)

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
# assert BEARER_TOKEN is not None


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials


app = FastAPI()
app.add_middleware(RequestIdInjectionMiddleware)


@app.get("/hello")
async def hello():
    return "Hello World!!!!"


from .utils import do_query, do_upsert_file


@app.post("/query")
async def post_query(
    request: QueryRequest = Body(...),
):
    try:
        logger.info("-----------------got request-----------------")
        logger.info(request)
        logger.info("-----------------got response-----------------")
        response = do_query(request.queries[0].query)
        logger.info("-------------------------------------------")
        logger.info("response source nodes length: {}", len(response.source_nodes))
        # We assume that there is a streamable response if there are source nodes
        if len(response.source_nodes) > 0:
            return StreamingResponse(
                response.response_gen, media_type="text/event-stream"
            )

        async def gen():
            yield b"No documents found that match your query. Maybe you need to upload some documents first?"

        return StreamingResponse(gen(), media_type="text/event-stream", status_code=404)

    except Exception as e:
        logger.error("---------Error post_query---------")
        logger.exception(e)
        logger.error("---------Error post_query end---------")
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post("/files")
async def upsert_files(files: list[UploadFile]):
    try:
        for file in files:
            tmp_file_path = TMP_PATH + "/" + file.filename
            dest_file_path = DOCS_PATH + "/" + file.filename
            logger.info("Creating file: {}", tmp_file_path)
            with open(tmp_file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

                logger.info("File created: {}, now ingesting", tmp_file_path)

                result = do_upsert_file(tmp_file_path)

                logger.info(
                    "Indexing complete for file {}, now moving to folder ",
                    tmp_file_path,
                )

                shutil.move(
                    tmp_file_path,
                    dest_file_path,
                )

        return "OK"

    except Exception as e:
        logger.error("---------Error upsert_file---------")
        logger.exception(e)
        logger.error("---------Error upsert_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")
    finally:
        file.file.close()


@app.get("/files")
async def get_files():
    return do_get_files(DOCS_PATH)


@app.get("/files/{filename}")
async def get_file(filename: str):
    path = DOCS_PATH + "/" + filename

    try:
        return FileResponse(path=path, filename=filename)
    except Exception as e:
        logger.error("---------Error get_file---------")
        logger.exception(e)
        logger.error("---------Error get_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.delete("/files/{filename}")
async def delete_file(filename: str):
    try:
        path = DOCS_PATH + "/" + filename

        logger.info("Deleting file: {}", path)

        do_delete_file(path)
        logger.info("File deleted: {}, now removing from index", path)

        where_filter = {
            "path": ["file_path"],
            "operator": "Equal",
            "valueText": filename,
        }
        query = (
            client.query.get(
                weaviate_collection_name, properties=["ref_doc_id", "file_path"]
            )
            .with_where(where_filter)
            .with_limit(10000)  # 10,000 is the max weaviate can fetch
        )
        query_result = query.do()
        parsed_result = parse_get_response(query_result)
        entries = parsed_result[weaviate_collection_name]
        logger.info(json.dumps(entries, indent=2))
        delete_result = client.batch.delete_objects(
            weaviate_collection_name, where_filter
        )
        logger.info("Delete result: ", delete_result)
        logger.info("Removing from index success")

        return "OK"
    except Exception as e:
        logger.error("---------Error delete_file---------")
        logger.exception(e)
        logger.error("---------Error delete_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
