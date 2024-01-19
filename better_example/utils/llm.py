import os
from llama_index.llms import OpenAI, LLM

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
assert openai_api_key is not None

llm: LLM = OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.1)
