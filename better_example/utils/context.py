from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from utils.embeddings import embedding_model
from utils.llm import llm
from vector_store.weaviate_client import vector_store

# Build the service context
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embedding_model)

# Build the index and query engine
index = VectorStoreIndex.from_vector_store(vector_store, service_context)
query_engine = index.as_query_engine(streaming=True)

# Build the storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)
