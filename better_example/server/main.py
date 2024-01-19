import os
from pathlib import Path
from fastapi.responses import StreamingResponse
import uvicorn
from fastapi import FastAPI, File, HTTPException, Depends, Body, UploadFile
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

import logging
import sys

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from contextlib import asynccontextmanager

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


@app.post(
    "/upsert-file",
    # response_model=UpsertResponse,
)
async def upsert_file(
    file: UploadFile = File(...),
):
    try:
        # fake multiple files
        # files = [file]
        # for file in files:
        tmp_path = TMP_PATH + "/" + file.filename
        dest_path = DOCS_PATH + "/" + file.filename
        print("Creating file: %s" % tmp_path)
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

            print("File created: %s, now ingesting" % tmp_path)

            result = do_upsert_file(tmp_path)

            print("Indexing complete for file %s, now moving to folder ", tmp_path)

            shutil.move(
                tmp_path,
                dest_path,
            )

            return "OK"

    except Exception as e:
        print("---------Error upsert_file---------")
        print(e)
        print("---------Error upsert_file end---------")
        raise HTTPException(status_code=500, detail=f"str({e})")
    finally:
        file.file.close()


# @app.post(
#     "/upsert",
#     response_model=UpsertResponse,
# )
# async def upsert(
#     request: UpsertRequest = Body(...),
# ):
#     try:
#         ids = await datastore.upsert(request.documents)
#         return UpsertResponse(ids=ids)
#     except Exception as e:
#         print("---------Error upsert---------")
#         print(e)
#         print("---------Error upsert end---------")
#         raise HTTPException(status_code=500, detail="Internal Service Error")


# @app.delete(
#     "/delete",
#     response_model=DeleteResponse,
# )
# async def delete(
#     request: DeleteRequest = Body(...),
# ):
#     if not (request.ids or request.filter or request.delete_all):
#         raise HTTPException(
#             status_code=400,
#             detail="One of ids, filter, or delete_all is required",
#         )
#     try:
#         success = await datastore.delete(
#             ids=request.ids,
#             filter=request.filter,
#             delete_all=request.delete_all,
#         )
#         return DeleteResponse(success=success)
#     except Exception as e:
#         print("---------Error delete---------")
#         print(e)
#         print("---------Error delete end---------")
#         raise HTTPException(status_code=500, detail="Internal Service Error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=9000, reload=True)
