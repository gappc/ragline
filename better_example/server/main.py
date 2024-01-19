import os
from os.path import isfile, join

from pathlib import Path
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
from fastapi import FastAPI, File, HTTPException, Depends, Body, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from vector_store.weaviate_client import client, weaviate_collection_name
from llama_index.vector_stores.weaviate_utils import (
    parse_get_response,
)
import json

import logging
import sys

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from contextlib import asynccontextmanager

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
# app = FastAPI(dependencies=[Depends(validate_token)])

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")

# # Create a sub-application, in order to access just the query endpoint in an OpenAPI schema, found at http://0.0.0.0:8000/sub/openapi.json when the app is running locally
# sub_app = FastAPI(
#     title="Retrieval Plugin API",
#     description="A retrieval API for querying and filtering documents based on natural language queries and metadata",
#     version="1.0.0",
#     servers=[{"url": "https://your-app-url.com"}],
#     dependencies=[Depends(validate_token)],
# )
# app.mount("/sub", sub_app)

# from .llm import query


@app.get("/hello")
async def hello():
    return "Hello World!!!!"


from .utils import do_query, do_upsert_file


@app.post("/query")
async def post_query(
    request: QueryRequest = Body(...),
):
    try:
        print("-----------------got request-----------------")
        print(request)
        print("-----------------got response-----------------")
        response = do_query(request.queries[0].query)
        # print(response)
        print("-------------------------------------------")
        return StreamingResponse(response.response_gen, media_type="text/event-stream")
    except Exception as e:
        print("---------Error post_query---------")
        print(e)
        print("---------Error post_query end---------")
        raise HTTPException(status_code=500, detail="Internal Service Error")


@app.post("/files")
async def upsert_files(files: list[UploadFile]):
    try:
        for file in files:
            tmp_file_path = TMP_PATH + "/" + file.filename
            dest_file_path = DOCS_PATH + "/" + file.filename
            print("Creating file: %s" % tmp_file_path)
            with open(tmp_file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

                print("File created: %s, now ingesting" % tmp_file_path)

                result = do_upsert_file(tmp_file_path)

                print(
                    "Indexing complete for file %s, now moving to folder ",
                    tmp_file_path,
                )

                shutil.move(
                    tmp_file_path,
                    dest_file_path,
                )

        return "OK"

    except Exception as e:
        print("---------Error upsert_file---------")
        print(e)
        print("---------Error upsert_file end---------")
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
        print("---------Error get_file---------")
        print(e)
        print("---------Error get_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@app.delete("/files/{filename}")
async def delete_file(filename: str):
    try:
        path = DOCS_PATH + "/" + filename

        print("Deleting file: %s" % path)

        do_delete_file(path)
        print("File deleted: %s, now removing from index" % path)

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
        print(json.dumps(entries, indent=2))
        delete_result = client.batch.delete_objects(
            weaviate_collection_name, where_filter
        )
        print("Delete result: ", delete_result)
        print("Removing from index success")

        return "OK"
    except Exception as e:
        print("---------Error delete_file---------")
        print(e)
        print("---------Error delete_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
