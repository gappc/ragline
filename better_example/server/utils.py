from utils.context import query_engine, index_documents
from llama_index import SimpleDirectoryReader


def do_query(query):
    response = query_engine.query(query)
    return response


def do_upsert_file(path: str):
    documents = SimpleDirectoryReader(input_files=[path]).load_data()
    return index_documents(documents)
