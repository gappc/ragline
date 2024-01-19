from llama_index.embeddings import BaseEmbedding, HuggingFaceEmbedding

embedding_model: BaseEmbedding = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5", cache_folder="./.cache/huggingface"
)
