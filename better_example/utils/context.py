from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.callbacks import CallbackManager
from utils.embeddings import embedding_model
from utils.llm import llm, token_counter
from vector_store.weaviate_client import vector_store

callback_manager = CallbackManager([token_counter])

# Build the service context
service_context = ServiceContext.from_defaults(
    llm=llm, embed_model=embedding_model, callback_manager=callback_manager
)

# Build the index and query engine
index = VectorStoreIndex.from_vector_store(vector_store, service_context)
query_engine = index.as_query_engine(streaming=True)

# Build the storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)
