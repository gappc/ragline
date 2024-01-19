import sys
import time
import logging
import json

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from llama_index import SimpleDirectoryReader
from llama_index.vector_stores.weaviate_utils import (
    parse_get_response,
)

from utils.context import index_documents
from vector_store.weaviate_client import client, weaviate_collection_name


class IndexingEventHandler(LoggingEventHandler):
    def on_created(self, event):
        super().on_created(event)
        if event.is_directory:
            return
        print("File created: %s, now ingesting" % event.src_path)

        documents = SimpleDirectoryReader(input_files=[event.src_path]).load_data()
        index_documents(documents)

        print("Indexing complete for file %s", event.src_path)

    def on_deleted(self, event):
        super().on_deleted(event)
        if event.is_directory:
            return
        print("File deleted: %s, now removing from index" % event.src_path)
        # file_path => this is the weaviate property name that must be matched
        where_filter = {
            "path": ["file_path"],
            "operator": "Equal",
            "valueText": event.src_path,
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

    def on_moved(self, event):
        super().on_moved(event)
        if event.is_directory:
            return
        print("File moved: %s" % event.src_path, event.dest_path)


if __name__ == "__main__":
    path = "./docs"
    event_handler = IndexingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
