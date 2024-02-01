import os

import tiktoken

# Load environment variables from .env file
from dotenv import load_dotenv
from llama_index.callbacks import TokenCountingHandler
from llama_index.llms import LLM, OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key is not None

llm_model = "gpt-3.5-turbo"

token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model(llm_model).encode
)

llm: LLM = OpenAI(api_key=openai_api_key, model=llm_model, temperature=0.1)


def get_token_counts_as_text():
    return (
        "Embedding Tokens: ",
        token_counter.total_embedding_token_count,
        "\n",
        "LLM Prompt Tokens: ",
        token_counter.prompt_llm_token_count,
        "\n",
        "LLM Completion Tokens: ",
        token_counter.completion_llm_token_count,
        "\n",
        "Total LLM Token Count: ",
        token_counter.total_llm_token_count,
        "\n",
    )
