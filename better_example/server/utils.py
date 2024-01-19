from utils.context import query_engine, index_documents
from llama_index import SimpleDirectoryReader


def do_query(query):
    response = query_engine.query(query)
    return response


def do_upsert_file(path: str):
    documents = SimpleDirectoryReader(input_files=[path]).load_data()
    print("----------------Documents to index----------------")
    print([x for x in documents])
    print("----------------End documents to index----------------")
    return index_documents(documents)
