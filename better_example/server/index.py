from typing import List
from llama_index import Document
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters
from log.custom_logger import logger
from utils.context import index, index_documents

RAGLINE_USER_KEY = "ragline_user"


def do_index(username: str, documents: List[Document]):
    for document in documents:
        document.metadata[RAGLINE_USER_KEY] = username
    logger.info("----------------Documents to index----------------")
    logger.info([x for x in documents])
    logger.info("----------------End documents to index----------------")
    return index_documents(documents)


def do_query(username: str, query: str):
    query_engine = index.as_query_engine(
        streaming=True,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key=RAGLINE_USER_KEY,
                    value=username,
                )
            ]
        ),
        similarity_top_k=3,
    )
    response = query_engine.query(query)
    return response
