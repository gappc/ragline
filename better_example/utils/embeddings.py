import os

from dotenv import load_dotenv
from llama_index.embeddings import BaseEmbedding, HuggingFaceEmbedding

load_dotenv()

embed_batch_size = os.getenv("EMBEDDING_BATCH_SIZE", 1)

embedding_model: BaseEmbedding = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./.cache/huggingface",
    embed_batch_size=embed_batch_size,
)
