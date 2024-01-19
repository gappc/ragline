import logging
import sys
from llama_index import SimpleDirectoryReader
from utils.context import index_documents

# set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# load documents
documents = SimpleDirectoryReader("./docs").load_data()

# index documents
index = index_documents(documents)

print("Indexing complete")
