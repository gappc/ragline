from typing import List

from llama_index import Document, VectorStoreIndex
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters
from llama_index.vector_stores.weaviate_utils import parse_get_response
from logger.custom_logger import logger
from utils.context import index, service_context, storage_context, vector_store
from vector_store.weaviate_client import client, weaviate_collection_name

RAGLINE_USER_KEY = "ragline_user"


def _filename_where_filter(filename: str):
    return {
        "path": ["file_path"],
        "operator": "Equal",
        "valueText": filename,
    }


def _username_where_filter(username: str):
    return {
        "path": ["ragline_user"],
        "operator": "Equal",
        "valueText": username,
    }


def index_add_documents(username: str, documents: List[Document]):
    for document in documents:
        document.metadata[RAGLINE_USER_KEY] = username
    logger.info("----------------Documents to index----------------")
    logger.info([x for x in documents])
    logger.info("----------------End documents to index----------------")
    return VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
        storage_context=storage_context,
    )


def index_delete_by_path(username: str, filename: str):
    username_filter = _username_where_filter(username)
    filename_filter = _filename_where_filter(filename)
    where_filter = {"operator": "And", "operands": [username_filter, filename_filter]}
    print("where_filter", where_filter)
    return client.batch.delete_objects(weaviate_collection_name, where_filter)


def _index_query_by_path(path: str):
    where_filter = _filename_where_filter(path)
    query = (
        client.query.get(
            weaviate_collection_name, properties=["ref_doc_id", "file_path"]
        )
        .with_where(where_filter)
        .with_limit(10000)  # 10,000 is the max weaviate can fetch
    )
    query_result = query.do()
    parsed_result = parse_get_response(query_result)
    return parsed_result[weaviate_collection_name]


if __name__ == "__main__":
    # result = index_query_by_path(
    #     ".cache/tmp/chris/Innsbruck__verkaufe_35_Zi._Wohnung_neu_renoviert.pdf"
    # )
    # result = index_delete_by_path(
    #     ".cache/tmp/chris/Innsbruck__verkaufe_35_Zi._Wohnung_neu_renoviert.pdf"
    # )
    # print(result)
    result = _index_query_by_path(
        ".cache/tmp/chris/Innsbruck__verkaufe_35_Zi._Wohnung_neu_renoviert.pdf"
    )
    # result = index_query_by_term("chris", "Innsbruck")
    print(result)
