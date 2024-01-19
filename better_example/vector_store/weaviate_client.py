import os
import json
import weaviate
from llama_index.vector_stores import WeaviateVectorStore

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

weaviate_collection_name = os.getenv("WEAVIATE_COLLECTION_NAME", "Ragline")
weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")

# Check if OPENAI_API_KEY environment variable is set, otherwise exit
if weaviate_collection_name is None:
    print("WEAVIATE_COLLECTION_NAME environment variable must be set, terminating...")
    exit(1)

client = weaviate.Client(weaviate_url)
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name=weaviate_collection_name
)


def show_collections():
    print("Collections:")
    collections = client.schema.get()
    print(json.dumps(collections, indent=2))


def show_collection(collection_name: str):
    collection = client.schema.get(collection_name)
    print(json.dumps(collection, indent=2))


def show_data(collection_name: str):
    data = client.data_object.get(class_name=collection_name)
    print(json.dumps(data, indent=2))


def ingest_data_into_collection(collection_name: str):
    client.schema.create_class(collection_name)
    print("Create successful")


def delete_collection(collection_name: str):
    client.schema.delete_class(class_name=collection_name)
    print("Delete successful")


def delete_data(collection_name: str, source):
    client.schema.delete_class(class_name=collection_name)
    print("Delete successful")


if __name__ == "__main__":
    show_collections()
