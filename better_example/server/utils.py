from utils.context import query_engine, index_documents
from llama_index import SimpleDirectoryReader
from log.custom_logger import logger


def do_query(query):
    response = query_engine.query(query)
    return response


def do_upsert_file(path: str):
    documents = SimpleDirectoryReader(input_files=[path]).load_data()
    logger.info("----------------Documents to index----------------")
    logger.info([x for x in documents])
    logger.info("----------------End documents to index----------------")
    return index_documents(documents)
